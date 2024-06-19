import re
from enum import Enum
from typing import Any, Dict, List, Literal, Tuple

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, create_model
from sqlalchemy.ext.asyncio import AsyncSession

from ..decorators import permission_name
from ..dependencies import current_active_user, current_permissions, get_db, has_access
from ..filters import BaseFilter
from ..models import Model
from ..schemas import (
    BaseResponseMany,
    BaseResponseSingle,
    ColumnInfo,
    ColumnRelationInfo,
    GeneralResponse,
    IgnoredData,
    InfoResponse,
    QueryBody,
    QuerySchema,
    RelInfo,
)
from ..utils import dump_schema
from .interface import SQLAInterface
from .utils import *


class ModelRestApi:
    """
    Represents a REST API for a SQLAlchemy model.

    Raises:
        ValueError: If the resource name is not provided.
        HTTPException: If an item is not found. The status code will be 404. Used in the get, update, and delete endpoints.
        HTTPException: If some items are not found. The status code will be 400. Used in the create endpoint.
        HTTPException: If an item is not found for a one-to-one or many-to-one relation. The status code will be 400. Used in the create endpoint.

    Returns:
        _type_: _description_
    """

    base_route = "/api/v1"
    """
    The base route for the API.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    resource_name: str | None = None
    """
    The name of the resource. If not given, defaults to the model name in lowercase.
    """
    router: APIRouter | None = None
    """
    The FastAPI router object.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    datamodel: SQLAInterface = None
    """
    The SQLAlchemy interface object.
    """
    max_page_size: int = 25
    """
    The maximum page size for the related fields in add_columns, edit_columns, and search_columns properties.
    """
    permissions: List[str] = []
    """
    The list of permissions for the API.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    exclude_routes: List[str] = None
    """
    The list of routes to exclude. available routes: `info`, `download`, `bulk`, `list`, `get`, `post`, `put`, `delete`.
    """
    base_order: Tuple[str, Literal["asc", "desc"]] | None = None
    """
    The default order for the list endpoint. Set this to set the default order for the list endpoint.

    Example:
    ```python
    base_order = ("name", "asc")
    ```
    """
    base_filters: List[Tuple[str, BaseFilter, Any]] = None
    """
    The default filters for the list endpoint. Set this to set the default filters for the list endpoint.

    Example:
    ```python
    base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """
    show_base_filters: List[Tuple[str, BaseFilter, Any]] = None
    """
    The default filters for the show endpoint. Set this to set the default filters for the show endpoint.

    Example:
    ```python
    show_base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """
    download_base_filters: List[Tuple[str, BaseFilter, Any]] = None
    """
    The default filters for the download endpoint. Set this to set the default filters for the download endpoint.

    Example:
    ```python
    download_base_filters = [
        ["status", FilterEqual, "active"],
    ]
    ```
    """

    info_return_schema: InfoResponse = None
    """
    The response schema for the info endpoint. 

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    _default_info_schema: bool = False
    """
    A flag to indicate if the default info schema is used.

    DO NOT MODIFY.
    """

    query_schema: QuerySchema = None
    """
    The query schema for the list endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    download_body_schema: QueryBody = None
    """
    The body schema for the download endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    list_title: str = None
    """
    The title for the list endpoint. If not provided, Defaults to "List {ModelName}".
    """
    list_columns: List[str] = None
    """
    The list of columns to display in the list endpoint. If not provided, all columns will be displayed.
    """
    list_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the list endpoint.
    """
    list_join_columns: List[str] = None
    """
    The list of columns to join in the list endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    list_return_schema: BaseResponseMany = None
    """
    The response schema for the list endpoint.
    
    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    description_columns: Dict[str, str] = None
    """
    The description for each column in the add columns, edit columns, and search columns properties.

    Example:
    ```python
    description_columns = {
        "name": "Name of the item",
        "description": "Description of the item",
    }
    ```
    """
    label_columns: Dict[str, str] = None
    """
    The label for each column in the list columns and show columns properties.

    Example:
    ```python
    label_columns = {
        "name": "Name",
        "description": "Description",
    }
    ```
    """
    order_columns: List[str] = None
    """
    The list of columns that can be ordered in the list endpoint.
    """
    order_rel_fields: Dict[str, Tuple[str, Literal["asc", "desc"]]] = None
    """
    Order the related fields in the add_columns, edit_columns, and search_columns properties.

    Example:
    ```python
    order_rel_fields = {
        "user": ("username", "asc"),
    }
    ```
    """

    show_title: str = None
    """
    The title for the show endpoint. If not provided, Defaults to "Show {ModelName}".
    """
    show_columns: List[str] = None
    """
    The list of columns to display in the show endpoint. If not provided, all columns will be displayed.
    """
    show_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the show endpoint.
    """
    show_join_columns: List[str] = None
    """
    The list of columns to join in the show endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    show_return_schema: BaseResponseSingle = None
    """
    The response schema for the show endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """

    add_title: str = None
    """
    The title for the add endpoint. If not provided, Defaults to "Add {ModelName}".
    """
    add_columns: List[str] = None
    """
    The list of columns to display in the add endpoint. If not provided, all columns will be displayed.
    """
    add_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the add endpoint.
    """
    add_schema: BaseModel = None
    """
    The schema for the add endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    add_return_schema: BaseResponseSingle = None
    """
    The response schema for the add endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    add_query_rel_fields: Dict[str, List[Tuple[str, BaseFilter, Any]]] = None
    """
    The query fields for the related fields in the add_columns property.

    Example:
    ```python
    add_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """

    edit_title: str = None
    """
    The title for the edit endpoint. If not provided, Defaults to "Edit {ModelName}".
    """
    edit_columns: List[str] = None
    """
    The list of columns to display in the edit endpoint. If not provided, all columns will be displayed.
    """
    edit_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the edit endpoint.
    """
    edit_schema: BaseModel = None
    """
    The schema for the edit endpoint.

    DO NOT MODIFY UNLESS YOU KNOW WHAT YOU ARE DOING.
    """
    edit_query_rel_fields: Dict[str, List[Tuple[str, BaseFilter, Any]]] = None
    """
    The query fields for the related fields in the edit_columns property.

    Example:
    ```python
    edit_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """

    search_columns: List[str] = None
    """
    The list of columns that are allowed to be filtered in the list endpoint. If not provided, all columns will be allowed.
    """
    search_exclude_columns: List[str] = None
    """
    The list of columns to exclude from the search columns.
    """
    search_query_rel_fields: Dict[str, List[Tuple[str, BaseFilter, Any]]] = None
    """
    The query fields for the related fields in the search_columns property.

    Example:
    ```python
    search_query_rel_fields = {
        "user": [
            ["username", FilterEqual, "admin"],
        ],
    }
    ```
    """
    filter_options: Dict[str, Any] = None
    """
    Additional filter options from the user for the info endpoint.

    Example:
    ```python
    filter_options = {
        "odd_numbers": [1, 3, 5, 7, 9],
    }
    ```
    """

    toolkit = None
    """
    The FastapiReactToolkit object. Automatically set when the API is added to the toolkit.
    """

    _cache: Dict[str, Any] = None
    """
    The cache for the API.
    
    DO NOT MODIFY.
    """

    def __init__(self) -> None:
        # Create resource name if not provided
        if not self.resource_name and self.datamodel:
            self.resource_name = self.datamodel.obj.__name__.lower()

        if not self.resource_name:
            raise ValueError("Resource name must be provided.")

        self._init_router()
        self._init_titles()
        self._init_properties()
        self._init_schema()
        self._init_routes()
        self.add_routes()

    @staticmethod
    def merge_schema(
        schema: BaseModel, fields: Dict[str, tuple[type, Field]], only_update=False
    ) -> BaseModel:
        """
        Replace or add fields to the given schema.

        Args:
            schema (BaseModel): The schema to be updated.
            fields (Dict[str, tuple[type, Field]]): The fields to be added or updated.
            only_update (bool): If True, only update the fields with the same name. Otherwise, add new fields.

        Returns:
            BaseModel: The updated schema.
        """
        new_fields = dict()
        if only_update:
            for key, value in schema.model_fields.items():
                if key in fields:
                    val = fields[key]
                    if isinstance(val, tuple):
                        new_fields[key] = val
                    else:
                        new_fields[key] = (value.annotation, val)
        else:
            new_fields = fields

        return create_model(
            schema.__name__,
            **new_fields,
            __base__=schema,
        )

    def add_routes(self) -> None:
        """
        Add routes to the API.

        This method is responsible for adding routes to the FastAPI application.
        It should be implemented by subclasses to define the specific routes for the API.

        Usage:
        ```python
        def add_routes(self):
            @self.router.get("/custom")
            async def custom_route():
                return {"message": "Custom route"}
        ```

        Returns:
            None
        """
        pass

    """
    -----------------------------------------
         INIT FUNCTIONS
    -----------------------------------------
    """

    def _init_router(self) -> None:
        """
        Initializes the router for the API.

        This method creates a new APIRouter object and sets the prefix and tags for the router.

        Returns:
            None
        """
        self.router = APIRouter(
            prefix=f"{self.base_route}/{self.resource_name}",
            tags=[self.__class__.__name__],
        )

    def _init_titles(self) -> None:
        """
        Init Titles if not defined
        """
        if not self.datamodel:
            return

        class_name = self.datamodel.obj.__name__
        if not self.list_title:
            self.list_title = "List " + self._prettify_name(class_name)
        if not self.add_title:
            self.add_title = "Add " + self._prettify_name(class_name)
        if not self.edit_title:
            self.edit_title = "Edit " + self._prettify_name(class_name)
        if not self.show_title:
            self.show_title = "Show " + self._prettify_name(class_name)
        self.title = self.list_title

    def _init_properties(self) -> None:
        if not self.datamodel:
            return

        list_cols = self.datamodel.get_user_columns_list()

        self.exclude_routes = self.exclude_routes or []
        self.exclude_routes = [x.lower() for x in self.exclude_routes]
        self.base_filters = self.base_filters or []
        self.show_base_filters = self.show_base_filters or []
        self.download_base_filters = self.download_base_filters or []

        self.list_exclude_columns = self.list_exclude_columns or []
        self.show_exclude_columns = self.show_exclude_columns or []
        self.add_exclude_columns = self.add_exclude_columns or []
        self.edit_exclude_columns = self.edit_exclude_columns or []
        self.search_exclude_columns = self.search_exclude_columns or []
        self.description_columns = self.description_columns or {}
        self.label_columns = self.label_columns or {}
        self.filter_options = self.filter_options or {}

        self.list_columns = self.list_columns or [
            x for x in list_cols if x not in self.list_exclude_columns
        ]
        self.show_columns = self.show_columns or [
            x for x in list_cols if x not in self.show_exclude_columns
        ]
        self.add_columns = self.add_columns or [
            x for x in list_cols if x not in self.add_exclude_columns
        ]
        self.edit_columns = self.edit_columns or [
            x for x in list_cols if x not in self.edit_exclude_columns
        ]
        self.search_columns = self.search_columns or [
            x
            for x in self.datamodel.get_search_columns_list()
            if x not in self.search_exclude_columns
        ]

        self.list_join_columns = self.list_join_columns or [
            x for x in self.list_columns if self.datamodel.is_relation(x)
        ]
        self.show_join_columns = self.show_join_columns or [
            x for x in self.show_columns if self.datamodel.is_relation(x)
        ]

        # Add columns with @property decorator
        property_cols = self.datamodel.get_property_column_list()
        self.list_columns += [
            x
            for x in property_cols
            if x not in self.list_columns and x not in self.list_exclude_columns
        ]
        self.show_columns += [
            x
            for x in property_cols
            if x not in self.show_columns and x not in self.show_exclude_columns
        ]

        self._gen_labels_columns(self.list_columns)
        self._gen_labels_columns(self.show_columns)

        self.order_columns = (
            self.order_columns
            or self.datamodel.get_order_columns_list(list_columns=self.list_columns)
        )

        self.order_rel_fields = self.order_rel_fields or dict()
        self.add_query_rel_fields = self.add_query_rel_fields or dict()
        self.edit_query_rel_fields = self.edit_query_rel_fields or dict()
        self.search_query_rel_fields = self.search_query_rel_fields or dict()

    def _init_schema(self) -> None:
        """
        Initializes the schema for the API.

        This method creates schema models for info, list, get, add, and edit endpoints based on the datamodel's table columns.

        Returns:
            None
        """
        if not self.datamodel:
            return

        if not self.info_return_schema:
            self.info_return_schema = InfoResponse(
                add_title=self.add_title,
                edit_title=self.edit_title,
                filter_options=self.filter_options,
            )
            self._default_info_schema = True

        order_column_enum = Enum(
            self.datamodel.obj.__name__,
            {col: col for col in self.order_columns},
            type=str,
        )

        self.query_schema = self.query_schema or self.merge_schema(
            QuerySchema,
            {
                "order_column": (order_column_enum | None, Field(default=None)),
            },
            True,
        )

        self.download_body_schema = self.download_body_schema or self.merge_schema(
            QueryBody,
            {
                "order_column": (order_column_enum | None, Field(default=None)),
            },
            True,
        )

        list_obj_schema = self.datamodel.generate_schema(self.list_columns, False)
        show_obj_schema = self.datamodel.generate_schema(self.show_columns, False)

        # Combine props with @property functions
        property_column_dict = dict()
        for col in self.list_columns:
            if self.datamodel.is_property(col):
                property_column_dict[col] = (Any, Field(default=None))

        list_obj_schema = (
            self.merge_schema(
                list_obj_schema,
                property_column_dict,
            )
            if property_column_dict
            else list_obj_schema
        )
        show_obj_schema = (
            self.merge_schema(
                show_obj_schema,
                property_column_dict,
            )
            if property_column_dict
            else show_obj_schema
        )

        self.list_return_schema = self.list_return_schema or self.merge_schema(
            BaseResponseMany,
            {
                **vars(self),
                "result": (List[list_obj_schema], ...),
            },
            True,
        )
        self.show_return_schema = self.show_return_schema or self.merge_schema(
            BaseResponseSingle,
            {
                **vars(self),
                "result": (show_obj_schema, ...),
            },
            True,
        )
        self.add_return_schema = self.add_return_schema or self.merge_schema(
            BaseResponseSingle,
            {
                **vars(self),
                "result": (show_obj_schema, ...),
            },
            True,
        )

        self.add_schema = self.add_schema or self._create_request_schema(
            self.add_columns
        )
        self.edit_schema = self.edit_schema or self._create_request_schema(
            self.edit_columns, True
        )

    def _init_routes(self) -> None:
        """
        Initializes the routes for the API endpoints.

        This method is responsible for initializing the routes for various API endpoints,
        such as the info, list, get, create, update, and delete endpoints.

        Returns:
            None
        """
        if not self.datamodel:
            return

        if not "info" in self.exclude_routes:
            self._init_info_endpoint()
        if not "download" in self.exclude_routes:
            self._init_download_endpoint()
        if not "bulk" in self.exclude_routes:
            self._init_bulk_endpoint()
        if not "list" in self.exclude_routes:
            self._init_list_endpoint()
        if not "get" in self.exclude_routes:
            self._init_get_endpoint()
        if not "post" in self.exclude_routes:
            self._init_create_endpoint()
        if not "put" in self.exclude_routes:
            self._init_update_endpoint()
        if not "delete" in self.exclude_routes:
            self._init_delete_endpoint()

    def _init_info_endpoint(self):
        """
        Initializes the info endpoint for the API.

        This method sets up the HTTP route for retrieving information about the API.

        Returns:
            None
        """

        @permission_name(self, "info")
        @self.router.get(
            "/_info",
            response_model=self.info_return_schema,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "info")),
            ],
        )
        async def get_info(
            *,
            permissions: List[str] = Depends(current_permissions(self)),
            db: AsyncSession = Depends(get_db),
        ):
            if self._default_info_schema:
                await self._update_info_schema(permissions, db)
            return self.info_return_schema

    def _init_download_endpoint(self):
        """
        Initializes the download endpoint for the API.

        This method sets up the HTTP route for downloading a file.

        Returns:
            None
        """

        @permission_name(self, "download")
        @self.router.post(
            "/download",
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "download")),
            ],
        )
        async def download(
            body: self.download_body_schema,
            db: AsyncSession = Depends(get_db),
        ):
            for filter in body.filters:
                if not filter.col in self.search_columns:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid filter: {filter.col}"
                    )

            await self.datamodel.query.add_options(
                db,
                join_columns=self.list_join_columns,
                order_column=body.order_column,
                order_direction=body.order_direction,
                filters=body.filters,
                filter_classes=self.download_base_filters,
            )

            try:
                return StreamingResponse(
                    generate_report(
                        self.datamodel.query.yield_per(db, 100),
                        self.list_columns,
                        self.label_columns,
                    ),
                    media_type="text/csv",
                    headers={
                        "Content-Disposition": f"attachment; filename={self.resource_name}.csv",
                    },
                )
            finally:
                await db.close()

    def _init_bulk_endpoint(self):
        """
        Initializes the bulk endpoint for the API.

        This method sets up the HTTP route for bulk operations.

        Returns:
            None
        """

        @permission_name(self, "bulk")
        @self.router.post(
            "/bulk/{handler}",
            response_model=GeneralResponse,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "bulk")),
            ],
        )
        async def bulk(
            handler: str,
            body: dict | list = Body(...),
            db: AsyncSession = Depends(get_db),
        ):
            bulk_handler: function | None = getattr(self, f"bulk_{handler}", None)
            if not bulk_handler:
                raise HTTPException(status_code=404, detail="Handler not found")
            try:
                response = await bulk_handler(body, db)
                return response
            except NotImplementedError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))

    async def bulk_handler(self, body: dict | list, db: AsyncSession) -> Response:
        """
        Bulk handler for the API.
        To be implemented by the subclass.

        Example:
        ```python
        async def bulk_read(self, body: dict | list, db: AsyncSession):
            self.datamodel.query.where_in(self.datamodel.get_pk_attr(), [item["id"] for item in body])
            items = await self.datamodel.query.execute(db)
            pks, data = self._convert_to_result(items)
            return data
        ```

        Args:
            body (dict | list): The request body.
            db (AsyncSession): The async db object for the database connection.

        Returns:
            Response: The response object.

        Raises:
            NotImplementedError: If the method is not implemented. To be implemented by the subclass.
        """
        raise NotImplementedError("Bulk handler not implemented")

    def _init_list_endpoint(self):
        """
        Initializes the list endpoint for the API.

        This method sets up the HTTP route for retrieving all items.

        Returns:
            None
        """

        @permission_name(self, "get")
        @self.router.get(
            "/",
            response_model=self.list_return_schema,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "get")),
            ],
        )
        async def get_all(
            q: self.query_schema = Depends(),
            db: AsyncSession = Depends(get_db),
        ):
            for filter in q.filters:
                if not filter.col in self.search_columns:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid filter: {filter.col}"
                    )
            base_order = None
            base_order_direction = None
            if self.base_order:
                base_order, base_order_direction = self.base_order
            filter_classes = self.base_filters
            await self.datamodel.query.add_options(
                db,
                join_columns=self.list_join_columns,
                page=q.page,
                page_size=q.page_size,
                order_column=q.order_column or base_order,
                order_direction=q.order_direction or base_order_direction,
                filters=q.filters,
                filter_classes=filter_classes,
            )
            items = await self.datamodel.query.execute(db)
            count = await self.datamodel.query.count(db, q.filters, filter_classes)
            pks, data = self._convert_to_result(items)
            body = self.list_return_schema(
                result=data,
                count=count,
                ids=pks,
                description_columns=self.description_columns,
                label_columns=self.label_columns,
                list_columns=self.list_columns,
                list_title=self.list_title,
                order_columns=self.order_columns,
            )
            self.pre_get_list(body)
            return body

    def pre_get_list(self, body: BaseResponseMany):
        """
        Pre-process the list response before returning it.
        The response still needs to adhere to the BaseResponseMany schema.

        Args:
            body (BaseResponseMany): The response body.
        """
        pass

    def _init_get_endpoint(self):
        """
        Initializes the get endpoint for the API.

        This method sets up the HTTP route for retrieving a single item.

        Returns:
            None
        """

        @permission_name(self, "get")
        @self.router.get(
            "/{id}",
            response_model=self.show_return_schema,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "get")),
            ],
        )
        async def get_one(
            id: self.datamodel.id_schema,
            db: AsyncSession = Depends(get_db),
        ):
            await self.datamodel.query.add_options(
                db,
                join_columns=self.show_join_columns,
                where_id=id,
                filter_classes=self.show_base_filters,
            )
            item = await self.datamodel.query.execute(db, many=False)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            pk, data = self._convert_to_result(item)
            body = self.show_return_schema(
                id=pk,
                result=data,
                description_columns=self.description_columns,
                label_columns=self.label_columns,
                show_columns=self.show_columns,
                show_title=self.show_title,
            )
            self.pre_get(body)
            return body

    def pre_get(self, body: BaseResponseSingle):
        """
        Pre-process the get response before returning it.
        The response still needs to adhere to the BaseResponseSingle schema.

        Args:
            body (BaseResponseSingle): The response body.
        """
        pass

    def _init_create_endpoint(self):
        """
        Initializes the create endpoint for the API.

        This method sets up the HTTP route for creating a new item.

        Returns:
            None
        """

        @permission_name(self, "post")
        @self.router.post(
            "/",
            response_model=self.add_return_schema,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "post")),
            ],
        )
        async def create(body: self.add_schema, db: AsyncSession = Depends(get_db)):
            body_json = await self._process_body(db, body)
            item = self.datamodel.obj(**body_json)
            self.pre_add(item)
            db.add(item)
            await db.commit()
            self.post_add(item)
            pk, data = self._convert_to_result(item)
            body = self.add_return_schema(id=pk, result=data)
            return body

    def pre_add(self, item: Model) -> None:
        """
        Pre-process the item before adding it to the database.

        Args:
            item: The item to be added to the database.
        """
        pass

    def post_add(self, item: Model) -> None:
        """
        Post-process the item after adding it to the database.
        But before sending the response.

        Args:
            item: The item that was added to the database.
        """
        pass

    def _init_update_endpoint(self):
        """
        Initializes the update endpoint for the API.

        This method sets up the HTTP route for updating an existing item.

        Returns:
            None
        """

        @permission_name(self, "put")
        @self.router.put(
            "/{id}",
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "put")),
            ],
        )
        async def update(
            id: self.datamodel.id_schema,
            body: self.edit_schema,
            db: AsyncSession = Depends(get_db),
        ):
            await self.datamodel.query.add_options(
                db,
                join_columns=self.show_join_columns,
                where_id=id,
            )
            item = await self.datamodel.query.execute(db, many=False)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            body_json = await self._process_body(db, body)
            item.update(body_json)
            self.pre_update(item)
            await db.commit()
            self.post_update(item)
            body_schema = self.datamodel.generate_schema(body_json.keys(), False)
            return body_schema.model_validate(item)

    def pre_update(self, item: Model) -> None:
        """
        Pre-process the item before updating it in the database.

        Args:
            item: The item to be updated in the database.
        """
        pass

    def post_update(self, item: Model) -> None:
        """
        Post-process the item after updating it in the database.
        But before sending the response.

        Args:
            item: The item that was updated in the database.
        """
        pass

    def _init_delete_endpoint(self):
        """
        Initializes the delete endpoint for the API.

        This method sets up the HTTP route for deleting an item.

        Returns:
            None
        """

        @permission_name(self, "delete")
        @self.router.delete(
            "/{id}",
            response_model=GeneralResponse,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "delete")),
            ],
        )
        async def delete(
            id: self.datamodel.id_schema,
            db: AsyncSession = Depends(get_db),
        ):
            await self.datamodel.query.add_options(
                db,
                join_columns=self.show_join_columns,
                where_id=id,
            )
            item = await self.datamodel.query.execute(db, many=False)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            self.pre_delete(item)
            await db.delete(item)
            await db.commit()
            self.post_delete(item)
            body = GeneralResponse(detail="Item deleted")
            return body

    def pre_delete(self, item: Model) -> None:
        """
        Pre-process the item before deleting it from the database.

        Args:
            item: The item to be deleted from the database.
        """
        pass

    def post_delete(self, item: Model) -> None:
        """
        Post-process the item after deleting it from the database.
        But before sending the response.

        Args:
            item: The item that was deleted from the database.
        """
        pass

    """
    -----------------------------------------
            CONVERSION FUNCTIONS
    -----------------------------------------
    """

    def _convert_to_result(self, data: Model | List[Model]):
        """
        Converts the given data to a result tuple.

        Args:
            data (Model | List[Model]): The data to be converted.

        Returns:
            tuple: A tuple containing the primary key(s) and the converted data.

        """
        if isinstance(data, list):
            pks = (
                [getattr(item, self.datamodel.get_pk_attr()) for item in data]
                if not self.datamodel.is_pk_composite()
                else [
                    {key: getattr(item, key) for key in self.datamodel.get_pk_attrs()}
                    for item in data
                ]
            )
        else:
            pks = (
                getattr(data, self.datamodel.get_pk_attr())
                if not self.datamodel.is_pk_composite()
                else {key: getattr(data, key) for key in self.datamodel.get_pk_attrs()}
            )

        return (pks, data)

    def _create_request_schema(
        self, columns: list[str] = [], optional=False
    ) -> Dict[str, Any]:
        """
        Create a request schema based on the data model. Useful for creating the schema for POST and PUT requests.
        Ignoring the primary key and foreign key columns. Adjusting the schema for relation columns.

        Args:
            columns (list[str]): The list of columns to include in the request schema. If empty, no columns will be included. Defaults to [].
            optional (bool): If True, the fields will be optional. Defaults to False.

        Returns:
            A dictionary representing the request schema, where the keys are the field names
            and the values are tuples containing the field type and default value.
        """
        columns = [x for x in columns if not self.datamodel.is_pk(x)]
        new_schema = self.datamodel.generate_schema(columns, False, optional)
        new_schema.model_config["extra"] = "forbid"

        rel_columns = [x for x in columns if self.datamodel.is_relation(x)]
        rel_schema = dict()

        for col in rel_columns:
            params = {}
            if optional:
                params["default"] = IgnoredData()
            elif self.datamodel.is_nullable(col):
                params["default"] = None
            # For relation, where the relation is one-to-one or many-to-one
            if self.datamodel.is_relation_one_to_one(
                col
            ) or self.datamodel.is_relation_many_to_one(col):
                related_interface = self.datamodel.get_related_interface(col)
                type = related_interface.id_schema | RelInfo
                if optional:
                    type = type | IgnoredData
                if self.datamodel.is_nullable(col):
                    type = type | None
                rel_schema[col] = (
                    type,
                    Field(**params),
                )
            else:
                if not optional:
                    params["default"] = []
                type = (
                    List[self.datamodel.get_related_interface(col).id_schema]
                    | List[RelInfo]
                )
                if optional:
                    type = type | IgnoredData
                if self.datamodel.is_nullable(col):
                    type = type | None
                related_interface = self.datamodel.get_related_interface(col)
                rel_schema[col] = (
                    type,
                    Field(**params),
                )

        return create_model(
            new_schema.__name__,
            **rel_schema,
            __base__=new_schema,
        )

    async def _update_info_schema(self, permissions: List[str], db: AsyncSession):
        """
        Update the information schema for the API.

        Args:
            permissions (List[str]): The list of permissions for the API.
            db (AsyncSession): The async db object for the database connection.

        Returns:
            None
        """
        self.info_return_schema.permissions = permissions
        self.info_return_schema.add_columns = []
        self.info_return_schema.edit_columns = []
        self.info_return_schema.filters = {}

        for key, val in self.filter_options.items():
            val = val() if callable(val) else val
            self.info_return_schema.filter_options[key] = val

        rel_cache = {}

        for col in self.add_columns:
            filters = self.add_query_rel_fields.get(col, [])
            order_column, order_direction = self.order_rel_fields.get(col, (None, None))
            cache_key = f"{col}_{filters}_{order_column}_{order_direction}"
            col_info = rel_cache.get(cache_key)
            if not col_info:
                col_info = await self._get_column_info(
                    col,
                    db,
                    filters,
                    order_column,
                    order_direction,
                )
                rel_cache[cache_key] = col_info
            self.info_return_schema.add_columns.append(col_info)

        for col in self.edit_columns:
            filters = self.edit_query_rel_fields.get(col, [])
            order_column, order_direction = self.order_rel_fields.get(col, (None, None))
            cache_key = f"{col}_{filters}_{order_column}_{order_direction}"
            col_info = rel_cache.get(cache_key)
            if not col_info:
                col_info = await self._get_column_info(
                    col,
                    db,
                    filters,
                    order_column,
                    order_direction,
                )
                rel_cache[cache_key] = col_info
            self.info_return_schema.edit_columns.append(col_info)

        for col in self.search_columns:
            info = dict()
            filters = self.cache.get(f"info_filters_{col}", None)
            if not filters:
                filters = [
                    {"name": filter.name, "operator": filter.arg_name}
                    for filter in self.datamodel._filters.get(col)
                ]
                self.cache[f"info_filters_{col}"] = filters
            info["filters"] = filters
            info["label"] = self.label_columns.get(col)
            query_filters = self.search_query_rel_fields.get(col, [])
            order_column, order_direction = self.order_rel_fields.get(col, (None, None))
            cache_key = f"{col}_{query_filters}_{order_column}_{order_direction}"
            info["schema"] = rel_cache.get(cache_key)
            if not info["schema"]:
                info["schema"] = await self._get_column_info(
                    col,
                    db,
                    query_filters,
                    order_column,
                    order_direction,
                )
            self.info_return_schema.filters[col] = info

    async def _get_column_info(
        self,
        col: str,
        db: AsyncSession,
        filters: List[Tuple[str, BaseFilter, Any]] = [],
        order_column: str | None = None,
        order_direction: str | None = None,
    ) -> ColumnInfo | ColumnRelationInfo:
        """
        Retrieves information about a column in the database table.

        Caches the column information to avoid repeated queries (Except for relations).

        Args:
            col (str): The name of the column.
            db (AsyncSession): The async db object for the database connection.
            filters (List[Tuple[str, BaseFilter, Any]]): The list of filters to apply to the column.
            order_column (str): The column to order by. Defaults to None.
            order_direction (str): The direction to order by. Defaults to None.

        Returns:
            ColumnInfo | ColumnRelationInfo: An object containing information about the column.

        Raises:
            None

        """
        column_info = self.cache.get(f"column_info_{col}", {})
        if column_info:
            return column_info

        column_info = {
            "description": self.description_columns.get(col, ""),
            "label": self.label_columns.get(col, ""),
            "name": col,
            "required": not self.datamodel.is_nullable(col),
            "unique": self.datamodel.is_unique(col),
        }

        if self.datamodel.is_relation(col):
            type = "Related"
            if self.datamodel.is_relation_one_to_many(
                col
            ) or self.datamodel.is_relation_many_to_many(col):
                type = "RelatedList"
            related_interface = self.datamodel.get_related_interface(col)
            await related_interface.query.add_options(
                db,
                page=0,
                page_size=self.max_page_size,
                order_column=order_column,
                order_direction=order_direction,
                filter_classes=filters,
            )
            related_items = await related_interface.query.execute(db)
            count = await related_interface.query.count(db, filter_classes=filters)
            values = []
            for item in related_items:
                if related_interface.is_pk_composite():
                    id = {
                        pk: getattr(item, pk) for pk in related_interface.get_pk_attrs()
                    }
                else:
                    id = getattr(item, related_interface.get_pk_attr())
                values.append({"id": id, "value": str(item)})
            column_info["count"] = count
            column_info["values"] = values
            column_info["type"] = type
            return ColumnRelationInfo(**column_info)
        else:
            column_info["type"] = self.datamodel.get_type_name(col)

        info = ColumnInfo(**column_info)
        self.cache[f"column_info_{col}"] = info
        return info

    async def _process_body(self, db: AsyncSession, body: BaseModel) -> Dict[str, Any]:
        """
        Process the body of the request by handling relations and returning a new body dictionary.

        Args:
            db (AsyncSession): The async db object for the database connection.
            body (BaseModel): The body of the request as a BaseModel object.

        Returns:
            Dict[str, Any]: The transformed body dictionary.

        Raises:
            HTTPException: If any related items are not found or if an item is not found for a one-to-one or many-to-one relation.
        """
        body_json = dump_schema(body)
        new_body = {}
        for key, value in body_json.items():
            # For relation, where the relation is one-to-many or many-to-many
            if self.datamodel.is_relation_one_to_many(
                key
            ) or self.datamodel.is_relation_many_to_many(key):
                # Ignore if the value is an empty list
                if not value:
                    new_body[key] = []
                    continue

                for val in value:
                    if isinstance(val, dict):
                        val = val.get("id")

                related_interface = self.datamodel.get_related_interface(key)
                related_interface.query.where_id_in(value)
                related_items = await related_interface.query.execute(db)

                # If the length is not equal, then some items were not found
                if len(related_items) != len(value):
                    raise HTTPException(
                        status_code=400, detail=f"Some items in {key} not found"
                    )

                new_body[key] = related_items
                continue

            # For relation, where the relation is one-to-one or many-to-one
            if self.datamodel.is_relation_one_to_one(
                key
            ) or self.datamodel.is_relation_many_to_one(key):
                # Ignore if the value is None or 0, or an empty string
                if not value:
                    new_body[key] = None
                    continue

                if isinstance(value, dict):
                    value = value.get("id")

                related_interface = self.datamodel.get_related_interface(key)
                related_interface.query.where_id(value)
                related_item = await related_interface.query.execute(db, many=False)

                if not related_item:
                    raise HTTPException(
                        status_code=400, detail=f"Item in {key} not found"
                    )

                new_body[key] = related_item
                continue

            # For other columns, just add the value to the new body
            new_body[key] = value
        return new_body

    """
    -----------------------------------------
         HELPER FUNCTIONS
    -----------------------------------------
    """

    def _gen_labels_columns(self, list_columns: List[str]) -> None:
        """
        Auto generates pretty label_columns from list of columns
        """
        for col in list_columns:
            if not self.label_columns.get(col):
                self.label_columns[col] = self._prettify_column(col)

    @staticmethod
    def _prettify_name(name: str) -> str:
        """
        Prettify pythonic variable name.

        For example, 'HelloWorld' will be converted to 'Hello World'

        :param name:
            Name to prettify.
        """
        return re.sub(r"(?<=.)([A-Z])", r" \1", name)

    @staticmethod
    def _prettify_column(name: str) -> str:
        """
        Prettify pythonic variable name.

        For example, 'hello_world' will be converted to 'Hello World'

        :param name:
            Name to prettify.
        """
        return re.sub("[._]", " ", name).title()

    @property
    def cache(self):
        """
        Returns the cache dictionary.

        If the cache dictionary is not initialized, it initializes it as an empty dictionary.

        Returns:
            dict: The cache dictionary.
        """
        if not self._cache:
            self._cache = {}
        return self._cache
