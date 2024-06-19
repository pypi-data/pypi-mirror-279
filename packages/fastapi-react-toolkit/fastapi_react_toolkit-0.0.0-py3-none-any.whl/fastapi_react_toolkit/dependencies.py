from fastapi import Depends, HTTPException

from .const import *
from .db import *
from .globals import g
from .models import PermissionApi

current_active_user = g.fastapi_users.current_user(active=True)


def permissions(as_object=False):
    """
    A dependency for FAST API to list all the apis that the current user has access to.

    Usage:
    ```python
    async def get_info(
            *,
            permissions: List[str] = Depends(permissions()),
            db: AsyncSession = Depends(get_async_session),
        ):
    ...more code
    ```

    Args:
        as_object (bool): Whether to return the permission objects or just the names.

    """

    async def permissions_depedency(
        user: User | None = Depends(current_active_user),
    ):
        g.user = user
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if not user.roles:
            raise HTTPException(status_code=403, detail="Forbidden")

        permissions = []
        for role in user.roles:
            for permission_api in role.permissions:
                if as_object:
                    permissions.append(permission_api)
                else:
                    permissions.append(permission_api.api.name)
        permissions = list(set(permissions))

        return permissions

    return permissions_depedency


def current_permissions(api):
    """
    A dependency for FAST API to list all the permissions of current user in the specified API.

    Usage:
    ```python
    async def get_info(
            *,
            permissions: List[str] = Depends(current_permissions(self)),
            db: AsyncSession = Depends(get_async_session),
        ):
    ...more code
    ```

    Args:
        api (ModelRestApi): The API to be checked.
    """

    async def current_permissions_depedency(
        permissions_apis: list[PermissionApi] = Depends(permissions(as_object=True)),
    ):
        return [
            permission_api.permission.name
            for permission_api in permissions_apis
            if permission_api.api.name == api.__class__.__name__
        ]

    return current_permissions_depedency


def has_access(
    api,
    permission: str,
):
    """
    A dependency for FAST API to check whether current user has access to the specified API and permission.

    Usage:
    ```python
    @self.router.get(
            "/_info",
            response_model=self.info_return_schema,
            dependencies=[
                Depends(current_active_user),
                Depends(has_access(self, "info")),
            ],
        )
    ...more code
    ```

    Args:
        api (ModelRestApi): The API to be checked.
        permission (str): The permission to check.
    """

    async def has_access_depedency(
        permissions: list[str] = Depends(current_permissions(api)),
    ):
        if f"{PERMISSION_PREFIX}{permission}" not in permissions:
            raise HTTPException(status_code=403, detail="Forbidden")
        return

    return has_access_depedency
