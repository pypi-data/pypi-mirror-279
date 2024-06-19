import random
from typing import List

from fastapi import HTTPException, Response
from fastapi_react_toolkit import (
    Depends,
    GeneralResponse,
    GenericApi,
    GenericColumn,
    GenericFilterEqual,
    GenericInterface,
    GenericModel,
    GenericSession,
    ModelRestApi,
    SQLAInterface,
    User,
    current_active_user,
    get_db,
    has_access,
    permission_name,
)
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from .app import toolkit
from .models import *


class AssetApi(ModelRestApi):
    resource_name = "assets"
    datamodel = SQLAInterface(Asset)
    page_size = 200
    description_columns = {
        "name": "Name of the asset",
        "owner_id": "ID of the asset owner",
        "owner": "Owner of the asset",
        "date_time": "Date time of the asset",
        "date": "Date of the asset",
    }
    quick_filters = [
        {
            "name": "asset_name",
            "label": "Asset Name",
            "column": "name",
            "type": "multiselect",
            "options": [
                {"value": f"asset&{i}", "label": f"asset&{i}"} for i in range(10)
            ],
        }
    ]

    def add_routes(self) -> None:

        @self.router.get("/hello", dependencies=[Depends(current_active_user), Depends(has_access(self, "hello"))])
        @permission_name(self, "hello")
        def hello(user: User = Depends(current_active_user), db: AsyncSession = Depends(get_db)):
            return "Hello"

        return super().add_routes()

    async def bulk_update_time(
        self, body: dict | List, session: AsyncSession
    ) -> Response:
        try:
            stmt = (
                update(Asset).where(Asset.id.in_(body)).values(date_time=db.func.now())
            )
            result = await session.execute(stmt)
            await session.commit()
            return GeneralResponse(detail=f"Updated {result.rowcount} records")
        except Exception as e:
            await session.rollback()
            print(e)
            raise HTTPException(status_code=500, detail=str(e))


class ApplicationApi(ModelRestApi):
    resource_name = "applications"
    datamodel = SQLAInterface(Application)
    description_columns = {
        "name": "Name of the Application",
        "description": "Description",
    }
    quick_filters = [
        {
            "name": "application_name",
            "label": "Application Name",
            "column": "name",
            "type": "multiselect",
            "options": [
                {"value": f"application_{i}", "label": f"application_{i}"}
                for i in range(10)
            ],
        }
    ]


class UnitApi(ModelRestApi):
    resource_name = "units"
    datamodel = SQLAInterface(Unit)
    description_columns = {"name": "Name of the unit"}
    quick_filters = [
        {
            "name": "unit_name",
            "label": "Unit Name",
            "column": "name",
            "type": "multiselect",
            "options": [
                {"value": f"unit_{i}", "label": f"unit_{i}"} for i in range(10)
            ],
        }
    ]


class StringPkApi(ModelRestApi):
    resource_name = "stringpk"

    datamodel = SQLAInterface(StringPk)

    def pre_add(self, item) -> None:
        """
        If criticality != green then close green status
        """
        print(item.name)
        item.id = item.name
        pass


class PSModel(GenericModel):
    id = GenericColumn(int, primary_key=True, auto_increment=True)
    first_name = GenericColumn(str, nullable=False)
    last_name = GenericColumn(str, nullable=False)
    email = GenericColumn(str, nullable=False)
    logged_in = GenericColumn(bool)


class PSSession(GenericSession):

    def load_data(self) -> List[GenericModel]:
        # Load 1000 records
        items = []

        for i in range(1000):
            model = PSModel()
            model.first_name = (
                str(i) + " " + random.choice(["John", "Jane", "Doe", "Alice", "Bob"])
            )
            model.last_name = random.choice(
                ["Doe", "Smith", "Johnson", "Brown", "Williams"]
            )
            model.email = (
                f"{model.first_name.lower()}.{model.last_name.lower()}@example.com"
            )
            model.logged_in = random.choice([True, False])
            items.append(model)
        return items


class PSApi(GenericApi):
    resource_name = "generic_datasource"
    base_order = ("email", "desc")
    download_base_filters = [["last_name", GenericFilterEqual, "Smith"]]
    datamodel = GenericInterface(PSModel, PSSession())


toolkit.add_api(AssetApi)
toolkit.add_api(ApplicationApi)
toolkit.add_api(UnitApi)
toolkit.add_api(StringPkApi)
toolkit.add_api(PSApi)
