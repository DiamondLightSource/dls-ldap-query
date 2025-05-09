"""Interface for ``python -m dls_ldap_query``."""

import grp
import re
from typing import Annotated

import typer

from . import __version__
from .formatter import Formats, format_results
from .ldap import LDAPServer

__all__ = ["main"]

RE_EMAIL = re.compile(r"\<([^\>]*)\>")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


def main():
    """
    Main entry point for this module - dls_ldap_query.
    """
    typer.run(query)


def query(
    search_string: Annotated[
        str, typer.Argument(help="comma separaed list of search terms")
    ] = "",
    email: Annotated[
        bool,
        typer.Option(
            "-e",
            help="treat the search sting as a list of emails copied from Outlook",
        ),
    ] = False,
    group: Annotated[
        str | None,
        typer.Option("-g", help="A linux group name to extract users ids from"),
    ] = None,
    attribute: Annotated[
        str,
        typer.Option(
            "-a",
            help="The LDAP attribute to search for.",
        ),
    ] = "cn",
    server: Annotated[
        str,
        typer.Option(
            "-s",
            help="The LDAP server to connect to.",
        ),
    ] = LDAPServer.default_server_url,
    search_base: Annotated[
        str,
        typer.Option(
            "-b",
            help="The LDAP search base to use.",
        ),
    ] = LDAPServer.default_search_base,
    version: Annotated[
        bool | None,
        typer.Option(
            callback=version_callback,
            help="print the version number and exit",
        ),
    ] = None,
):
    if group is not None:
        # search for all users in a linux group
        group_obj = grp.getgrnam(group)
        attribute = "cn"
        search_array = group_obj.gr_mem
    elif email:
        # extract the emails from a list pasted from outlook
        search_array = RE_EMAIL.findall(search_string)
    else:
        # treat search_string as a comma separated list
        search_array = search_string.split(",")

    ldap_server = LDAPServer(server, search_base)

    entries = ldap_server.search(search_array, attribute)
    format_results(entries, Formats.ansible)


if __name__ == "__main__":
    typer.run(main)
