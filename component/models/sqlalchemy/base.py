"""
SQLAlchemy Base class
"""

from typing import Any, Dict

from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:  # pylint: disable=too-few-public-methods
    """SQLAlchemy base class"""

    description = ""

    def as_dict(self, serializable=False) -> Dict[str, Any]:
        """
        Return non-private members of Model as a dictionary

        :return: Dictionary of item elements, keyed by columns
        """
        if serializable:
            return {
                key: str(value) for key, value in vars(self).items() if key[0] != "_"
            }
        return {key: value for key, value in vars(self).items() if key[0] != "_"}
