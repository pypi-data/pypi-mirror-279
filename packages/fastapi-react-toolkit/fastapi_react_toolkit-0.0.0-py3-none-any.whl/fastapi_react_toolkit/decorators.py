from .const import PERMISSION_PREFIX


def permission_name(cls, name):
    if name not in cls.permissions:
        cls.permissions.append(f"{PERMISSION_PREFIX}{name}")

    def decorator(func):
        func._permission_name = name
        return func

    return decorator
