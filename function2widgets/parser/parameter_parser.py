import inspect
import typing
from typing import Optional, List, Any

from function2widgets.common import parse_type_info
from function2widgets.info import ParameterInfo

TYPE_FOR_VARARGS = list.__name__
TYPE_FOR_KWARGS = dict.__name__


BASIC_TYPES = {
    int: "int",
    float: "float",
    str: "str",
    bool: "bool",
    list: "list",
    tuple: "tuple",
    dict: "dict",
}

BASIC_TYPING_TYPES = {
    # "typing.Any": "any"
    str(typing.Any): "any",
    # "typing.AnyStr": "str"
    str(typing.AnyStr): "str",
    str(typing.Dict): "dict",
    str(typing.OrderedDict): "dict",
    str(typing.MutableMapping): "dict",
    str(typing.Iterable): "list",
    str(typing.List): "list",
    str(typing.Sequence): "list",
    str(typing.MutableSequence): "list",
    str(typing.Tuple): "tuple",
    str(typing.Union): str(typing.Union),
    str(typing.Optional): str(typing.Optional),
    str(typing.Literal): str(typing.Literal),
}


class ParameterInfoParser(object):
    def __init__(self):
        pass

    def parse(self, param_obj: inspect.Parameter) -> Optional[ParameterInfo]:
        param_type, type_extras = self._parse_type_info(param_obj=param_obj)
        param_default = self._parse_default(param_obj=param_obj)
        return ParameterInfo(
            name=param_obj.name,
            typename=param_type,
            type_extras=type_extras,
            default=param_default,
            description=None,
            widget=None,
        )

    @staticmethod
    def _parse_default(param_obj: inspect.Parameter) -> Any:
        if param_obj.default is inspect.Parameter.empty:
            return inspect.Parameter.empty
        return param_obj.default

    @staticmethod
    def _parse_type_info(
        param_obj: inspect.Parameter,
    ) -> (Optional[str], Optional[List[str]]):
        if param_obj.kind == inspect.Parameter.POSITIONAL_ONLY:
            raise TypeError(
                f"positional only parameter is not supported: '{param_obj.name}'"
            )
        # positional var
        if param_obj.kind == inspect.Parameter.VAR_POSITIONAL:
            return TYPE_FOR_VARARGS, None
        # keyword var
        if param_obj.kind == inspect.Parameter.VAR_KEYWORD:
            return TYPE_FOR_KWARGS, None
        # no type annotation
        if (
            param_obj.annotation is None
            or param_obj.annotation is inspect.Parameter.empty
        ):
            return None, None
        typename: str = BASIC_TYPES.get(param_obj.annotation, None)
        if typename is not None:
            return typename, None

        annotation_str = str(param_obj.annotation)
        typename, type_extra = parse_type_info(annotation_str=annotation_str)
        typename = BASIC_TYPING_TYPES.get(typename, None)
        if typename is not None:
            return typename, type_extra

        if inspect.isclass(param_obj.annotation):
            return param_obj.annotation.__name__, None
        return annotation_str, None
