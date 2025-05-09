from enum import StrEnum

from .ldap import Person


class Formats(StrEnum):
    """predifined output formats"""

    none = "none"
    email = "email"
    fedid = "fedid"
    ansible = "ansible"


def format_results(
    results: list[Person], format: Formats = Formats.none, format_str: str = ""
) -> None:
    """
    Format the results of the LDAP query.
    """

    # supplying a format string overrides predefined formats
    if format_str:
        format = Formats.none

    for user in results:
        # using match allows us to use fstring features not available to str.format()
        match format:
            case Formats.ansible:
                output = (
                    f"- {user.cn:12} # {user.sn + ', ' + user.givenName:28}"
                    f"  {user.mail}"
                )
            case Formats.email:
                output = f"{user.mail}"
            case Formats.fedid:
                output = f"{user.cn}"
            case Formats.none:
                try:
                    output = format_str.format(user=user)
                except KeyError:
                    print("format_str should contain fields like: '{user.cn}'")
                    exit(1)

        # skip blank format results
        if output != "":
            print(output)
