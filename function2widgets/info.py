import dataclasses
import warnings
from typing import List, Optional, Dict, Any

from docstring_parser import Docstring, DocstringParam


@dataclasses.dataclass
class FunctionInfo(object):
    name: str
    description: str
    parameters: List["ParameterInfo"]


@dataclasses.dataclass
class ParameterInfo(object):
    name: str
    default: Any
    typename: str
    type_extras: Optional[List[str]] = None
    description: Optional[str] = None
    widget: Optional["ParameterWidgetInfo"] = None


@dataclasses.dataclass
class ParameterWidgetInfo(object):
    widget_class: str
    widget_args: Dict[str, Any]

    def update(self, new_configs: Dict[str, Any]):
        widget_args = new_configs["widget_args"]
        if isinstance(widget_args, dict) and "parameter_name" in widget_args:
            if widget_args["parameter_name"] == self.widget_args["parameter_name"]:
                return
            raise ValueError("parameter_name can not be changed")

        placeholder = object()
        for key, new_value in new_configs.items():
            if new_value is None:
                continue
            if key.startswith("_"):
                continue
            if key not in self.__annotations__:
                continue
            if key == "widget_args":
                self.update_widget_args(new_value)
                continue

            old_value = getattr(self, key, placeholder)
            if old_value is placeholder:
                continue

            expected_type = self.__annotations__[key]
            if type(new_value) is expected_type:
                setattr(self, key, new_value)
            else:
                warnings.warn(
                    f"unexpected type for field '{key}': expected {expected_type}, got{type(new_value)}"
                )

    def update_widget_args(self, new_args: dict):
        if not isinstance(new_args, dict):
            return
        for key, value in new_args.items():
            self.widget_args[key] = value

    def update_with_flattened_dict(self, new_configs: dict):
        structured_dict = self._flattened_to_structured(new_configs)
        self.update(structured_dict)

    @classmethod
    def _flattened_to_structured(cls, flattened_dict: dict) -> dict:
        result = {}
        widget_args = {}
        for key, value in flattened_dict.items():
            if key == "widget_args":
                # widget_args
                if isinstance(value, dict):
                    widget_args.update(value)
                else:
                    widget_args[key] = value
                continue

            if key not in cls.__annotations__:
                widget_args[key] = value
                continue

            expected_type = cls.__annotations__[key]
            if type(value) is not expected_type:
                # 若为已定义的字段，但类型不匹配，则警告
                warnings.warn(
                    f"unexpected type for field '{key}': expected {expected_type}, got {type(value)}"
                )
                continue
            else:
                # 已定义的字段，且类型匹配，则收集该字段
                result[key] = value

        result["widget_args"] = widget_args
        return result


@dataclasses.dataclass
class FunctionDocstringInfo(object):
    docstring_text: str
    docstring_obj: Docstring
    widget_configs: Dict[str, Dict[str, Any]]

    def _find_param(self, param_name: str) -> Optional[DocstringParam]:
        for param in self.docstring_obj.params:
            if param.arg_name == param_name:
                return param
        return None

    def get_function_description(self) -> str:
        desc = self.docstring_obj.description or ""
        return desc.strip()

    def has_parameter(self, param_name: str):
        return self._find_param(param_name) is not None

    def get_parameter_description(self, param_name: str) -> Optional[str]:
        param = self._find_param(param_name)
        if param is None:
            return None
        return param.description.strip()

    def get_parameter_default(self, param_name: str) -> Any:
        param = self._find_param(param_name)
        if param is None:
            return None
        return param.default

    def get_parameter_typename(self, param_name: str) -> Optional[str]:
        param = self._find_param(param_name)
        if param is None:
            return None
        return param.type_name

    def get_widget_configs(self, param_name: str) -> Optional[Dict[str, Any]]:
        if param_name not in self.widget_configs:
            return None
        return self.widget_configs[param_name]
