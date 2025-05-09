from enum import Enum

from .ldap import Person


class Formats(Enum):
    """predifined output formats"""

    none = 0
    email = 1
    fedid = 2
    ansible = 3


def format_results(
    results: list[Person], format: Formats = Formats.none, format_str: str = ""
) -> None:
    """
    Format the results of the LDAP query.
    """

    for user in results:
        # using match allows us to use fstring features not available to str.format()
        match format:
            case Formats.ansible:
                output = (
                    f"- {user.cn:12} # {user.sn + ', ' + user.givenName:28}"
                    f"  {user.mail}"
                )
            case Formats.email:
                output = "{user.mail}"
            case Formats.fedid:
                output = "{user.cn}"
            case Formats.none:
                output = format_str.format(user)

        print(output)
