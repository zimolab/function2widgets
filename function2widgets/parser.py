import ast
import dataclasses
import inspect
import re
import typing
import warnings
from typing import Any, Callable, List, Optional, Dict

import docstring_parser
import tomli
from PyQt6.QtWidgets import QApplication
from docstring_parser import Docstring, DocstringParam

from function2widgets.common import safe_pop, remove_prefix, remove_suffix
from function2widgets.description import (
    FunctionDescription,
    WidgetDescription,
    ParameterDescription,
)
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
)

TYPING_ANNOTATION_PATTERN = re.compile(r"^(typing\..+?)(\[.+])*$")


def dict_to_widget_descriptions(raw: Dict[str, Any]) -> Optional[WidgetDescription]:
    if not raw:
        return None
    # 检查WidgetDescription.type字段
    if "type" not in raw:
        warnings.warn(QApplication.tr(f"invalid widget description: {raw}"))
        return None
    widget_type = raw["type"]
    # 获取WidgetDescription.label字段
    label = raw.get("label", "")
    # 获取WidgetDescription.docstring字段
    docstring = raw.get("docstring", "")
    # 获取WidgetDescription.show_label字段
    show_label = raw.get("show_label", True)
    # 获取WidgetDescription.show_docstring字段
    show_docstring = raw.get("show_docstring", True)
    # 剔除以上字段，剩余字段作为init_args
    init_args = safe_pop(
        raw, "type", "label", "docstring", "show_label", "show_docstring"
    )
    return WidgetDescription(
        type=widget_type,
        label=label,
        docstring=docstring,
        show_label=show_label,
        show_docstring=show_docstring,
        init_args=init_args,
    )


def parse_toml_metadata(metadata: str) -> dict:
    try:
        return tomli.loads(metadata)
    except BaseException as e:
        warnings.warn(QApplication.tr(f"failed to parse metadata: {e}"))
        return {}


def normalize_typing_annotation_str(
    typing_annotation_str: str,
) -> (str, Optional[List[str]]):
    typing_annotation_str = typing_annotation_str.strip()
    match_result = re.match(TYPING_ANNOTATION_PATTERN, typing_annotation_str)
    if not match_result:
        return typing_annotation_str, None
    basic_typing_name = match_result.group(1)
    if match_result.group(2):

        type_extras_str = match_result.group(2).strip()
        type_extras_str = remove_prefix(type_extras_str, "[")
        type_extras_str = remove_suffix(type_extras_str, "]")
        type_extras = [ast.literal_eval(x.strip()) for x in type_extras_str.split(",")]
    else:
        type_extras = None
    return basic_typing_name, type_extras


class _DocstringInfo(object):
    def __init__(
        self,
        docstring_text: str,
        docstring_obj: Docstring,
        param_widgets_description: Dict[str, WidgetDescription],
    ):
        self._docstring_text = docstring_text
        self._docstring_obj = docstring_obj
        self._param_widgets_description = param_widgets_description

    def _find_param(self, param_name: str) -> Optional[DocstringParam]:
        for param in self._docstring_obj.params:
            if param.arg_name == param_name:
                return param

    def get_func_description(self) -> str:
        desc = self.get_short_description() + "\n" + self.get_long_description()
        return desc.strip()

    def get_short_description(self) -> str:
        return self._docstring_obj.short_description or ""

    def get_long_description(self) -> str:
        return self._docstring_obj.long_description or ""

    def has_parameter(self, param_name: str) -> bool:
        return self._find_param(param_name) is not None

    def get_param_description(
        self, param_name: str, fallback: str = None
    ) -> Optional[str]:
        doc_param = self._find_param(param_name)
        if not doc_param:
            return fallback
        return doc_param.description

    def get_param_typename(
        self, param_name: str, fallback: str = None
    ) -> Optional[str]:
        doc_param = self._find_param(param_name)
        if not doc_param:
            return fallback
        return doc_param.type_name

    def get_param_default(self, param_name: str, fallback: Any = None) -> str:
        doc_param = self._find_param(param_name)
        if not doc_param:
            return fallback
        return doc_param.default

    def has_param_widget(self, param_name: str) -> bool:
        return param_name in self._param_widgets_description

    def get_param_widget(
        self, param_name: str, default: WidgetDescription = None
    ) -> Optional[WidgetDescription]:
        return self._param_widgets_description.get(param_name, default)

    def get_raw_docstring(self) -> str:
        return self._docstring_text


class DocstringInfoParser(object):
    WIDGETS_BLOCK_START_TAG = "@begin"
    WIDGETS_BLOCK_END_TAG = "@end"

    def __init__(
        self,
        metadata_start_tag: str = WIDGETS_BLOCK_START_TAG,
        metadata_end_tag: str = WIDGETS_BLOCK_END_TAG,
        metadata_parser: Callable[[str], Optional[dict]] = parse_toml_metadata,
    ):
        self._metadata_pattern = (
            rf"^(\s*{metadata_start_tag}\s*(.*\n.+)^\s*{metadata_end_tag}\s*\n)"
        )
        self._metadata_parser = metadata_parser

    def _extract_metadata_from_docstring(self, docstring: str) -> str:
        match_result = re.search(
            self._metadata_pattern, docstring, re.MULTILINE | re.DOTALL
        )
        if match_result:
            return match_result.group(2)
        return ""

    def _remove_metadata_in_docstring(self, docstring: str):
        match_result = re.search(
            self._metadata_pattern, docstring, re.MULTILINE | re.DOTALL
        )
        if match_result:
            return re.sub(
                self._metadata_pattern, "", docstring, flags=re.MULTILINE | re.DOTALL
            )
        return docstring

    # noinspection PyMethodMayBeStatic
    def _process_metadata(self, metadata: dict) -> Dict[str, WidgetDescription]:
        param_widgets_descriptions = {}
        for param_name, param_widget_dict in metadata.items():
            if not isinstance(param_widget_dict, dict) or not param_widget_dict:
                continue
            widget_description = dict_to_widget_descriptions(param_widget_dict)
            if not widget_description:
                continue
            param_widgets_descriptions[param_name] = widget_description

        return param_widgets_descriptions

    # noinspection PyMethodMayBeStatic
    def _parse_docstring(self, docstring: str) -> Docstring:
        try:
            return docstring_parser.parse(docstring)
        except BaseException as e:
            warnings.warn(QApplication.tr(f"docstring parsing error: {e}"))
            return Docstring()

    def parse(self, docstring: str) -> _DocstringInfo:

        metadata_in_docstring = self._extract_metadata_from_docstring(docstring).strip()
        docstring_without_metadata = self._remove_metadata_in_docstring(
            docstring
        ).strip()

        if not metadata_in_docstring:
            raw_metadata = {}
        else:
            try:
                raw_metadata = self._metadata_parser(metadata_in_docstring)
            except BaseException as e:
                warnings.warn(QApplication.tr(f"metadata parsing error: {e}"))
                raw_metadata = {}
        func_docstring_obj = self._parse_docstring(docstring_without_metadata)
        param_widgets_descriptions = self._process_metadata(raw_metadata)
        return _DocstringInfo(
            docstring_text=docstring_without_metadata,
            docstring_obj=func_docstring_obj,
            param_widgets_description=param_widgets_descriptions,
        )


@dataclasses.dataclass
class _ParameterInfo(object):
    name: str
    typename: Optional[str]
    default: Any
    type_extras: Any = None

    def __str__(self):
        return f"{self.name}={self.default}(type={self.typename}, extras={self.type_extras})"


@dataclasses.dataclass
class _FunctionInfo(object):

    def __init__(self, function_name: str):
        self._function_name: str = function_name
        self._parameters: Dict[str, _ParameterInfo] = {}

    def get_function_name(self) -> str:
        return self._function_name

    @property
    def parameters(self) -> Dict[str, _ParameterInfo]:
        return {**self._parameters}

    def get_parameter(self, param_name: str) -> _ParameterInfo:
        if not self.has_parameter(param_name):
            raise ValueError(QApplication.tr(f"parameter {param_name} not found"))
        return self._parameters[param_name]

    def has_parameter(self, param_name: str) -> bool:
        return param_name in self._parameters

    def get_parameter_names(self) -> List[str]:
        return list(self._parameters.keys())

    def get_parameter_typename(self, param_name: str) -> str:
        if not self.has_parameter(param_name):
            raise ValueError(QApplication.tr(f"parameter {param_name} not found"))
        return self._parameters[param_name].typename

    def get_parameter_default(self, param_name: str) -> Any:
        if not self.has_parameter(param_name):
            raise ValueError(QApplication.tr(f"parameter {param_name} not found"))
        return self._parameters[param_name].default

    def add_parameter(self, param_name: str, func_param: _ParameterInfo):
        self._parameters[param_name] = func_param

    def __str__(self):
        return f"{self._function_name}({', '.join(self._parameters)})"


class FunctionInfoParser(object):
    TYPENAME_FOR_VARARGS = list.__name__
    TYPENAME_FOR_KWARGS = dict.__name__
    DEFAULT_FOR_EMPTY = inspect.Parameter.empty

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
        str(typing.Any): "any",
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

    def _find_typename(self, type_annotation: Any) -> (Optional[str], Any):

        basic_type = self.BASIC_TYPES.get(type_annotation, None)
        if basic_type is not None:
            return basic_type, None

        type_annotation_str = str(type_annotation)
        basic_name, extras = normalize_typing_annotation_str(type_annotation_str)
        typing_type = self.BASIC_TYPING_TYPES.get(basic_name, None)
        if typing_type is not None:
            return typing_type, extras

        if inspect.isclass(type_annotation):
            return type_annotation.__name__, None

        return type_annotation_str, None

    def _param_typename(self, param: inspect.Parameter) -> (Optional[str], Any):
        # 不支持仅通过位置传递的参数
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            raise TypeError(
                QApplication.tr(
                    f"positional only parameter is not supported: '{param.name}'"
                )
            )
        # 可变位置参数
        if param.kind == inspect.Parameter.VAR_POSITIONAL:
            return self.TYPENAME_FOR_VARARGS, None
        # 可变关键字参数
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return self.TYPENAME_FOR_KWARGS, None
        # 未标注参数类型
        if param.annotation is inspect.Parameter.empty:
            return None, None
        typename, extras = self._find_typename(param.annotation)
        return typename, extras

    def _param_default_value(self, param: inspect.Parameter) -> Any:
        if param.default is inspect.Parameter.empty:
            return self.DEFAULT_FOR_EMPTY
        return param.default

    def _parse_parameter_info(
        self, param: inspect.Parameter
    ) -> Optional[_ParameterInfo]:
        param_name = param.name
        param_typename, extras = self._param_typename(param)
        param_default = self._param_default_value(param)
        return _ParameterInfo(
            name=param_name,
            typename=param_typename,
            default=param_default,
            type_extras=extras,
        )

    def parse(self, func, ignore_self_param: bool = True) -> _FunctionInfo:
        func_name = func.__name__
        func_info = _FunctionInfo(function_name=func_name)

        func_signature = inspect.signature(func)
        for param_name in func_signature.parameters:
            if param_name == "self" and ignore_self_param:
                continue
            param = func_signature.parameters[param_name]
            param_info = self._parse_parameter_info(param)
            if not param_info:
                continue
            func_info.add_parameter(param_name, param_info)
        return func_info


class FunctionDescriptionComposer(object):
    TYPENAME_FOR_EMPTY = "any"
    DEFAULT_FOR_EMPTY = None

    DEFAULT_WIDGET_TYPES = {
        bool.__name__: CheckBox.__name__,
        int.__name__: IntLineEdit.__name__,
        float.__name__: FloatLineEdit.__name__,
        str.__name__: LineEdit.__name__,
        list.__name__: ListEditor.__name__,
        tuple.__name__: TupleEditor.__name__,
        dict.__name__: DictEditor.__name__,
        str(typing.Literal): ComboBox.__name__,
        str(typing.Union): JsonEditor.__name__,
        str(typing.Optional): JsonEditor.__name__,
        str(typing.Any): JsonEditor.__name__,
        "any": JsonEditor.__name__,
    }

    DEFAULT_FALLBACK_PARAM_WIDGET = DEFAULT_WIDGET_TYPES["any"]

    def __init__(self, fallback_param_widget_type: str = DEFAULT_FALLBACK_PARAM_WIDGET):
        self._fallback_param_widget = fallback_param_widget_type

    def determine_param_type(
        self, param_info: _ParameterInfo, docstring_info: _DocstringInfo
    ) -> str:
        if param_info.typename is not None:
            return param_info.typename
        typename_in_docstring = docstring_info.get_param_typename(
            param_info.name, self.TYPENAME_FOR_EMPTY
        )
        return typename_in_docstring

    def determine_param_default(
        self, param_info: _ParameterInfo, docstring_info: _DocstringInfo
    ) -> Any:
        if param_info.default is FunctionInfoParser.DEFAULT_FOR_EMPTY:
            return self.DEFAULT_FOR_EMPTY
        if param_info.default is not None:
            return param_info.default
        return docstring_info.get_param_default(param_info.name, self.DEFAULT_FOR_EMPTY)

    # noinspection PyMethodMayBeStatic
    def _make_param_widget_of_type(
        self,
        widget_type: str,
        param_info: _ParameterInfo,
        docstring_info: _DocstringInfo,
        **init_args,
    ) -> WidgetDescription:
        param_docstring = docstring_info.get_param_description(
            param_name=param_info.name, fallback=""
        )
        show_docstring = param_docstring != ""

        # 一些类型需要特定化处理
        if param_info.typename == str(typing.Literal):
            if (
                isinstance(param_info.type_extras, list)
                and len(param_info.type_extras) > 0
            ):
                widget_type = ComboBox.__name__
                init_args["items"] = param_info.type_extras
            else:
                widget_type = ComboBoxEdit.__name__

        widget = WidgetDescription(
            type=widget_type,
            label=param_info.name,
            docstring=param_docstring,
            show_label=True,
            show_docstring=show_docstring,
            init_args=init_args,
        )
        return widget

    def _param_widget_of_type(
        self,
        param_type: str,
        param_info: _ParameterInfo,
        docstring_info: _DocstringInfo,
    ) -> Optional[WidgetDescription]:
        widget_type = self.DEFAULT_WIDGET_TYPES.get(param_type, None)
        if widget_type is None:
            return None
        widget = self._make_param_widget_of_type(
            widget_type=widget_type,
            param_info=param_info,
            docstring_info=docstring_info,
        )
        return widget

    # noinspection PyMethodMayBeStatic
    def _tweak_param_widget(
        self,
        param_widget: WidgetDescription,
        param_info: _ParameterInfo,
        docstring_info: _DocstringInfo,
    ):
        if not param_widget.docstring:
            param_widget.docstring = docstring_info.get_param_description(
                param_info.name, ""
            )

        if not param_widget.label:
            param_widget.label = param_info.name

        if (
            param_widget.type == ComboBox.__name__
            or param_widget.type == ComboBoxEdit.__name__
        ):
            if "items" not in param_widget.init_args and isinstance(
                param_info.type_extras, list
            ):
                param_widget.init_args["items"] = param_info.type_extras

    def determine_param_widget(
        self, param_info: _ParameterInfo, docstring_info: _DocstringInfo
    ) -> WidgetDescription:
        # 如果在docstring中描述了参数的控件，则优先使用该描述
        param_widget = docstring_info.get_param_widget(param_info.name, None)
        if param_widget is not None:
            self._tweak_param_widget(param_widget, param_info, docstring_info)
            return param_widget
        # 否则使用该参数类型的默认控件
        param_widget = self._param_widget_of_type(
            param_info.typename, param_info, docstring_info
        )
        if param_widget is not None:
            return param_widget
        # 如果该参数类型没有定义默认的控件，则使用fallback_param_widget
        return self._make_param_widget_of_type(
            widget_type=self._fallback_param_widget,
            param_info=param_info,
            docstring_info=docstring_info,
        )

    def compose(
        self, func_info: _FunctionInfo, docstring_info: _DocstringInfo
    ) -> FunctionDescription:
        func_description = FunctionDescription(
            name=func_info.get_function_name(),
            docstring=docstring_info.get_func_description(),
        )
        for param_name, param_info in func_info.parameters.items():
            param_typename = self.determine_param_type(param_info, docstring_info)
            param_default = self.determine_param_default(param_info, docstring_info)

            param = ParameterDescription(
                name=param_info.name,
                type=param_typename,
                type_extras=param_info.type_extras or None,
                default=param_default,
                docstring=docstring_info.get_param_description(param_name, None),
                widget=self.determine_param_widget(param_info, docstring_info),
            )
            func_description.parameters.append(param)
        return func_description


class FunctionDescriptionParser(object):
    def __init__(
        self,
        docstring_info_parser: DocstringInfoParser = DocstringInfoParser(),
        func_info_parser: FunctionInfoParser = FunctionInfoParser(),
        func_description_maker: FunctionDescriptionComposer = FunctionDescriptionComposer(),
    ):
        self._docstring_info_parser = docstring_info_parser
        self._func_info_parser = func_info_parser
        self._func_description_maker = func_description_maker

    def parse(
        self, func: Any, parse_class: bool = True, ignore_self_param: bool = True
    ) -> FunctionDescription:
        if not parse_class and inspect.isclass(func):
            raise TypeError(
                QApplication.tr(f"func must be a function or method, but got {func}")
            )

        if inspect.isclass(func):
            # noinspection PyTypeChecker
            func = func.__init__

        if not inspect.isfunction(func) and not inspect.ismethod(func):
            raise TypeError(
                QApplication.tr(f"func must be a function or method, but got {func}")
            )

        func_docstring = self._docstring_info_parser.parse(func.__doc__ or "")
        func_info = self._func_info_parser.parse(func, ignore_self_param)

        return self._func_description_maker.compose(func_info, func_docstring)


def __test_main():
    class Demo(object):
        """this is a demo class

        this class is for demo use
        """

        def __init__(
            self,
            a: int,
            b: str,
            c: list,
            d: dict,
            e: tuple,
            g: list,
            h: dict,
            i: tuple,
            *args,
            **kwargs,
        ):
            """this is init method

            this is an init method and will create an instance of class Demo

            :param a:  this is param a
            :param b:  this is param b
            :param c:
            :param d:
            :param e:
            :param g:
            :param h:
            :param i:
            :param args:
            :param kwargs:

            @begin
            [a]
            type="IntLineEdit"
            placeholder="input a number here"
            @end

            """
            pass

        def func2(
            self,
            labels: typing.Literal["a", "b", "c"],
            path: str,
            opt: typing.Literal["opt1", "opt2", "opt3"] = "opt1",
        ):
            """

            :param opt:
            :param labels:
            :param path: select file
            :return:

            @begin
            [path]
            type="FilePathEdit"
            label="文件路径"
            select_button_text="选择文件"

            [opt]
            type="ComboBoxEdit"

            @end
            """
            pass

    parser = FunctionDescriptionParser()
    # func = parser.parse(Demo)
    # print(func)

    func2 = parser.parse(Demo.func2)
    print(func2)


if __name__ == "__main__":
    __test_main()
