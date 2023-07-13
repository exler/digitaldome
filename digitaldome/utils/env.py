import os


def get_env_str(key: str, default: str | None = None) -> str | None:
    return os.environ.get(key, default)


def get_env_int(key: str, default: int | None = None) -> int | None:
    value = os.environ.get(key, default)
    if value is None:
        return None

    try:
        return int(value)
    except TypeError:
        return None


def get_env_float(key: str, default: float | None = None) -> float | None:
    value = os.environ.get(key, default)
    if value is None:
        return None

    try:
        return float(value)
    except TypeError:
        return None


def get_env_list(key: str, default: list[str] = []) -> list[str]:
    value = os.environ.get(key, None)
    if value is None:
        return default

    return value.split(",")


def get_env_bool(key: str, default: bool = False) -> bool:
    value = os.environ.get(key)
    if value in ["1", "True", "true"]:
        return True
    elif value in ["0", "False", "false"]:
        return False
    return default
