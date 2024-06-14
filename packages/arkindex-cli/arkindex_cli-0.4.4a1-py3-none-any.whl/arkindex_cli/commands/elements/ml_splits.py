# -*- coding: utf-8 -*-
import logging
import random
from argparse import ArgumentTypeError
from dataclasses import dataclass
from itertools import chain, permutations
from operator import attrgetter
from pathlib import Path
from textwrap import dedent
from typing import Optional
from urllib.parse import urljoin
from uuid import UUID

from apistar.exceptions import ErrorResponse
from rich.progress import track

from arkindex_cli.auth import Profiles

logger = logging.getLogger(__name__)


@dataclass
class Set:
    name: str
    ratio: float

    def __post_init__(self) -> None:
        try:
            self.ratio = float(self.ratio)
        except (ValueError, TypeError):
            raise Exception(f"'{self.ratio}' is not a valid number")

    def check(self) -> None:
        assert (
            0 < self.ratio < 1
        ), f"The ratio of the {self.name} set must be strictly between 0 and 1 (not included)."


class Splits:
    """
    Split the elements of one or more given element type(s) inside a project or parent
    element between several sets for machine learning processes.
    """

    def __init__(
        self,
        profile_slug: Optional[str] = None,
        gitlab_secure_file: Optional[Path] = None,
        project: Optional[UUID] = None,
        folder: Optional[UUID] = None,
        element_type: Optional[list] = ["page"],
        dataset_name: Optional[str] = "Training dataset",
        sets: Optional[list[Set]] = [
            Set(name="train", ratio=0.8),
            Set(name="dev", ratio=0.1),
            Set(name="test", ratio=0.1),
        ],
        nb_elements: Optional[int] = None,
        recursive: Optional[bool] = False,
    ):
        self.project_id = project
        self.folder_id = folder
        self.types = element_type
        self.dataset_name = dataset_name
        self.sets = sets
        self.nb_elems = nb_elements
        self.children_recursive = recursive

        profiles = Profiles(gitlab_secure_file)
        # The profile URL is used later on
        profile = profiles.get_or_exit(profile_slug)
        self.instance_url = profile.url
        self.api_client = profiles.get_api_client(profile)

    def check_arguments(self):
        # --project and --folder are mutually exclusive
        assert (self.project_id is None) ^ (
            self.folder_id is None
        ), "Only one of --project or --folder may be set."

        # The --recursive option only makes sense if using a folder element
        if self.children_recursive:
            assert (
                self.folder_id
            ), "The --recursive option can only be used with the --folder one."

        # Check the sets
        assert len(self.sets), "The --set option should have at least one value."

        # Check the ratios
        for set_object in self.sets:
            set_object.check()

        # Check that the sum of all the ratios is 1
        assert (
            sum(map(attrgetter("ratio"), self.sets)) == 1
        ), "The sum of the set ratios must be equal to 1."

        # Check that the given parent folder exists
        if self.folder_id:
            logger.info("Retrieving parent element…")
            try:
                folder = self.api_client.request("RetrieveElement", id=self.folder_id)
            except ErrorResponse as e:
                if e.status_code == 404:
                    raise ValueError(
                        f"Parent element {self.folder_id} does not exist. Check the UUID."
                    ) from None
                else:
                    raise

        self.project_id = self.project_id or folder["corpus"]["id"]

        # Check that the given parent project exists
        logger.info("Retrieving project information…")
        try:
            corpus = self.api_client.request("RetrieveCorpus", id=self.project_id)
        except ErrorResponse as e:
            if e.status_code == 404:
                raise ValueError(
                    f"Project {self.project_id} does not exist. Check the UUID."
                ) from None
            else:
                raise

        # Check that the parent folder is a folder
        folder_types = [
            item["slug"]
            for item in corpus["types"]
            if "folder" in item and item["folder"]
        ]
        if self.folder_id and folder["type"] not in folder_types:
            logger.warning(f"Parent element {folder['name']} is not a folder type.")

        # Check that the given element types exist in the project
        type_slugs = [item["slug"] for item in corpus["types"]]
        missing = [item for item in self.types if item not in type_slugs]
        assert (
            len(missing) == 0
        ), f"Element type(s) {', '.join(missing)} not found in project {corpus['name']}."

    def make_splits(self, elements) -> dict[str, list]:
        # Shuffle the list of IDs
        random.shuffle(elements)

        # Use nb_elems if set
        if self.nb_elems:
            if self.nb_elems > len(elements):
                logger.warning(
                    dedent(
                        f"The number of elements to use was set to {self.nb_elems}, but only "
                        f"{len(elements)} were returned. Using all the returned elements."
                    )
                )
            else:
                elements = elements[: self.nb_elems]

        # Build the sets
        splits, nb_assigned = {}, 0
        for set_object in self.sets:
            to_assign = nb_assigned + int(set_object.ratio * len(elements))
            splits[set_object.name] = elements[nb_assigned:to_assign]
            nb_assigned = to_assign

        # `int` rounded down so some elements were not assigned to any set
        for set_name, element in zip(
            map(attrgetter("name"), self.sets), elements[nb_assigned:]
        ):
            splits[set_name].append(element)

        # Make some checks
        used_elements = list(chain.from_iterable(splits.values()))
        assert len(used_elements) == len(
            elements
        ), f"{len(elements)} elements were retrieved but {len(used_elements)} elements were used in the splits."

        for (set_name_1, set_elements_1), (set_name_2, set_elements_2) in permutations(
            splits.items(), r=2
        ):
            common_items = set(set_elements_1).intersection(set(set_elements_2))
            assert (
                not common_items
            ), f"{len(common_items)} items are present both in the `{set_name_1}` and `{set_name_2}` sets."

        return splits

    def create_dataset(self, splits: dict[str, list]) -> dict:
        try:
            dataset = self.api_client.request(
                "CreateDataset",
                id=self.project_id,
                body={
                    "name": self.dataset_name,
                    "description": "Dataset created with the CLI command",
                    "set_names": list(splits),
                },
            )
        except ErrorResponse as e:
            error_message = e.content
            if e.status_code == 400:
                if (
                    "A dataset with this name already exists in this corpus"
                    in e.content.get("non_field_errors", [])[0]
                ):
                    error_message = (
                        f"A dataset with the name {self.dataset_name} already exists in the project.\n"
                        "You can set a different name using the --dataset-name parameter."
                    )
            raise ValueError(
                f"Failed creating dataset: {e.status_code} -- {error_message}"
            ) from e
        return dataset

    def link(self, dataset: dict, set_name: str, elements: set):
        for item in track(
            elements,
            transient=True,
            description=f"Linking {len(elements)} elements to set {set_name}",
        ):
            try:
                self.api_client.request(
                    "CreateDatasetElement",
                    id=dataset["id"],
                    body={
                        "element_id": item,
                        "set": set_name,
                    },
                )
            except ErrorResponse as e:
                logger.error(
                    f"Failed to add element {item} to set {set_name} of dataset {dataset['name']} ({dataset['id']}): {e.status_code} - {e.content}"
                )

    def run(self):
        self.check_arguments()
        elements = []
        for element_type in self.types:
            logger.info(f"Retrieving {element_type} elements…")
            if self.folder_id:
                response = self.api_client.paginate(
                    "ListElementChildren",
                    id=self.folder_id,
                    type=element_type,
                    recursive=self.children_recursive,
                )
            elif self.project_id:
                response = self.api_client.paginate(
                    "ListElements", corpus=self.project_id, type=element_type
                )
            elements += [item["id"] for item in response]
        assert len(elements), "No elements were returned."

        splits = self.make_splits(elements)
        dataset = self.create_dataset(splits)

        for set_name, elements in splits.items():
            self.link(dataset, set_name, elements)

        dataset_url = urljoin(self.instance_url, f"dataset/{dataset['id']}")
        logger.info(
            f"Training dataset successfully created! You can access it here: {dataset_url}."
        )


def check_set(value: str) -> Set:
    values = value.split(":")
    if len(values) != 2:
        raise ArgumentTypeError(
            f"'{value}' is not in the correct format `<set_name>:<set_ratio>`"
        )

    set_name, set_ratio = values
    try:
        return Set(name=set_name, ratio=set_ratio)
    except Exception as e:
        raise ArgumentTypeError(str(e))


def add_splits_parser(subcommands):
    splits_parser = subcommands.add_parser(
        "ml-splits",
        description="Split elements between several sets and create a dataset.",
        help="""
            Create a dataset for machine learning training and testing.
            Split elements of one or more given element types, belonging to a project
            or a given parent element, between several sets according to a given ratio.
        """,
    )
    source = splits_parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--project",
        help="UUID of a project to get the elements from and where the dataset will be created.",
        type=UUID,
    )
    source.add_argument(
        "--folder",
        help="UUID of a parent element to get the elements from.",
        type=UUID,
    )
    splits_parser.add_argument(
        "--element-type",
        help="One or more element types to retrieve. Defaults to 'page'.",
        type=str,
        nargs="+",
        default=["page"],
    )
    splits_parser.add_argument(
        "--recursive",
        help="Recursively list children elements (if using a folder element).",
        action="store_true",
    )
    splits_parser.add_argument(
        "--set",
        help="""
            The name of the set with the portion of the retrieved elements to put in it, separated by a colon.
            The portion must be a number between 0 and 1.
            0 (no data) and 1 (all data) are not valid values.
            Defaults to ["train:0.8", "dev:0.1", "test:0.1"]
        """,
        type=check_set,
        nargs="+",
        default=list(map(check_set, ["train:0.8", "dev:0.1", "test:0.1"])),
        dest="sets",
    )
    splits_parser.add_argument(
        "--dataset-name",
        help="""
            The name of the dataset which will be created and containing the sets.
            Defaults to "Training dataset".
        """,
        type=str,
        default="Training dataset",
    )
    splits_parser.add_argument(
        "--nb-elements",
        help="""
            Limit the number of retrieved elements. If not set, all elements corresponding
            to the given element type and parent UUID will be retrieved.
        """,
        type=int,
    )
    splits_parser.set_defaults(func=run)


def run(
    profile_slug: Optional[str] = None,
    gitlab_secure_file: Optional[Path] = None,
    **kwargs,
):
    Splits(profile_slug, gitlab_secure_file, **kwargs).run()
