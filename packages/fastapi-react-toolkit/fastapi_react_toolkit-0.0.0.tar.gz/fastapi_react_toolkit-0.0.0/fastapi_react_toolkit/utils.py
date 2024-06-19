from pydantic import BaseModel


def both_are_filled_or_empty(v1: str, v2: str) -> None:
    """
    Checks if both values are either filled or empty.

    Args:
        v1 (str): The first value to check.
        v2 (str): The second value to check.

    Raises:
        ValueError: If one value is filled and the other is empty.

    Returns:
        None
    """
    if bool(v1) != bool(v2):
        raise ValueError("Both values must be filled or empty")


def dump_schema(schema: BaseModel):
    """
    Dump the given schema into a dictionary and remove any nested dictionaries that should be ignored.

    Args:
        schema (BaseModel): The schema to be dumped.

    Returns:
        dict: The dumped schema.
    """
    from .schemas import IgnoredData

    data = schema.model_dump()
    for key in list(data.keys()):
        if isinstance(data[key], dict):
            try:
                IgnoredData.model_validate(data[key], strict=True)
                del data[key]
            except:
                pass
    return data
