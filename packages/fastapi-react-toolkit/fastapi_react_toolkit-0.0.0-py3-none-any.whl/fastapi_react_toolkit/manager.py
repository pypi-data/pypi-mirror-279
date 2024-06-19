from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, exceptions
from fastapi_users.db import BaseUserDatabase
from fastapi_users.password import PasswordHelperProtocol

from .db import UserDatabase
from .models import User


class IDParser:
    def parse_id(self, value: Any) -> int:
        if isinstance(value, int):
            return value
        try:
            return int(value)
        except ValueError as e:
            raise exceptions.InvalidID() from e


class UserManager(IDParser, BaseUserManager[User, int]):
    user_db: UserDatabase

    def __init__(
        self,
        user_db: BaseUserDatabase[User, int],
        secret_key: str,
        password_helper: PasswordHelperProtocol | None = None,
    ):
        super().__init__(user_db, password_helper)
        self.reset_password_token_secret = secret_key
        self.verification_token_secret = secret_key

    async def get_by_username(self, username: str) -> User | None:
        """
        Get a user by its username.

        :param username: The username of the user.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_username(username)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def authenticate(self, credentials: OAuth2PasswordRequestForm) -> User | None:
        """
        Override the default authenticate method to search by username instead of email.

        Args:
            credentials (OAuth2PasswordRequestForm): The credentials to authenticate the user.

        Returns:
            User | None: The user if the credentials are valid, None otherwise.
        """
        try:
            user = await self.get_by_username(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            return None

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            await self.user_db.update(
                user, {"fail_login_count": user.fail_login_count + 1}
            )
            return None
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        await self.user_db.update(user, {"fail_login_count": 0})
        return user

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        """
        Perform logic after user login.

        Please call await super().on_after_login(user, request, response) to keep the default behavior.

        *You should overload this method to add your own logic.*

        :param user: The user that is logging in
        :param request: Optional FastAPI request
        :param response: Optional response built by the transport.
        Defaults to None
        """
        update_fields = {
            "last_login": datetime.now(UTC),
            "login_count": user.login_count + 1,
        }
        await self.user_db.update(user, update_fields)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        raise HTTPException(status_code=501, detail="Not implemented")

    async def on_after_reset_password(
        self, user: User, request: Request | None = None
    ) -> None:
        raise HTTPException(status_code=501, detail="Not implemented")

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        raise HTTPException(status_code=501, detail="Not implemented")
