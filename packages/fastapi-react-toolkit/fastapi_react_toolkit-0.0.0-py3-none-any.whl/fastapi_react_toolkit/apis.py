from fastapi import Depends, HTTPException, Request, exceptions, status
from fastapi_users.router.common import ErrorCode, ErrorModel

from .api import ModelRestApi, SQLAInterface
from .decorators import permission_name
from .globals import g
from .manager import UserManager
from .models import Api, Permission, PermissionApi, Role, User
from .routers import get_oauth_router
from .schemas import UserCreate, UserRead, UserUpdate


class PermissionViewApi(ModelRestApi):
    resource_name = "permissionview"
    datamodel = SQLAInterface(PermissionApi)


class ViewsMenusApi(ModelRestApi):
    resource_name = "viewsmenus"
    datamodel = SQLAInterface(Api)


class PermissionsApi(ModelRestApi):
    resource_name = "permissions"
    datamodel = SQLAInterface(Permission)


class RolesApi(ModelRestApi):
    resource_name = "roles"
    datamodel = SQLAInterface(Role)


class InfoApi(ModelRestApi):
    resource_name = "info"

    security_level_apis = [
        "PermissionsApi",
        "RolesApi",
        "UsersApi",
        "ViewsMenusApi",
        "PermissionViewApi",
    ]
    excluded_apis = ["InfoApi", "AuthApi"]

    def __init__(self) -> None:
        super().__init__()

        @self.router.get("/")
        @permission_name(self, "info")
        async def get_info():
            if not self.toolkit:
                return []

            apis = self.cache.get("get_info", [])
            if apis:
                return apis

            for api in self.toolkit.apis:
                if api.__class__.__name__ in self.excluded_apis:
                    continue

                api_info = {}
                api_info["name"] = api.resource_name.capitalize()
                api_info["icon"] = "Table" if api.datamodel else ""
                api_info["permission_name"] = api.__class__.__name__
                api_info["path"] = api.resource_name
                api_info["type"] = "table" if api.datamodel else "default"
                api_info["level"] = (
                    "security" if api in self.security_level_apis else "default"
                )
                apis.append(api_info)

            self.cache["get_info"] = apis
            return apis


class UsersApi(ModelRestApi):
    resource_name = "users"
    datamodel = SQLAInterface(User)

    exclude_routes = ["post"]

    list_exclude_columns = ["password", "hashed_password"]
    show_exclude_columns = ["password", "hashed_password"]
    add_exclude_columns = [
        "active",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]
    edit_exclude_columns = [
        "username",
        "password",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]

    def __init__(self) -> None:
        super().__init__()
        self.label_columns["password"] = "Password"


class AuthApi(ModelRestApi):
    resource_name = "auth"

    def add_routes(self) -> None:
        self.router.include_router(
            g.fastapi_users.get_auth_router(g.cookie_backend),
        )
        self.router.include_router(
            g.fastapi_users.get_auth_router(g.jwt_backend),
            prefix="/jwt",
        )
        self.router.include_router(
            g.fastapi_users.get_register_router(UserRead, UserCreate),
        )
        self.router.include_router(
            g.fastapi_users.get_reset_password_router(),
        )
        self.router.include_router(
            g.fastapi_users.get_verify_router(UserRead),
        )

        for oauth_client in g.oauth_clients:
            associate_by_email = False

            # Check whether the oauth_client is a tuple
            try:
                oauth_client, associate_by_email = oauth_client
            except:
                pass

            self.router.include_router(
                get_oauth_router(
                    oauth_client=oauth_client,
                    backend=g.cookie_backend,
                    get_user_manager=g.fastapi_users.get_user_manager,
                    state_secret=g.secret_key,
                    redirect_url=g.oauth_redirect_uri,
                    associate_by_email=associate_by_email,
                ),
            )

        get_current_active_user = g.fastapi_users.authenticator.current_user(
            active=True, verified=False
        )
        get_user_manager = g.fastapi_users.get_user_manager

        @self.router.get(
            "/user",
            response_model=UserRead,
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
            },
        )
        async def user(
            user: UserRead = Depends(get_current_active_user),
        ):
            return user

        @self.router.put(
            "/user",
            response_model=UserRead,
            dependencies=[Depends(get_current_active_user)],
            responses={
                status.HTTP_401_UNAUTHORIZED: {
                    "description": "Missing token or inactive user.",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "model": ErrorModel,
                    "content": {
                        "application/json": {
                            "examples": {
                                ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                                    "summary": "A user with this email already exists.",
                                    "value": {
                                        "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                                    },
                                },
                                ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                                    "summary": "Password validation failed.",
                                    "value": {
                                        "detail": {
                                            "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                            "reason": "Password should be"
                                            "at least 3 characters",
                                        }
                                    },
                                },
                            }
                        }
                    },
                },
            },
        )
        async def update_user(
            request: Request,
            user_update: UserUpdate,
            user: User = Depends(get_current_active_user),
            user_manager: UserManager = Depends(get_user_manager),
        ):
            try:
                user = await user_manager.update(
                    user_update, user, safe=True, request=request
                )
                return UserUpdate.model_validate(user)
            except exceptions.InvalidPasswordException as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                        "reason": e.reason,
                    },
                )
            except exceptions.UserAlreadyExists:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
                )
