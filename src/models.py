"""Models package

Defines SQLAlchemy model : Short
"""
from sqlalchemy import Column, String

from .database import Base


class Short(Base):
    # corresponding table name in database
    __tablename__ = "short"

    # key is the primary key
    key = Column(String, primary_key=True, index=True)
    # url is unique, indexed and not nullable
    url = Column(String, unique=True, index=True, nullable=False)

    # redefine the objects equality comparison operator
    def __eq__(self, other: object) -> bool:
        """Equality comparison operator

        Replace the standard object equality comparison operator by a shallow version.
        Check only objects type and attributes (key, url) values.

        Args:
            other (object): other object to compare to.

        Returns:
            bool: True if other object has the same type and attribute values as the current one.
        """

        if isinstance(other, self.__class__):
            return self.key == other.key and self.url == other.url
        return False
