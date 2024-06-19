from typing import Any

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..db import QueryManager
from ..schemas import FilterSchema
from .filters import GenericBaseFilter
from .model import GenericModel, GenericSession


class GenericQueryManager(QueryManager):
    """
    A class to manage database queries for generic. It provides methods to add options for pagination, ordering, and filtering to the query.

    Raises:
        e: If an error occurs during query execution.
    """

    session: GenericSession | None = None

    def __init__(self, datamodel: Any, session: GenericSession | None = None):
        self.session = session
        super().__init__(datamodel)

    def where(self, column: str, value: Any):
        self._apply_where(column, value)

    def where_in(self, column: str, values: list[Any]):
        self._apply_where_in(column, values)

    async def count(
        self,
        db: AsyncSession,
        filters: list[FilterSchema] = ...,
        filter_classes: list[tuple[str, GenericBaseFilter, Any]] = ...,
    ) -> int:
        try:
            self._init_query()
            await self._apply_filters(None, filters)
            self._apply_filter_classes(filter_classes)
            count, _ = self.session.all()
            return count
        finally:
            self._init_query()

    async def execute(
        self, db: AsyncSession, many=True
    ) -> GenericModel | list[GenericModel] | None:
        try:
            _, items = self.session.all()
            if many:
                return items

            return items[0] if items else None
        except Exception as e:
            raise e
        finally:
            self._init_query()

    async def yield_per(self, db: AsyncSession, page_size: int):
        try:
            items = self.session.yield_per(page_size)
            while True:
                chunk = items[:page_size]
                items = items[page_size:]
                if not chunk:
                    break
                yield chunk
        finally:
            self._init_query()

    def _init_query(self):
        self.session = self.session.query(self.datamodel.obj)

    def _apply_where(self, column: str, value: Any):
        self.session = self.session.equal(column, value)

    def _apply_where_in(self, column: str, values: list[Any]):
        self.session = self.session.in_(column, values)

    def _apply_join(self, join_columns: list[str]) -> NotImplementedError:
        pass

    def _apply_page(self, page: int | None, page_size: int | None):
        if page is None or page_size is None:
            return
        self.session = self.session.offset(page * page_size).limit(page_size)

    def _apply_order(self, order_column: str | None, order_direction: str | None):
        if not order_column or not order_direction:
            return
        col = order_column
        col = col.lstrip()

        #! If the order column comes from a request, it will be in the format ClassName.column_name
        if col.startswith(self.datamodel.obj.__class__.__name__) or col.startswith(
            self.datamodel.obj.__name__
        ):
            col = col.split(".", 1)[1]

        self.session = self.session.order_by(f"{col} {order_direction}")

    async def _apply_filter(self, _: None, filter: FilterSchema):
        filter_classes = self.datamodel._filters.get(filter.col)
        filter_class = None
        for f in filter_classes:
            if f.arg_name == filter.opr:
                filter_class = f
                break
        if not filter_class:
            raise HTTPException(
                status_code=400, detail=f"Invalid filter opr: {filter.opr}"
            )

        col = filter.col
        value = filter.value

        self.session = filter_class.apply(self.session, col, value)

    def _apply_filter_class(
        self, col: str, filter_class: GenericBaseFilter, value: Any
    ):
        self.session = filter_class.apply(self.session, col, value)
