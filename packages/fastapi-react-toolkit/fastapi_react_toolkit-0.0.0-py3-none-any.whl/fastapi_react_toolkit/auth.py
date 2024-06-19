from typing import Optional, Tuple, Type

from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend
from fastapi_users.authentication import Authenticator as BaseAuthenticator
from fastapi_users.authentication import BearerTransport, CookieTransport, JWTStrategy
from fastapi_users.models import ID, UP
from fastapi_users.password import PasswordHelper, PasswordHelperProtocol
from pwdlib import PasswordHash

from .const import *
from .db import User, UserDatabase, get_user_db
from .hasher import PBKDF2Hasher, ScryptHasher
from .manager import UserManager


class FABPasswordHelper(PasswordHelper):
    """
    Helper class for old version of password-related operations in the FAB React Toolkit.

    Args:
        password_hash (Optional[PasswordHash]): An optional `PasswordHash` object to use for password hashing.

    Attributes:
        password_hash (PasswordHash): The `PasswordHash` object used for password hashing.

    """

    def __init__(self, password_hash: Optional[PasswordHash] = None) -> None:
        if password_hash is None:
            self.password_hash = PasswordHash(
                (
                    ScryptHasher(),
                    PBKDF2Hasher(),
                )
            )
        else:
            self.password_hash = password_hash  # pragma: no cover


class Authenticator(BaseAuthenticator):

    async def _authenticate(
        self,
        *args,
        user_manager: BaseUserManager[UP, ID],
        optional: bool = False,
        active: bool = False,
        verified: bool = False,
        superuser: bool = False,
        **kwargs,
    ) -> Tuple[UP | None, str | None]:
        user, token = await super()._authenticate(
            *args,
            user_manager=user_manager,
            optional=optional,
            active=active,
            verified=verified,
            superuser=superuser,
            **kwargs,
        )

        # Retrieve list of apis, that user has access to
        if user:
            user.permissions = []
            for role in user.roles:
                for permission_api in role.permissions:
                    user.permissions.append(permission_api.api.name)
            user.permissions = list(set(user.permissions))

        return user, token


class AuthConfigurator:
    password_helper: PasswordHelperProtocol | None = None

    _secret_key = DEFAULT_SECRET
    _cookie_warned = False
    _user_manager: Type[UserManager] | None = None
    _cookie_transport: CookieTransport | None = None
    _bearer_transport: BearerTransport | None = None
    _cookie_backend: AuthenticationBackend | None = None
    _jwt_backend: AuthenticationBackend | None = None
    _authenticator: Authenticator | None = None
    _fastapi_users: FastAPIUsers | None = None

    def __init__(self):
        if self.__class__.__name__ == "AuthConfigurator":
            raise Exception(
                "AuthConfigurator is a singleton and cannot be instantiated."
            )

    @property
    def secret_key(self):
        """
        Get the secret key.

        Returns:
            The secret key.
        """
        if self._secret_key == DEFAULT_SECRET and not self._cookie_warned:
            self._cookie_warned = True
            logger.warning(
                "You are using the default secret key. Please change it in production."
            )
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        """
        Set the secret key.

        Args:
            value: The secret key value.
        """
        self._secret_key = value

    @property
    def user_manager(self):
        """
        Get the user manager.

        if the user manager is not set, it will default to the UserManager class.

        Returns:
            The user manager.
        """
        if self._user_manager is None:
            self._user_manager = UserManager
        return self._user_manager

    @user_manager.setter
    def user_manager(self, value):
        """
        Set the user manager.

        Use this to use a custom user manager.

        Args:
            value: The user manager value.
        """
        self._user_manager = value

    @property
    def cookie_transport(self):
        """
        Get the cookie transport.

        if the cookie transport is not set, it will default to the cookie_transport global variable.

        Returns:
            The cookie transport.
        """
        if self._cookie_transport is None:
            self._cookie_transport = CookieTransport(
                cookie_name=DEFAULT_COOKIE_NAME, cookie_max_age=3600
            )
        return self._cookie_transport

    @cookie_transport.setter
    def cookie_transport(self, value):
        """
        Set the cookie transport.

        Use this to use a custom cookie transport.

        Args:
            value: The cookie transport value.
        """
        self._cookie_transport = value

        # Clear dependent cookie backend
        self._cookie_backend = None

    @property
    def bearer_transport(self):
        """
        Get the bearer transport.

        if the bearer transport is not set, it will default to the bearer_transport global variable.

        Returns:
            The bearer transport.
        """
        if self._bearer_transport is None:
            self._bearer_transport = BearerTransport(tokenUrl=DEFAULT_TOKEN_URL)
        return self._bearer_transport

    @bearer_transport.setter
    def bearer_transport(self, value):
        """
        Set the bearer transport.

        Use this to use a custom bearer transport.

        Args:
            value: The bearer transport value.
        """
        self._bearer_transport = value

        # Clear dependent JWT backend
        self._jwt_backend = None

    @property
    def cookie_backend(self):
        """
        Get the cookie backend.

        if the cookie backend is not set, it will default to the cookie_backend global variable.

        Returns:
            The cookie backend.
        """
        if self._cookie_backend is None:
            self._cookie_backend = AuthenticationBackend(
                name="cookie",
                transport=self.cookie_transport,
                get_strategy=self.get_jwt_strategy,
            )
        return self._cookie_backend

    @cookie_backend.setter
    def cookie_backend(self, value):
        """
        Set the cookie backend.

        Use this to use a custom cookie backend.

        Args:
            value: The cookie backend value.
        """
        self._cookie_backend = value

        # Clear dependent authenticator
        self._authenticator = None

    @property
    def jwt_backend(self):
        """
        Get the JWT backend.

        if the JWT backend is not set, it will default to the jwt_backend global variable.

        Returns:
            The JWT backend.
        """
        if self._jwt_backend is None:
            self._jwt_backend = AuthenticationBackend(
                name="jwt",
                transport=self.bearer_transport,
                get_strategy=self.get_jwt_strategy,
            )
        return self._jwt_backend

    @jwt_backend.setter
    def jwt_backend(self, value):
        """
        Set the JWT backend.

        Use this to use a custom JWT backend.

        Args:
            value: The JWT backend value.
        """
        self._jwt_backend = value

        # Clear dependent authenticator
        self._authenticator = None

    @property
    def authenticator(self):
        """
        Get the authenticator.

        if the authenticator is not set, it will default to the authenticator global variable.

        Returns:
            The authenticator.
        """
        if self._authenticator is None:

            self._authenticator = Authenticator(
                [self.cookie_backend, self.jwt_backend], self.get_user_manager
            )
        return self._authenticator

    @authenticator.setter
    def authenticator(self, value):
        """
        Set the authenticator.

        Use this to use a custom authenticator.

        Args:
            value: The authenticator value.
        """
        self._authenticator = value

        # Clear dependent FastAPIUsers instance
        self._fastapi_users = None

    @property
    def fastapi_users(self):
        """
        Get the FastAPIUsers instance.

        if the FastAPIUsers instance is not set, it will default to the fastapi_users global variable.

        Returns:
            The FastAPIUsers instance.
        """
        if self._fastapi_users is None:

            self._fastapi_users = FastAPIUsers[User, int](
                self.get_user_manager, [self.cookie_backend, self.jwt_backend]
            )
            self.fastapi_users.authenticator = self.authenticator
        return self._fastapi_users

    @fastapi_users.setter
    def fastapi_users(self, value):
        """
        Set the FastAPIUsers instance.

        Use this to use a custom FastAPIUsers instance.

        Args:
            value: The FastAPIUsers instance value.
        """
        self._fastapi_users = value

    async def get_user_manager(self, user_db: UserDatabase = Depends(get_user_db)):
        """
        Get the user manager as a dependency.

        Args:
            user_db: The user database.

        Returns:
            The user manager generator.
        """
        yield self.user_manager(user_db, self.secret_key, self.password_helper)

    def get_jwt_strategy(self):
        """
        Get the JWT strategy as a dependency.

        Returns:
            The JWT strategy generator.
        """
        return JWTStrategy(
            secret=self.secret_key,
            lifetime_seconds=3600,
        )
