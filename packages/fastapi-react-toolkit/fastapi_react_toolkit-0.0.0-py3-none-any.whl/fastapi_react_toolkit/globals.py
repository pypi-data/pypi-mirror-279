from .auth import AuthConfigurator
from .const import *
from .models import User


class G(AuthConfigurator):
    """
    Represents the global configuration for the application.

    This global configuration subclassing AuthConfigurator, so that the authentication can be configured from outside

    Attributes:
        user (User | None): The currently authenticated user, if any.
        oauth_clients (list): A list of OAuth clients.
        oauth_redirect_uri (str | None): The redirect URI for OAuth authentication, if any.
    """

    user: User | None = None
    oauth_clients = []
    oauth_redirect_uri: str | None = None


g = G()
