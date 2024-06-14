# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from typing import List, Optional

from apistar.exceptions import ErrorResponse

from arkindex_cli.auth import Profiles
from arkindex_cli.commands.utils import parse_config
from arkindex_cli.git import LocalGitRepository

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def add_publish_parser(subcommands) -> None:
    recover_parser = subcommands.add_parser(
        "publish",
        description="Publish an available worker version, creating its Git stack (repository, revision, worker) if required",
        help="Publish an available worker version, creating its Git stack (repository, revision, worker) if required",
    )
    recover_parser.add_argument(
        "docker_image_tag",
        help="Tag of the Docker image to be published on the new worker version",
    )
    recover_parser.add_argument(
        "--repository-url",
        help=(
            "URL of the Git project repository containing the worker. "
            "If unset, the repository is automatically detected from the current directory."
        ),
    )
    recover_parser.add_argument(
        "--revision-hash",
        help="Hash of the Git revision on which the worker version is published.",
    )
    recover_parser.add_argument(
        "--revision-message",
        help="Message of the Git revision on which the worker version is published.",
    )
    recover_parser.add_argument(
        "--revision-author",
        help="Name of the author of the Git revision on which the worker version is published.",
    )
    recover_parser.add_argument(
        "--revision-branch",
        help="Name of a branch to assign to the Git revision.",
    )
    recover_parser.add_argument(
        "--revision-tags",
        nargs="+",
        help="Tags to assign to the Git revision.",
    )
    recover_parser.set_defaults(func=run)


def run(
    *,
    docker_image_tag: str,
    repository_url: Optional[str],
    revision_hash: Optional[str],
    revision_message: Optional[str],
    revision_author: Optional[str],
    revision_branch: Optional[str],
    revision_tags: List[str],
    profile_slug: Optional[str] = None,
    gitlab_secure_file: Optional[Path] = None,
) -> int:

    workers_data = parse_config(Path.cwd())["workers"]
    if not workers_data:
        logger.error("No workers found. Skipping...")
        return

    local_repo = LocalGitRepository()

    if repository_url is None:
        logger.info("Identifying repository from the current directory")
        repository_url = local_repo.url
    if revision_hash is None:
        revision_hash = local_repo.hash
    if revision_message is None:
        revision_message = local_repo.message
    if revision_author is None:
        revision_author = local_repo.author
    if revision_branch is None:
        revision_branch = local_repo.branch
    if revision_tags is None:
        revision_tags = local_repo.tags

    logger.info("Building a new worker version:")
    logger.info(f" * Repository: {repository_url}")
    logger.info(f" * Revision: {revision_hash}")
    logger.info(f" * Message: {revision_message}")
    logger.info(f" * Author: {revision_author}")
    logger.info(f" * Branch: {revision_branch}")
    logger.info(f" * Tags: {revision_tags}")

    references = []

    # We might not always have a Git branch, as CI jobs running on tags only have the tag set and not the branch
    if revision_branch:
        references.append({"type": "branch", "name": revision_branch})

    if revision_tags:
        references.extend([{"type": "tag", "name": val} for val in revision_tags])

    logger.info("Pushing new version to Arkindex")

    profiles = Profiles(gitlab_secure_file)
    profile = profiles.get_or_exit(profile_slug)
    api_client = profiles.get_api_client(profile)

    failures = 0
    for worker in workers_data:
        payload = {}

        description_path = worker.pop("description")
        if description_path:
            assert (
                description_path.exists()
            ), f"Worker description was not found @ {description_path}"
            payload["worker_description"] = description_path.read_text()

        payload["docker_image_iid"] = docker_image_tag
        payload["repository_url"] = repository_url
        payload["revision_hash"] = revision_hash
        payload["revision_message"] = revision_message
        payload["revision_author"] = revision_author
        payload["revision_references"] = references
        payload["worker_slug"] = worker["slug"]
        payload["worker_name"] = worker["name"]
        payload["worker_type"] = worker["type"]
        payload["gpu_usage"] = worker.pop("gpu_usage")
        payload["model_usage"] = worker.pop("model_usage")
        payload["configuration"] = worker

        try:
            worker_version = api_client.request(
                "CreateDockerWorkerVersion",
                body=payload,
            )
        except ErrorResponse as e:
            logger.error(f"An error occurred: [{e.status_code}] {e.content}")
            failures += 1
        else:
            logger.info(f"Successfully pushed version {worker_version['id']}")

    if failures > 0:
        return 1
    return 0
