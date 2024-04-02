import ast
import logging
import os.path
import re
import warnings
from datetime import datetime
from typing import Any, Optional, List, Dict

import tomli
from PyQt6.QtCore import QDateTime, QDate, QTime

TYPING_ANNOTATION_PATTERN = re.compile(r"^(typing\..+?)(\[.+])*$")


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


def safe_eval(literal: str) -> str:
    literal = literal.strip()
    try:
        return str(ast.literal_eval(literal))
    except BaseException as e:
        # warnings.warn(f"failed to eval {literal}: {e}")
        logging.debug(f"failed to eval {literal}: {e}, return as is instead")
        return str(literal)


def load_toml(toml_str: str, error_on_fail: bool = True) -> Dict[str, Any]:
    try:
        return tomli.loads(toml_str)
    except BaseException as e:
        if error_on_fail:
            raise e
        return {}


def parse_type_info(annotation_str: str) -> (str, Optional[List[str]]):
    annotation_str = annotation_str.strip()
    result = re.match(TYPING_ANNOTATION_PATTERN, annotation_str)
    if not result:
        return annotation_str, None
    typename = result.group(1).strip()
    if result.group(2):
        type_extras = result.group(2).strip()
        type_extras = remove_prefix(type_extras, "[")
        type_extras = remove_suffix(type_extras, "]")
        type_extras = type_extras.strip()
        type_extras = [safe_eval(x) for x in type_extras.split(",")]
    else:
        type_extras = None
    return typename, type_extras


def to_datetime(datetime_str: str, datetime_format: str) -> QDateTime:
    return QDateTime.fromString(datetime_str, datetime_format)


def to_date(date_str: str, date_format: str) -> QDate:
    return QDate.fromString(date_str, date_format)


def to_time(time_str: str, time_format: str) -> QTime:
    return QTime.fromString(time_str, time_format)
