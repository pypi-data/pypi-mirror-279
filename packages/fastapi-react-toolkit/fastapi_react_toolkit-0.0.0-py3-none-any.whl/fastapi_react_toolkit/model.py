import re

from sqlalchemy import Table as SA_Table
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

camelcase_re = re.compile(r"([A-Z]+)(?=[a-z0-9])")


def camel_to_snake_case(name):
    def _join(match):
        word = match.group()

        if len(word) > 1:
            return ("_%s_%s" % (word[:-1], word[-1])).lower()

        return "_" + word.lower()

    return camelcase_re.sub(_join, name).lstrip("_")


class Model(DeclarativeBase):
    """
    Use this class has the base for your models,
    it will define your table names automatically
    MyModel will be called my_model on the database.

    ::

        from sqlalchemy import Integer, String
        from fastapi-react-toolkit import Model

        class MyModel(Model):
            id = Column(Integer, primary_key=True)
            name = Column(String(50), unique = True, nullable=False)

    """

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Returns the table name for the given class.

        The table name is derived from the class name by converting
        any uppercase letters to lowercase and inserting an underscore
        before each uppercase letter.

        Returns:
            str: The table name.
        """
        return camel_to_snake_case(cls.__name__)

    __table_args__ = {"extend_existing": True}

    def update(self, data: dict[str, any]):
        """
        Updates the model instance with the given data.

        Args:
            data (dict): The data to update the model instance with.

        Returns:
            None
        """
        for key, value in data.items():
            setattr(self, key, value)

    @property
    def name_(self):
        """
        Returns the string representation of the object.
        """
        return str(self)


metadata = Model.metadata


class Table(SA_Table):
    """
    Represents a table in the database.
    """

    pass


"""
    This is for retro compatibility
"""
Base = Model
