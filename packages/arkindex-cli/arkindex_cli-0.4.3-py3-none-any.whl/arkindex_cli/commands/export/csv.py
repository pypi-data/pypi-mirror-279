# -*- coding: utf-8 -*-

import csv
import fnmatch
import logging
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import chain, repeat, starmap
from pathlib import Path
from typing import List, Optional
from uuid import UUID

from arkindex_cli.commands.export.utils import uuid_or_manual
from arkindex_export import (
    Classification,
    Element,
    ElementPath,
    Entity,
    EntityType,
    Image,
    Metadata,
    Transcription,
    TranscriptionEntity,
    open_database,
)
from arkindex_export.queries import list_children, list_parents
from peewee import JOIN, fn

logger = logging.getLogger(__name__)


def get_elements(parent_id=None, element_type=None, recursive=False):
    elements = Element.select()
    if parent_id:
        elements = elements.join(
            ElementPath, on=(Element.id == ElementPath.child_id)
        ).where(ElementPath.parent_id == parent_id)
        if recursive:
            elements = list_children(parent_id)
    if element_type:
        elements = elements.where(Element.type == element_type)
    return elements


def classes_columns(elements, classification_worker_version=None):
    classifications = Classification.select(
        Classification.class_name,
        Classification.element_id,
        fn.COUNT("*").alias("count"),
    ).group_by(Classification.element_id, Classification.class_name)
    # Filter by element id if the exported elements have been filtered by parent or type
    if elements is not None:
        classifications = classifications.where(
            Classification.element_id.in_(elements.select(Element.id))
        )
    if classification_worker_version:
        if classification_worker_version == "manual":
            classifications = classifications.where(
                Classification.worker_version_id.is_null()
            )
        else:
            classifications = classifications.where(
                Classification.worker_version_id == classification_worker_version
            )

    with_count = (
        Classification.select(
            classifications.c.class_name,
            fn.MAX(classifications.c.count).alias("max_count"),
        )
        .from_(classifications)
        .group_by(classifications.c.class_name)
        .order_by(classifications.c.class_name)
    )

    columns = list(chain.from_iterable(starmap(repeat, with_count.tuples())))
    return columns


def entity_type_columns(elements, entities_worker_version=None):
    entity_types = (
        EntityType.select(
            EntityType.name, Transcription.element_id, fn.COUNT("*").alias("count")
        )
        .join(Entity)
        .join(TranscriptionEntity)
        .join(Transcription)
        .group_by(Transcription.element_id, EntityType.name)
    )
    # Filter by element id if the exported elements have been filtered by parent or type
    if elements is not None:
        entity_types = entity_types.where(
            Transcription.element_id.in_(elements.select(Element.id))
        )
    if entities_worker_version:
        if entities_worker_version == "manual":
            entity_types = entity_types.where(
                TranscriptionEntity.worker_version_id.is_null()
            )
        else:
            entity_types = entity_types.where(
                TranscriptionEntity.worker_version_id == entities_worker_version
            )

    with_count = (
        EntityType.select(
            entity_types.c.name, fn.MAX(entity_types.c.count).alias("max_count")
        )
        .from_(entity_types)
        .group_by(entity_types.c.name)
        .order_by(entity_types.c.name)
    )

    # Build an alphabetically ordered list of columns, containing each entity type as many times as the max_count
    columns = list(chain.from_iterable(starmap(repeat, with_count.tuples())))

    return columns


def metadata_columns(elements, load_parents=False):
    """
    When using the with_parent_metadata option, for each element we need to retrieve its own
    metadata as well as the metadata of every one of its parents: we need to recursively list
    all the parents of every relevant element.
    To do so, we build a recursive subquery that returns two columns:
    - exported_element_id (the elements which correspond to a line in the output CSV)
    - metadata_element_id (the parent elements whose metadata are added to the element's own).
    When the with_parent_metadata option isn't used, the two columns contain the same elements.
    This recursive subquery is then joined with the Metadata table, adding all of an element's
    parents' metadata to its own metadata, to be output on its line in the CSV.
    """
    # Use all elements when there are no parent or type filters
    if elements is None:
        elements = Element.select()

    # Removing the ordering by elements as it cannot come before the UNION clause.
    base = (
        elements.order_by()
        .select(Element.id, Element.id)
        .cte(
            "element_parents",
            recursive=load_parents,
            columns=("exported_element_id", "metadata_element_id"),
        )
    )
    if load_parents:
        parents = ElementPath.select(
            base.c.exported_element_id, ElementPath.parent_id
        ).join(base, on=(base.c.metadata_element_id == ElementPath.child_id))
        cte = base.union(parents)
    # If not loading the parents' metadata, the CTE doesn't become recursive and the metadata
    # elements are the same as the exported elements.
    else:
        cte = base

    metadata = (
        Metadata.select(
            Metadata.name, cte.c.exported_element_id, fn.COUNT("*").alias("count")
        )
        .join(cte, on=(Metadata.element_id == cte.c.metadata_element_id))
        .group_by(Metadata.name, cte.c.exported_element_id)
    )

    # If elements listing is recursive, using list_children from arkindex_export, then `elements`
    # already has a CTE and defining a new one overwrites it (see
    # https://docs.peewee-orm.com/en/latest/peewee/api.html#Query.with_cte). However, we can use
    # the hidden `_cte_list` attribute to retrieve it
    # (https://github.com/coleifer/peewee/blob/a6f479dc0e8063a9a7f7053b04d93f34d67737ce/peewee.py#L2111)
    if elements._cte_list:
        metadata = metadata.with_cte(*elements._cte_list, cte)
    else:
        metadata = metadata.with_cte(cte)

    with_count = (
        Metadata.select(metadata.c.name, fn.MAX(metadata.c.count).alias("max_count"))
        .from_(metadata)
        .group_by(metadata.c.name)
        .order_by(metadata.c.name)
    )

    # Build an alphabetically ordered list of columns, containing each metadata name as many times as the max_count
    columns = list(chain.from_iterable(starmap(repeat, with_count.tuples())))
    return columns


def element_classes(element_id, classification_worker_version=None):
    element_classifications = Classification.select(
        Classification.class_name, Classification.confidence
    ).where(Classification.element_id == element_id)
    if classification_worker_version:
        if classification_worker_version == "manual":
            element_classifications = element_classifications.where(
                Classification.worker_version_id.is_null()
            )
        else:
            element_classifications = element_classifications.where(
                Classification.worker_version_id == classification_worker_version
            )
    return element_classifications


def element_entities(element_id, entities_worker_version=None):
    entities = (
        EntityType.select(
            EntityType.name.alias("type_name"),
            Entity.name.alias("name"),
            fn.ROW_NUMBER().over(partition_by=([EntityType.name])).alias("number"),
        )
        .join(Entity)
        .join(TranscriptionEntity)
        .join(Transcription)
        .where(Transcription.element_id == element_id)
        .group_by(Entity.id)
        .order_by(EntityType.name, Entity.name)
    )
    if entities_worker_version:
        if entities_worker_version == "manual":
            entities = entities.where(TranscriptionEntity.worker_version_id.is_null())
        else:
            entities = entities.where(
                TranscriptionEntity.worker_version_id == entities_worker_version
            )
    return entities.namedtuples()


def element_metadata(
    element_id,
    load_parents=False,
):
    metadata = Metadata.select(Metadata.name, Metadata.value).where(
        Metadata.element_id == element_id
    )
    if load_parents:
        metadata = Metadata.select(Metadata.name, Metadata.value).where(
            Metadata.element.in_(list_parents(element_id))
        )
    return Metadata.select(
        metadata.c.name,
        metadata.c.value,
        fn.ROW_NUMBER().over(partition_by=([metadata.c.name])).alias("number"),
    ).from_(metadata)


def is_present(csv_header, key):
    """
    Check if there are columns in the CSV header prefixed with either metadata, classification
    or entity (the key). If the CSV header has been filtered and there are none, then there is
    no need to make the request to retrieve this additional information.
    """
    return any(item.startswith(key) for item in csv_header)


def element_dict(
    item,
    with_classes=False,
    with_metadata=False,
    with_parent_metadata=False,
    with_entities=False,
    classes_columns=None,
    metadata_columns=None,
    entity_type_columns=None,
    classification_worker_version=None,
    entities_worker_version=None,
):
    assert (
        not with_metadata or metadata_columns is not None
    ), "Metadata columns are required to output element metadata"
    assert (
        not with_classes or classes_columns is not None
    ), "Classes columns are required to output element classifications"
    assert (
        not with_entities or entity_type_columns is not None
    ), "Entity type columns are required to output element entities"
    serialized_element = {
        "id": item.id,
        "name": item.name,
        "type": item.type,
        "image_id": None,
        "image_url": None,
        "polygon": item.polygon,
        "worker_version_id": item.worker_version_id,
        "created": datetime.fromtimestamp(item.created, tz=timezone.utc).isoformat(),
        "metadata": defaultdict(list),
        "classifications": defaultdict(list),
        "entities": defaultdict(list),
    }
    if item.image_id:
        serialized_element["image_id"] = item.image_id
        serialized_element["image_url"] = item.image.url
    # metadata
    if with_metadata and metadata_columns:
        element_md = element_metadata(item.id, load_parents=with_parent_metadata)
        for metadata in element_md:
            serialized_element["metadata"][metadata.name].append(metadata.value)
    # classifications
    if with_classes and classes_columns:
        classes = element_classes(item.id, classification_worker_version)
        for classification in classes:
            serialized_element["classifications"][classification.class_name].append(
                classification.confidence
            )
    # entities
    if with_entities and entity_type_columns:
        entities = element_entities(item.id, entities_worker_version)
        for entity in entities:
            serialized_element["entities"][entity.type_name].append(entity.name)

    return serialized_element


def fill_columns(element_dict, header, row, k, columns, prefix):
    """
    Fill rows with the appropriate metadata, classifications and entities values. This adds the
    values at the right position (in the correct columns) and fills columns with None when there
    are less values for a metadata/class/entity type on an element than the maximum number of
    values across all elements.
    """
    # Only keep the information for which there is a column in the CSV header
    columns = [column for column in columns if f"{prefix}_{column}" in header]
    column_counts = Counter(columns)
    for column, column_count in column_counts.items():
        if column not in element_dict[k]:
            row.extend(repeat(None, column_count))
        else:
            for i in range(column_count):
                row.append(
                    element_dict[k][column][i]
                    if i <= len(element_dict[k][column]) - 1
                    else None
                )
    return row


def element_row(
    element_dict,
    csv_columns,
    classes_columns=None,
    metadata_columns=None,
    entity_type_columns=None,
):
    # Ensure the base (non metadata, classification or entity) information are in the correct order
    row = [
        element_dict[column_name]
        for column_name in csv_columns
        if column_name in element_dict
    ]

    # Order in the CSV header: metadata, classifications, entities
    # Add metadata
    if metadata_columns:
        row = fill_columns(
            element_dict, csv_columns, row, "metadata", metadata_columns, "metadata"
        )
    # Add classifications
    if classes_columns:
        row = fill_columns(
            element_dict,
            csv_columns,
            row,
            "classifications",
            classes_columns,
            "classification",
        )
    # Add entities
    if entity_type_columns:
        row = fill_columns(
            element_dict, csv_columns, row, "entities", entity_type_columns, "entity"
        )

    return row


def filter_columns(input_columns, output_header):
    return list(
        chain(*(fnmatch.filter(input_columns, header) for header in output_header))
    )


def build_csv_header(
    output_header=None, md_columns=None, cl_columns=None, et_columns=None
):
    csv_header = [
        "id",
        "name",
        "type",
        "image_id",
        "image_url",
        "polygon",
        "worker_version_id",
        "created",
    ]

    # Order in the CSV header: metadata, classifications, entities
    if md_columns:
        csv_header = csv_header + [f"metadata_{col_name}" for col_name in md_columns]
    if cl_columns:
        csv_header = csv_header + [
            f"classification_{col_name}" for col_name in cl_columns
        ]
    if et_columns:
        csv_header = csv_header + [f"entity_{col_name}" for col_name in et_columns]

    if output_header:
        csv_header = filter_columns(csv_header, output_header)

    return csv_header


def run(
    database_path: Path,
    output_path: Path,
    profile_slug: Optional[str] = None,
    gitlab_secure_file: Optional[Path] = None,
    parent: Optional[UUID] = None,
    type: Optional[str] = None,
    recursive: Optional[bool] = False,
    with_classes: Optional[bool] = False,
    with_metadata: Optional[bool] = False,
    with_parent_metadata: Optional[bool] = False,
    with_entities: Optional[bool] = False,
    classification_worker_version: Optional[str] = None,
    entities_worker_version: Optional[str] = None,
    output_header: Optional[List[str]] = None,
):
    database_path = database_path.absolute()
    assert database_path.is_file(), f"Database at {database_path} not found"
    if with_parent_metadata:
        assert (
            with_metadata
        ), "The --with-parent-metadata option can only be used if --with-metadata is set."
    if entities_worker_version:
        assert (
            with_entities
        ), "The --entities-worker-version option can only be used if --with-entities is set."

    output_path = output_path.absolute()

    if recursive:
        assert (
            parent
        ), "The recursive option can only be used if a parent_element is given. If no parent_element is specified, element listing is recursive by default."

    open_database(database_path)

    elements = get_elements(parent, type, recursive)

    md_columns = None
    cl_columns = None
    et_columns = None
    if with_metadata:
        # Fetch all the metadata keys to build one CSV column by key
        if not parent and not type:
            md_columns = metadata_columns(
                None,
                load_parents=with_parent_metadata,
            )
        else:
            md_columns = metadata_columns(
                elements,
                load_parents=with_parent_metadata,
            )
    if with_classes:
        if not parent and not type:
            cl_columns = classes_columns(None)
        else:
            cl_columns = classes_columns(elements)
    if with_entities:
        if not parent and not type:
            et_columns = entity_type_columns(None, entities_worker_version)
        else:
            et_columns = entity_type_columns(elements, entities_worker_version)

    csv_header = build_csv_header(output_header, md_columns, cl_columns, et_columns)

    # Disable classes, metadata and classification options if there are no corresponding columns in the header
    if not is_present(csv_header, "entity"):
        if with_entities and output_header:
            logger.warning(
                "After filtering columns based on the --field argument, no entities will be exported."
            )
        with_entities = False
    if not is_present(csv_header, "classifications"):
        if with_classes and output_header:
            logger.warning(
                "After filtering columns based on the --field argument, no classifications will be exported."
            )
        with_classes = False
    if not is_present(csv_header, "metadata"):
        if with_metadata and output_header:
            logger.warning(
                "After filtering columns based on the --field argument, no metadata will be exported."
            )
        with_metadata = False
        with_parent_metadata = False

    elements = elements.select(Element, Image).join(
        Image, JOIN.LEFT_OUTER, on=[Image.id == Element.image_id]
    )

    with open(output_path, "w", encoding="UTF8", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(csv_header)

        for element in elements:
            item_dict = element_dict(
                element,
                with_classes,
                with_metadata,
                with_parent_metadata,
                with_entities,
                classes_columns=cl_columns,
                metadata_columns=md_columns,
                entity_type_columns=et_columns,
                classification_worker_version=classification_worker_version,
                entities_worker_version=entities_worker_version,
            )

            item_row = element_row(
                item_dict, csv_header, cl_columns, md_columns, et_columns
            )
            writer.writerow(item_row)

        logger.info(f"Exported elements successfully written to {output_path}.")


def add_csv_parser(subcommands):
    csv_parser = subcommands.add_parser(
        "csv",
        description="Read data from an exported database and generate a CSV file.",
        help="Generates a CSV file from an Arkindex export.",
    )
    csv_parser.add_argument(
        "--parent",
        type=UUID,
        help="Limit the export to the children of a given element.",
    )
    csv_parser.add_argument(
        "--type", type=str, help="Limit the export to elements of a given type."
    )
    csv_parser.add_argument(
        "--recursive", action="store_true", help="Get elements recursively."
    )
    csv_parser.add_argument(
        "--with-classes", action="store_true", help="Retrieve element classes."
    )
    csv_parser.add_argument(
        "--classification-worker-version",
        type=uuid_or_manual,
        help="The worker version that created the classifications that will be in the csv",
    )
    csv_parser.add_argument(
        "--with-metadata", action="store_true", help="Retrieve element metadata."
    )
    csv_parser.add_argument(
        "--with-parent-metadata",
        action="store_true",
        help="Recursively retrieve metadata of element ancestors.",
    )
    csv_parser.add_argument(
        "--with-entities", action="store_true", help="Retrieve element entities."
    )
    csv_parser.add_argument(
        "--entities-worker-version",
        type=uuid_or_manual,
        help="Only retrieve the entities created by a specific worker version.",
    )
    csv_parser.add_argument(
        "-o",
        "--output",
        default=Path.cwd() / "elements.csv",
        type=Path,
        help="Path to a CSV file where results will be outputted. Defaults to '<current_directory>/elements.csv'.",
        dest="output_path",
    )
    csv_parser.add_argument(
        "-f",
        "--field",
        nargs="+",
        type=str,
        help="Limit the CSV columns to the selected fields",
        dest="output_header",
    )
    csv_parser.set_defaults(func=run)
