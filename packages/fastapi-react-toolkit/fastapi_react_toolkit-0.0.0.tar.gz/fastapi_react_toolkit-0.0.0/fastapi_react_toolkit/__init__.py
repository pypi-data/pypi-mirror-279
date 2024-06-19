import importlib.util
import io

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jinja2 import Environment, TemplateNotFound, select_autoescape
from sqlalchemy import and_, create_engine, insert
from sqlalchemy.orm import Session, sessionmaker

# Import all submodules
from .api import *
from .apis import *
from .auth import *
from .const import *
from .db import *
from .decorators import *
from .dependencies import *
from .filters import *
from .generic import *
from .globals import *
from .hasher import *
from .manager import *
from .model import *
from .models import *
from .routers import *
from .schemas import *
from .types import *
from .utils import *


class FastapiReactToolkit:
    """
    The main class for the FastapiReactToolkit library.

    This class provides a set of methods to initialize a FastAPI application, add APIs, manage permissions and roles,
    and initialize the database with permissions, APIs, roles, and their relationships.

    In case you need to create a synchronous session, set the `with_session` parameter to True. this will allow you to use `db` attribute to interact with the database.

    Usage:
    ```python
    toolkit = FastapiReactToolkit(
        config_file="./app/config.py",
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Run when the app is starting up
        toolkit.connect_to_database()

        # Not needed if you setup a migration system like Alembic
        async with sessionmanager.connect() as conn:
            await sessionmanager.create_all(conn)

        # Creating permission, apis, roles, and connecting them
        await toolkit.init_database()

        async with sessionmanager.session() as session:
            # Add base data
            await add_base_data(session)

        yield

        # Run when the app is shutting down
        if sessionmanager._engine:
            await sessionmanager.close()


    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    toolkit.initialize(app)
    ```
    """

    app: FastAPI = None
    apis: list[ModelRestApi] = None

    db: sessionmaker[Session] = None
    initialized: bool = False
    config = {}

    _mounted = False

    def __init__(
        self,
        *,
        app: FastAPI | None = None,
        config_file: str | None = None,
        user_manager: Type[UserManager] | None = None,
        cookie_transport: CookieTransport | None = None,
        bearer_transport: BearerTransport | None = None,
        cookie_backend: AuthenticationBackend | None = None,
        jwt_backend: AuthenticationBackend | None = None,
        authenticator: Authenticator | None = None,
        fast_api_users: FastAPIUsers[User, int] | None = None,
        password_helper: PasswordHelperProtocol | None = None,
        with_session: bool = False,
    ) -> None:
        """
        Initialize the FastAPI extension.

        Args:
            app (FastAPI | None, optional): The FastAPI application instance. Defaults to None.
            config_file (str | None, optional): The path to the configuration file. Defaults to None.
            user_manager (Type[UserManager] | None, optional): Set this to override default user manager class. Defaults to None.
            cookie_transport (CookieTransport | None, optional): Set this to override default cookie transport instance. Defaults to None.
            bearer_transport (BearerTransport | None, optional): Set this to override default bearer transport instance. Defaults to None.
            cookie_backend (AuthenticationBackend | None, optional): Set this to override default cookie backend instance. Defaults to None.
            jwt_backend (AuthenticationBackend | None, optional): Set this to override default jwt backend instance. Defaults to None.
            authenticator (Authenticator | None, optional): Set this to override default authenticator instance. Defaults to None.
            fast_api_users (FastAPIUsers[User, int] | None, optional): Set this to override default FastAPIUsers instance. Defaults to None.
            password_helper (PasswordHelperProtocol | None, optional): Set this to override default password helper instance. Defaults to None.
            with_session (bool, optional): Flag indicating whether to enable session management. Defaults to False.

        Raises:
            ValueError: If SQLALCHEMY_DATABASE_URI is not set in the configuration.
        """
        if config_file:
            self.read_config_file(config_file)

        # Override default classes
        g.user_manager = user_manager or g.user_manager
        g.cookie_transport = cookie_transport or g.cookie_transport
        g.bearer_transport = bearer_transport or g.bearer_transport
        g.cookie_backend = cookie_backend or g.cookie_backend
        g.jwt_backend = jwt_backend or g.jwt_backend
        g.authenticator = authenticator or g.authenticator
        g.fastapi_users = fast_api_users or g.fastapi_users
        g.password_helper = password_helper or g.password_helper

        if app:
            self.initialize(app)

        if with_session:
            if not self.config.get("SQLALCHEMY_DATABASE_URI"):
                raise ValueError(
                    "SQLALCHEMY_DATABASE_URI is not set in the configuration"
                )
            engine = create_engine(self.config.get("SQLALCHEMY_DATABASE_URI"))
            self.db = sessionmaker(bind=engine)

    def initialize(self, app: FastAPI) -> None:
        """
        Initializes the FastAPI application.

        Args:
            app (FastAPI): The FastAPI application instance.

        Returns:
            None
        """
        if self.initialized:
            return

        self.initialized = True
        self.app = app
        self.apis = []

        # Add the APIs
        self._init_info_api()
        self._init_auth_api()
        self._init_users_api()
        self._init_roles_api()
        self._init_permissions_api()
        self._init_apis_api()
        self._init_permission_apis_api()

        # Add the JS manifest route
        self._init_js_manifest()

    def add_api(self, api: ModelRestApi) -> None:
        """
        Adds the specified API to the FastAPI application.

        Parameters:
        - api (ModelRestApi): The API to be added.

        Returns:
        - None

        Raises:
        - ValueError: If the API is added after the `mount()` method is called.
        """
        if self._mounted:
            raise ValueError(
                "API Mounted after mount() was called, please add APIs before calling mount()"
            )

        api = api if isinstance(api, ModelRestApi) else api()
        self.apis.append(api)
        self.app.include_router(api.router)
        api.toolkit = self

    def total_permissions(self) -> list[str]:
        """
        Returns the total list of permissions required by all APIs.

        Returns:
        - list[str]: The total list of permissions.
        """
        permissions = []
        for api in self.apis:
            permissions.extend(getattr(api, "permissions", []))
        return list(set(permissions))

    def read_config_file(self, config_file: str):
        """
        Reads a configuration file and sets the `config` attribute with the variables defined in the file.

        It will also set the `SECRET_KEY` in the global `g` object if it is defined in the configuration file.

        Args:
            config_file (str): The path to the configuration file.

        Returns:
            None
        """
        spec = importlib.util.spec_from_file_location("config", config_file)
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)

        # Get the dictionary of variables in the module
        self.config = {
            key: value
            for key, value in config_module.__dict__.items()
            if not key.startswith("__")
        }

        self._post_read_config()

    def mount(self):
        """
        Mounts the static and template folders specified in the configuration.

        PLEASE ONLY RUN THIS AFTER ALL APIS HAVE BEEN ADDED.
        """
        if self._mounted:
            return

        self._mounted = True
        self._mount_static_folder()
        self._mount_template_folder()

    def connect_to_database(self):
        """
        Connects to the database using the configured SQLAlchemy database URI.

        This method initializes the database session maker with the SQLAlchemy
        database URI specified in the configuration. If no URI is found in the
        configuration, the default URI is used.

        Returns:
            None
        """
        session_manager.init_db(
            self.config.get(
                "SQLALCHEMY_DATABASE_URI_ASYNC",
                DEFAULT_SQLALCHEMY_DATABASE_URI_ASYNC,
            )
        )

    async def init_database(self):
        """
        Initializes the database by inserting permissions, APIs, roles, and their relationships.

        The initialization process is as follows:
        1. Inserts permissions into the database.
        2. Inserts APIs into the database.
        3. Inserts roles into the database.
        4. Inserts the relationship between permissions and APIs into the database.
        5. Inserts the relationship between permissions, APIs, and roles into the database.

        Returns:
            None
        """
        async with session_manager.session() as db:
            logger.info("INITIALIZING DATABASE")
            await self._insert_permissions(db)
            await self._insert_apis(db)
            await self._insert_roles(db)
            await self._associate_permission_with_api(db)
            await self._associate_permission_api_with_role(db)

    async def _insert_permissions(self, db: AsyncSession):
        new_permissions = self.total_permissions()
        stmt = select(Permission).where(Permission.name.in_(new_permissions))
        result = await db.execute(stmt)
        existing_permissions = [
            permission.name for permission in result.scalars().all()
        ]
        if len(new_permissions) == len(existing_permissions):
            return

        permission_objs = [
            Permission(name=permission)
            for permission in new_permissions
            if permission not in existing_permissions
        ]
        for permission in permission_objs:
            logger.info(f"ADDING PERMISSION {permission}")
            db.add(permission)
        await db.commit()

    async def _insert_apis(self, db: AsyncSession):
        new_apis = [api.__class__.__name__ for api in self.apis]
        stmt = select(Api).where(Api.name.in_(new_apis))
        result = await db.execute(stmt)
        existing_apis = [api.name for api in result.scalars().all()]
        if len(new_apis) == len(existing_apis):
            return

        api_objs = [Api(name=api) for api in new_apis if api not in existing_apis]
        for api in api_objs:
            logger.info(f"ADDING API {api}")
            db.add(api)
        await db.commit()

    async def _insert_roles(self, db: AsyncSession):
        new_roles = DEFAULT_ROLES
        stmt = select(Role).where(Role.name.in_(new_roles))
        result = await db.execute(stmt)
        existing_roles = [role.name for role in result.scalars().all()]
        if len(new_roles) == len(existing_roles):
            return

        role_objs = [
            Role(name=role) for role in new_roles if role not in existing_roles
        ]
        for role in role_objs:
            logger.info(f"ADDING ROLE {role}")
            db.add(role)
        await db.commit()

    async def _associate_permission_with_api(self, db: AsyncSession):
        for api in self.apis:
            new_permissions = getattr(api, "permissions", [])
            if not new_permissions:
                continue

            # Get the api object
            stmt = select(Api).where(Api.name == api.__class__.__name__)
            result = await db.execute(stmt)
            api_obj = result.scalars().first()

            if not api_obj:
                raise ValueError(f"API {api.__class__.__name__} not found")

            stmt = select(Permission).where(
                and_(
                    Permission.name.in_(new_permissions),
                    ~Permission.id.in_([p.permission_id for p in api_obj.permissions]),
                )
            )
            result = await db.execute(stmt)
            new_permissions = result.scalars().all()

            if not new_permissions:
                continue

            for permission in new_permissions:
                stmt = insert(PermissionApi).values(
                    permission_id=permission.id, api_id=api_obj.id
                )
                await db.execute(stmt)
                logger.info(f"ASSOCIATING PERMISSION {permission} WITH API {api_obj}")
            await db.commit()

    async def _associate_permission_api_with_role(self, db: AsyncSession):
        # Get admin role
        stmt = select(Role).where(Role.name == ADMIN_ROLE)
        result = await db.execute(stmt)
        admin_role = result.scalars().first()

        if admin_role:
            # Get list of permission-api.assoc_permission_api_id of the admin role
            stmt = select(PermissionApi).where(
                ~PermissionApi.roles.contains(admin_role)
            )
            result = await db.execute(stmt)
            existing_assoc_permission_api_roles = result.scalars().all()

            # Add admin role to all permission-api objects
            for permission_api in existing_assoc_permission_api_roles:
                permission_api.roles.append(admin_role)
                logger.info(
                    f"ASSOCIATING {admin_role} WITH PERMISSION-API {permission_api}"
                )
            await db.commit()

        # Read config based roles
        roles_dict = self.config.get("ROLES") or self.config.get("FAB_ROLES", {})

        for role_name, role_permissions in roles_dict.items():
            stmt = select(Role).where(Role.name == role_name)
            result = await db.execute(stmt)
            role = result.scalars().first()

            if not role:
                role = Role(name=role_name)
                db.add(role)
                logger.info(f"ADDING ROLE {role}")

            for apis, permissions in role_permissions:
                api_names = apis.split("|")
                permission_names = permissions.split("|")

                stmt = (
                    select(PermissionApi)
                    .where(
                        and_(
                            Api.name.in_(api_names),
                            Permission.name.in_(permission_names),
                        )
                    )
                    .join(Permission)
                    .join(Api)
                    .options(selectinload(PermissionApi.roles))
                )
                result = await db.execute(stmt)
                permission_apis = result.scalars().all()

                for permission_api in permission_apis:
                    if role not in permission_api.roles:
                        permission_api.roles.append(role)
                        logger.info(
                            f"ASSOCIATING {role} WITH PERMISSION-API {permission_api}"
                        )

                await db.commit()

    def _post_read_config(self):
        """
        Function to be called after setting the configuration.

        - Sets the secret key in the global `g` object if it exists in the configuration.
        - Sets the OAuth clients in the global `g` object if it exists in the configuration.
        - Sets the OAuth redirect URI in the global `g` object if it exists in the configuration.

        Returns:
            None
        """
        secret_key = self.config.get("SECRET_KEY")
        if secret_key:
            g.secret_key = secret_key

        g.oauth_clients = self.config.get("OAUTH_CLIENTS") or self.config.get(
            "OAUTH_PROVIDERS", []
        )
        g.oauth_redirect_uri = self.config.get("OAUTH_REDIRECT_URI")

    def _mount_static_folder(self):
        """
        Mounts the static folder specified in the configuration.

        Returns:
            None
        """
        # If the folder does not exist, create it
        os.makedirs(
            self.config.get("STATIC_FOLDER", DEFAULT_STATIC_FOLDER), exist_ok=True
        )

        static_folder = self.config.get("STATIC_FOLDER", DEFAULT_STATIC_FOLDER)
        self.app.mount("/static", StaticFiles(directory=static_folder), name="static")

    def _mount_template_folder(self):
        """
        Mounts the template folder specified in the configuration.

        Returns:
            None
        """
        # If the folder does not exist, create it
        os.makedirs(
            self.config.get("TEMPLATE_FOLDER", DEFAULT_TEMPLATE_FOLDER), exist_ok=True
        )

        templates = Jinja2Templates(
            directory=self.config.get("TEMPLATE_FOLDER", DEFAULT_TEMPLATE_FOLDER)
        )

        @self.app.get("/{full_path:path}", response_class=HTMLResponse)
        def index(request: Request):
            try:
                return templates.TemplateResponse(
                    request=request,
                    name="index.html",
                    context={"base_path": self.config.get("BASE_PATH", "/")},
                )
            except TemplateNotFound:
                raise HTTPException(status_code=404, detail="Not Found")

    """
    -----------------------------------------
         INIT FUNCTIONS
    -----------------------------------------
    """

    def _init_info_api(self):
        self.add_api(InfoApi)

    def _init_auth_api(self):
        self.add_api(AuthApi)

    def _init_users_api(self):
        self.add_api(UsersApi)

    def _init_roles_api(self):
        self.add_api(RolesApi)

    def _init_permissions_api(self):
        self.add_api(PermissionsApi)

    def _init_apis_api(self):
        self.add_api(ViewsMenusApi)

    def _init_permission_apis_api(self):
        self.add_api(PermissionViewApi)

    def _init_js_manifest(self):
        @self.app.get("/server-config.js", response_class=StreamingResponse)
        def js_manifest():
            env = Environment(autoescape=select_autoescape(["html", "xml"]))
            template_string = "window.fab_react_config = {{ react_vars |tojson }}"
            template = env.from_string(template_string)
            rendered_string = template.render(
                react_vars=json.dumps(self.config.get("FAB_REACT_CONFIG", {}))
            )
            content = rendered_string.encode("utf-8")
            scriptfile = io.BytesIO(content)
            return StreamingResponse(
                scriptfile,
                media_type="application/javascript",
            )
