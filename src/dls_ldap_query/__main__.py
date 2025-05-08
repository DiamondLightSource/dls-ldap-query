"""Interface for ``python -m dls_ldap_query``."""

from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer

from . import __version__

__all__ = ["main"]


# LDAP attributes to get. Full list that could be added herer is found at:
# https://www.ibm.com/docs/en/cip?topic=api-user-identity-attributes
@dataclass
class Person:
    cn: str  # The common name (fedID)
    displayName: str  # e.g. Knap, Giles (DLSLtd,RAL,LSCI)
    name: str  # The name of the person
    mail: str  # The email address of the person
    givenName: str  # The first name of the person
    sn: str  # The surname of the person


# a list of the above fields
ATTRIBUTES = Person.__annotations__.keys()


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
    ],
    emails: Annotated[
        bool | None,
        typer.Option(
            "--emails",
            "-e",
            help="treat the search sting as a list of emails copies from Outlook",
        ),
    ] = False,
    group: Annotated[
        str | None, typer.Option(help="A linux group name to extract users ids from")
    ] = None,
    version: Annotated[
        bool | None,
        typer.Option(
            "--version",
            callback=version_callback,
            help="print the version number and exit",
        ),
    ] = None,
):
    pass


if __name__ == "__main__":
    typer.run(main)
