import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_react_toolkit import (
    FastapiReactToolkit,
    User,
    current_active_user,
    session_manager,
)
from fastapi_react_toolkit.manager import UserManager

from .base_data import add_base_data

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.INFO)


class CustomUserManager(UserManager):
    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        await super().on_after_login(user, request, response)
        print("User logged in: ", user)

    pass


toolkit = FastapiReactToolkit(
    config_file="./app/config.py",
    user_manager=CustomUserManager,
    # password_helper=FABPasswordHelper(), #! Add this line to use old password hash
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run when the app is starting up
    toolkit.connect_to_database()

    # Not needed if you setup a migration system like Alembic
    async with session_manager.connect() as conn:
        await session_manager.create_all(conn)

    # Creating permission, apis, roles, and connecting them
    await toolkit.init_database()

    async with session_manager.session() as session:
        # Add base data
        await add_base_data(session)

    yield

    # Run when the app is shutting down
    if session_manager._engine:
        await session_manager.close()


app = FastAPI(lifespan=lifespan, docs_url="/openapi/v1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
toolkit.initialize(app)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    print("USER ROLES: ", user.roles)
    return {"message": f"Hello {user.email}!"}

from .apis import *

toolkit.mount()
