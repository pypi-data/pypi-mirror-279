from datetime import date, datetime
from enum import Enum
from typing import Any, List, Optional, Type

from pydantic import BaseModel, ConfigDict, Field, create_model

from ..api import SQLAInterface
from ..schemas import IgnoredData
from .db import *
from .filters import *
from .model import *


class GenericInterface(SQLAInterface):
    """
    Represents an interface for a Generic model (Based on pydantic).
    """

    obj: GenericModel
    query: GenericQueryManager = None
    filter_converter: GenericFilterConverter = GenericFilterConverter()
    session: GenericSession | None = None

    list_columns: dict[str, Any]
    list_properties: dict[str, Any]

    _filters: dict[str, list[GenericBaseFilter]] = None

    def __init__(self, obj: GenericModel, session: GenericSession | None = None):
        self.session = session
        super().__init__(obj)

    def generate_schema(
        self, columns: List[str] = [], with_name_=True, optional=False
    ) -> BaseModel:
        """
        Generate a Pydantic schema based on the object's properties.

        Args:
            columns (List[str], optional): A list of columns to include in the schema. Returns an empty schema if not specified. Defaults to [].
            with_name_ (bool, optional): Whether to include the name_ column. Defaults to True.
            optional (bool, optional): Whether the columns should be optional. Required for PUT or PATCH requests. Defaults to False.

        Returns:
            BaseModel: The Pydantic schema for the object.
        """
        schema_dict = {
            "__model_name": self.obj.__name__,
            "__config__": ConfigDict(from_attributes=True),
        }

        if with_name_:
            schema_dict["name_"] = (str, Field())

        if not columns:
            return create_model(**schema_dict)

        prop_dict = self.list_properties
        for key, column in prop_dict.items():
            # Ignore it if it is a fk or not in the list of columns
            if self.is_fk(key) or key not in columns:
                continue

            params = {}
            type = self.get_type(key)
            if self.is_pk(key):
                self.id_schema = type
            if self.is_nullable(key) or optional:
                params["default"] = IgnoredData() if optional else None
                type = type | IgnoredData if optional else type | None
            schema_dict[key] = (type, Field(**params))
        return create_model(**schema_dict)

    def get_type(self, col: str) -> Type:
        """
        Get the Python type corresponding to the specified column name.

        Args:
            col (str): The name of the column.

        Returns:
            Type: The Python type corresponding to the column.

        """
        return self.obj.properties[col].col_type

    def get_type_name(self, col: str) -> str:
        if self.is_string(col):
            return "String"
        if self.is_integer(col):
            return "Integer"
        if self.is_boolean(col):
            return "Boolean"
        if self.is_date(col):
            return "DateTime"
        return "Raw"

    def _init_properties(self):
        """
        Initialize the properties of the object.

        This method initializes the properties of the object by creating a dictionary of the object's columns and their corresponding types.

        Returns:
            None
        """
        self.query = GenericQueryManager(self, self.session)
        self.list_columns = self.obj.properties
        self.list_properties = self.obj.properties

    """
    ------------------------------
     FUNCTIONS FOR RELATED MODELS
    ------------------------------
    """

    def get_related_model(self, col_name: str) -> GenericModel:
        if self.is_relation(col_name):
            return self.list_properties[col_name].__class__

        raise ValueError(f"{col_name} is not a relation")

    """
    -------------
     GET METHODS
    -------------
    """

    def get_search_columns_list(self) -> List[str]:
        return [x for x in self.obj.columns if not self.is_pk(x)]

    def get_file_column_list(self) -> List[str]:
        return []

    def get_image_column_list(self) -> List[str]:
        return []

    """
    -----------------------------------------
         FUNCTIONS for Testing TYPES
    -----------------------------------------
    """

    def is_image(self, col_name: str) -> bool:
        return False

    def is_file(self, col_name: str) -> bool:
        return False

    def is_string(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == str

    def is_text(self, col_name: str) -> bool:
        return self.is_string(col_name)

    def is_binary(self, col_name: str) -> bool:
        return False

    def is_integer(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == int

    def is_numeric(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_float(self, col_name: str) -> bool:
        return self.is_integer(col_name)

    def is_boolean(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == bool

    def is_date(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == date or self.is_datetime(
            col_name
        )

    def is_datetime(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == datetime

    def is_enum(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == Enum

    def is_json(self, col_name: str) -> bool:
        return self.obj.properties[col_name].col_type == dict

    def is_relation(self, col_name: str) -> bool:
        return self.is_relation_one_to_one(col_name) or self.is_relation_one_to_many(
            col_name
        )

    def is_relation_many_to_one(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many(self, col_name: str) -> bool:
        # TODO: AS OF NOW, cant detect
        return False

    def is_relation_many_to_many_special(self, col_name: str) -> bool:
        return False

    def is_relation_one_to_one(self, col_name: str) -> bool:
        return isinstance(self.list_properties[col_name], GenericModel)

    def is_relation_one_to_many(self, col_name: str) -> bool:
        if not isinstance(self.list_properties[col_name], list):
            return False
        for prop in self.list_properties[col_name]:
            if not isinstance(prop, GenericModel):
                return False

        return True

    def is_pk_composite(self) -> bool:
        return False

    def is_fk(self, col_name: str) -> bool:
        return False

    def get_max_length(self, col_name: str) -> int:
        raise NotImplementedError
