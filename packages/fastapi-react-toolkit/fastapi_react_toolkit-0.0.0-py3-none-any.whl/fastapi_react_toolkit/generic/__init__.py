from fastapi import Depends

from ..api import ModelRestApi
from ..decorators import permission_name
from ..dependencies import current_active_user, has_access
from ..schemas import GeneralResponse
from .db import *
from .filters import *
from .interface import *
from .model import *


class GenericApi(ModelRestApi):
    datamodel: GenericInterface

    def _init_delete_endpoint(self):

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
        ):
            await self.datamodel.query.add_options(
                db,
                join_columns=self.show_join_columns,
                where=(self.datamodel.get_pk_attr(), id),
            )
            item = await self.datamodel.query.execute(db, many=False)
            if not item:
                raise HTTPException(status_code=404, detail="Item not found")
            self.pre_delete(item)
            self.datamodel.session.delete(getattr(item, item.pk))
            self.post_delete(item)
            body = GeneralResponse(detail="Item deleted")
            return body

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
        async def create(body: self.add_schema):
            body_json = await self._process_body(db, body)
            item = self.datamodel.obj(**body_json)
            self.pre_add(item)
            self.datamodel.session.add(item)
            self.post_add(item)
            pk, data = self._convert_to_result(item)
            body = self.add_return_schema(id=pk, result=data)
            return body
