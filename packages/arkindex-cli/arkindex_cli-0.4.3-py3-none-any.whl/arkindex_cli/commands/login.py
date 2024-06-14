# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Optional

from apistar.exceptions import ErrorResponse
from rich import print

from arkindex_cli.argtypes import URLArgument
from arkindex_cli.auth import Profiles
from arkindex_cli.utils import ask
from teklia_toolbox.requests import get_arkindex_client


def add_login_parser(subcommands) -> None:
    login_parser = subcommands.add_parser(
        "login",
        description="Login to an Arkindex instance.",
        help="Login to an Arkindex instance.",
    )
    login_parser.add_argument(
        "--host",
        type=URLArgument(allow_query=False, allow_fragment=False),
        help="URL of the Arkindex instance to login to.",
    )
    login_parser.add_argument("--email", help="Email to login with.")
    login_parser.set_defaults(func=run)


def run(
    host: Optional[str] = None,
    profile_slug: Optional[str] = None,
    gitlab_secure_file: Optional[Path] = None,
    email: Optional[str] = None,
) -> int:
    while not host:
        parser = URLArgument(allow_query=False, allow_fragment=False)
        try:
            host = parser(ask("Arkindex instance URL", default="demo.arkindex.org"))
        except ValueError as e:
            print(f"[bright_red]{e}")

    print("Loading API client…", end="")
    cli = get_arkindex_client(base_url=host)
    print(" Done!")

    token = None
    while not token:
        while not email:
            email = ask("E-mail address")
        password = None
        while not password:
            password = ask("Password", hidden=True)

        try:
            token = cli.login(email, password)["auth_token"]
            print("[bright_green bold]Authentication successful")
        except ErrorResponse as e:
            print(f"[bright_red bold]Authentication failure: {e.content}")
            email = None
            password = None

    while not profile_slug:
        profile_slug = ask("Slug to save profile as", default="default")

    profiles = Profiles()
    profiles.add_profile(profile_slug, host, token)

    make_default = None
    while make_default not in ("yes", "no"):
        make_default = ask("Set this profile as the default?", default="yes").lower()

    if make_default == "yes":
        profiles.set_default_profile(profile_slug)

    profiles.save()
