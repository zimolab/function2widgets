import os.path
import warnings
from typing import Any, Optional


class NotRegisteredError(Exception):
    pass


class AlreadyRegisteredError(Exception):
    pass


def safe_pop(target: dict, key: str, *more_keys: str):
    if not more_keys:
        if key in target:
            target.pop(key)
        return target

    all_keys = [key, *more_keys]
    for k in all_keys:
        if k in target:
            target.pop(k)
    return target


def remove_tuple_element(t: tuple, ele: Any) -> tuple:
    tmp = [e for e in t if e != ele]
    return tuple(tmp)


def safe_read_file(path: str, encoding: str = "utf-8") -> Optional[str]:
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except BaseException as e:
        warnings.warn(f"Failed to read file {path}: {e}")
        return None


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    else:
        return text


def remove_suffix(text: str, suffix: str) -> str:
    if text.endswith(suffix):
        return text[: -len(suffix)]
    else:
        return text
