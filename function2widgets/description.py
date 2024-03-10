import dataclasses
import warnings
from typing import Any, OrderedDict


@dataclasses.dataclass
class WidgetDescription(object):
    type: str
    label: str = ""
    docstring: str = ""
    show_label: bool = True
    show_docstring: bool = True
    init_args: dict = dataclasses.field(default_factory=OrderedDict)

    def update(self, new_configs: dict[str, Any]):
        placeholder = object()
        for key, new_value in new_configs.items():
            if new_value is None:
                continue
            if key.startswith("_"):
                continue
            if key not in self.__annotations__:
                continue
            if key == "init_args":
                self.update_init_args(new_value)
                continue
            old_value = getattr(self, key, placeholder)
            if old_value is placeholder:
                continue
            expected_type = self.__annotations__[key]
            if type(new_value) is expected_type:
                setattr(self, key, new_value)
            else:
                warnings.warn(f"unexpected type for field '{key}': expected {expected_type}, got{type(new_value)}")

    def update_init_args(self, new_args: dict):
        if not isinstance(new_args, dict):
            return
        for key, value in new_args.items():
            self.init_args[key] = value

    def update_with_flattened_dict(self, new_configs: dict):
        structured_dict = self._flattened_to_structured(new_configs)
        self.update(structured_dict)

    @classmethod
    def _flattened_to_structured(cls, flattened_dict: dict) -> dict:
        result = {}
        init_args = {}
        for key, value in flattened_dict.items():
            if key == "init_args":
                # init_args需要特殊处理
                if isinstance(value, dict):
                    init_args.update(value)
                else:
                    init_args[key] = value
                continue

            if key not in cls.__annotations__:
                # 非已定义的字段，则作为init_args收集
                init_args[key] = value
                continue

            expected_type = cls.__annotations__[key]
            if type(value) is not expected_type:
                # 若为已定义的字段，但类型不匹配，则警告
                warnings.warn(f"unexpected type for field '{key}': expected {expected_type}, got {type(value)}")
                continue
            else:
                # 已定义的字段，且类型匹配，则收集该字段
                result[key] = value

        result["init_args"] = init_args
        return result


@dataclasses.dataclass
class ParameterDescription(object):
    name: str
    type: str
    type_extras: Any = None
    default: Any = None
    docstring: str | None = None
    widget: WidgetDescription | None = None


@dataclasses.dataclass
class FunctionDescription(object):
    """A description of a function."""
    name: str
    docstring: str
    parameters: list[ParameterDescription] = dataclasses.field(default_factory=list)