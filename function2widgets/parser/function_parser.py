import inspect
import typing
from collections import OrderedDict
from datetime import datetime, date, time
from typing import Any

from function2widgets.info import (
    FunctionInfo,
    FunctionDocstringInfo,
    ParameterWidgetInfo,
    ParameterInfo,
)
from function2widgets.parser.docstr_parser import FunctionDocstringParser
from function2widgets.parser.parameter_parser import ParameterInfoParser
from function2widgets.widgets import (
    CheckBox,
    IntLineEdit,
    FloatLineEdit,
    LineEdit,
    ListEditor,
    TupleEditor,
    DictEditor,
    ComboBox,
    JsonEditor,
    ComboBoxEdit,
    DateTimeEdit,
    DateEdit,
    TimeEdit,
)

DEFAULT_WIDGET_TYPES = {
    bool.__name__: CheckBox.__name__,
    int.__name__: IntLineEdit.__name__,
    float.__name__: FloatLineEdit.__name__,
    str.__name__: LineEdit.__name__,
    list.__name__: ListEditor.__name__,
    tuple.__name__: TupleEditor.__name__,
    dict.__name__: DictEditor.__name__,
    datetime.__name__: DateTimeEdit.__name__,
    date.__name__: DateEdit.__name__,
    time.__name__: TimeEdit.__name__,
    str(typing.Union): JsonEditor.__name__,
    str(typing.Optional): JsonEditor.__name__,
    str(typing.Any): JsonEditor.__name__,
    "any": JsonEditor.__name__,
}


TYPENAME_FOR_EMPTY = "any"
DEFAULT_FOR_EMPTY = inspect.Parameter.empty
FALLBACK_WIDGET_TYPE = DEFAULT_WIDGET_TYPES["any"]

DEFAULT_WIDGET_FOR_LITERALS = ComboBox.__name__


class FunctionInfoParser(object):

    def __init__(self):
        self._parameter_parser: ParameterInfoParser = ParameterInfoParser()
        self._func_docstring_parser: FunctionDocstringParser = FunctionDocstringParser()

    def parse(
        self,
        func_obj: Any,
        ignore_self_param: bool = True,
        raw_docstring_as_description: bool = False,
    ) -> FunctionInfo:
        if inspect.isclass(func_obj):
            func_obj = func_obj.__init__

        if not inspect.isfunction(func_obj) and not inspect.ismethod(func_obj):
            raise TypeError(f"'{func_obj}' is not a function or method")

        func_info = self._parse_signature(
            func_obj=func_obj, ignore_self_param=ignore_self_param
        )
        func_docstring_info = self._parse_docstring(func_obj=func_obj)

        func_info = self._merge(func_info, func_docstring_info)

        if not raw_docstring_as_description:
            tmp = func_docstring_info.get_function_description()
            if tmp is not None:
                func_info.description = tmp
        return func_info

    def _merge(
        self, func_info: FunctionInfo, func_docstring_info: FunctionDocstringInfo
    ) -> FunctionInfo:
        for param_info in func_info.parameters:
            param_name = param_info.name
            # determine typename
            if not param_info.typename:
                param_info.typename = func_docstring_info.get_parameter_typename(
                    param_name=param_name
                )
            if not param_info.typename:
                param_info.typename = TYPENAME_FOR_EMPTY

            # determine default value
            if param_info.default is inspect.Parameter.empty:
                param_info.default = DEFAULT_FOR_EMPTY
            if param_info.default is None:
                param_info.default = func_docstring_info.get_parameter_default(
                    param_name
                )

            # determine description
            param_info.description = (
                func_docstring_info.get_parameter_description(param_name) or ""
            )

            # determine widget info
            param_info.widget = self._create_param_widget_info(
                param_info, func_docstring_info
            )
        return func_info

    def _parse_signature(self, func_obj: Any, ignore_self_param: bool) -> FunctionInfo:
        func_info = FunctionInfo(
            name=func_obj.__name__,
            description=func_obj.__doc__,
            parameters=[],
        )
        func_signature = inspect.signature(func_obj)
        for param_name, param_obj in func_signature.parameters.items():
            if param_name == "self" and ignore_self_param:
                continue
            param_info = self._parameter_parser.parse(param_obj=param_obj)
            if param_info is None:
                continue
            func_info.parameters.append(param_info)
        return func_info

    def _parse_docstring(self, func_obj: Any) -> FunctionDocstringInfo:
        raw_docstring_text = func_obj.__doc__ or ""
        return self._func_docstring_parser.parse(raw_docstring_text=raw_docstring_text)

    def _create_param_widget_info(
        self, param_info: ParameterInfo, func_docstring_info: FunctionDocstringInfo
    ) -> ParameterWidgetInfo:
        widget_info = self.make_default_param_widget_info(param_info)
        widget_configs = func_docstring_info.get_widget_configs(param_info.name)
        if widget_configs:
            widget_info.update_with_flattened_dict(widget_configs)

        return widget_info

    @staticmethod
    def make_default_param_widget_info(
        param_info: ParameterInfo,
    ) -> ParameterWidgetInfo:
        widget_class = DEFAULT_WIDGET_TYPES.get(
            param_info.typename, FALLBACK_WIDGET_TYPE
        )

        widget_args = OrderedDict()
        # some spacial processing for particular types
        if param_info.typename == str(typing.Literal):
            if param_info.type_extras:
                widget_class = DEFAULT_WIDGET_FOR_LITERALS
                widget_args["items"] = param_info.type_extras
            else:
                widget_class = ComboBoxEdit.__name__
                widget_args["items"] = []
        # set common args for all widgets
        widget_args["parameter_name"] = param_info.name
        if param_info.default is not DEFAULT_FOR_EMPTY:
            widget_args["default"] = param_info.default
        widget_args["label"] = param_info.name
        widget_args["description"] = param_info.description
        widget_args["stylesheet"] = None
        widget_args["set_default_on_init"] = None
        widget_args["hide_default_widget"] = None
        widget_args["default_widget_text"] = None

        param_widget_info = ParameterWidgetInfo(
            widget_class=widget_class, widget_args=widget_args
        )

        return param_widget_info
