import dataclasses
import json
from typing import Any, Optional, cast

from PyQt6.QtWidgets import QWidget, QMessageBox

from function2widgets.common import remove_tuple_element
from function2widgets.widget import InvalidValueError
from function2widgets.widgets._sourcecodeedit import DEFAULT_CONFIGS
from .base import BaseCodeEditorDialog, BaseCodeEditor, BaseCodeEditorArgs

_NoneType = type(None)
JsonTopLevelTypes = (dict, list, tuple, int, str, float, bool, _NoneType)


class JsonEditorDialog(BaseCodeEditorDialog):
    def __init__(
        self,
        top_level_types: tuple,
        configs: dict = None,
        window_title: str = None,
        parent=None,
    ):
        self._current_value = None
        self._top_level_types = top_level_types

        super().__init__(configs=configs, window_title=window_title, parent=parent)

    def set_value(self, value: Any, indent=4, ensure_ascii=False, *args, **kwargs):
        if not isinstance(value, self._top_level_types):
            raise InvalidValueError(
                self.tr(
                    f"value '{value}' is not  one of the following types: {self._top_level_types}"
                )
            )

        try:
            json_str = json.dumps(
                value, indent=indent, ensure_ascii=ensure_ascii, *args, **kwargs
            )
        except BaseException as e:
            raise InvalidValueError() from e
        self._current_value = value
        self._code_edit.setText(json_str)

    def get_value(self, *args, **kwargs) -> Any:
        text = self._code_edit.text()
        try:
            obj = json.loads(text, *args, **kwargs)
        except BaseException as e:
            raise ValueError(f"json deserialization error: {e}")
        if not isinstance(obj, self._top_level_types):
            raise ValueError(
                f"current source is not one of the following types: {self._top_level_types}"
            )
        self._current_value = obj
        return obj

    @property
    def current_value(self) -> Any:
        return self._current_value

    def on_confirm(self):
        try:
            self.get_value()
        except BaseException as e:
            QMessageBox.critical(self, self.tr("Error"), str(e))
            return
        else:
            self.accept()


@dataclasses.dataclass(frozen=True)
class JsonEditorArgs(BaseCodeEditorArgs):
    parameter_name: str
    default: Any = ""
    configs: dict = dataclasses.field(default_factory=DEFAULT_CONFIGS.copy)
    top_level_types: tuple = JsonTopLevelTypes


class JsonEditor(BaseCodeEditor):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = JsonEditorArgs

    def __init__(self, args: JsonEditorArgs, parent: Optional[QWidget] = None):
        configs = args.configs
        if not isinstance(configs, dict):
            configs = DEFAULT_CONFIGS.copy()
        configs["Lexer"] = "JSON"
        default = args.default
        top_level_types = args.top_level_types

        if default is not None:
            top_level_types = remove_tuple_element(top_level_types, _NoneType)

        if not isinstance(default, top_level_types):
            raise ValueError(
                f"default value '{default}' is not one of the following types: {top_level_types}"
            )

        args = dataclasses.replace(
            args, configs=configs, top_level_types=top_level_types
        )

        super().__init__(args=args, parent=parent)

    @property
    def _args(self) -> JsonEditorArgs:
        return cast(JsonEditorArgs, super()._args)

    def source_code_dialog(self) -> JsonEditorDialog:
        top_level_types = self._args.top_level_types
        configs = self._args.configs
        window_title = self._args.window_title
        dialog = JsonEditorDialog(
            top_level_types=top_level_types,
            configs=configs,
            window_title=window_title,
            parent=self,
        )
        dialog.set_value(self._current_value)
        return dialog

    def fetch_result_from_dialog(self, dialog: JsonEditorDialog):
        return dialog.current_value
