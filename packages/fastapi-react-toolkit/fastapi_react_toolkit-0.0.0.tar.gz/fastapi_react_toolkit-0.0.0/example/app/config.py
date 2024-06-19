import os

from httpx_oauth.clients.google import GoogleOAuth2

basedir = os.path.abspath(os.path.dirname(__file__))

#! AVAILABLE KEYS
# SECRET_KEY
# SQLALCHEMY_DATABASE_URI
# SQLALCHEMY_DATABASE_URI_ASYNC
# OAUTH_PROVIDERS or OAUTH_CLIENTS
# OAUTH_REDIRECT_URI
# FAB_ROLES or ROLES

STATIC_FOLDER = os.path.join(basedir, "app/static")
TEMPLATE_FOLDER = os.path.join(basedir, "app/templates")

# Your App secret key
SECRET_KEY = "hf45hf8578h5n487hv487h474584"

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_DATABASE_URI_ASYNC = "sqlite+aiosqlite:///" + os.path.join(basedir, "app.db")
# SQLALCHEMY_DATABASE_URI = 'mysql://myapp@localhost/myapp'
# SQLALCHEMY_DATABASE_URI = 'postgresql://root:password@localhost/myapp'

google_oauth_client = GoogleOAuth2(
    "client_id",
    "client_secret",
)

OAUTH_PROVIDERS = [google_oauth_client]
OAUTH_REDIRECT_URI = "http://localhost:6006"

# General roles, that everyone should be able to read
GENERAL_READ = [
    "AssetApi|UnitApi",
    "can_info|can_get",
]

FAB_ROLES = {
    "Operator": [GENERAL_READ],
    "Reporter": [GENERAL_READ],
}

# OR to associate the oauth with current account
# OAUTH_PROVIDERS = [(google_oauth_client, True)]