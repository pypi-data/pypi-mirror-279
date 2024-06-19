import logging

USER_TABLE = "ab_user"
ROLE_TABLE = "ab_role"
PERMISSION_TABLE = "ab_permission"
API_TABLE = "ab_view_menu"
PERMISSION_API_TABLE = "ab_permission_view"
ASSOC_PERMISSION_API_ROLE_TABLE = "ab_permission_view_role"
ASSOC_USER_ROLE_TABLE = "ab_user_role"

PERMISSION_PREFIX = "can_"
ADMIN_ROLE = "Admin"
PUBLIC_ROLE = "Public"
DEFAULT_ROLES = [ADMIN_ROLE, PUBLIC_ROLE]

DEFAULT_SQLALCHEMY_DATABASE_URI_ASYNC = "sqlite+aiosqlite:///./app.db"
DEFAULT_TOKEN_URL = "/api/v1/auth/jwt/login"
DEFAULT_SECRET = "SUPERSECRET"
DEFAULT_COOKIE_NAME = "dataTactics"
DEFAULT_STATIC_FOLDER = "static"
DEFAULT_TEMPLATE_FOLDER = "templates"

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("DT_FASTAPI")
