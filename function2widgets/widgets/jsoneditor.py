import json
from typing import Any, Optional

from PyQt6.QtWidgets import QWidget, QApplication, QMessageBox

from function2widgets.common import remove_tuple_element
from function2widgets.widget import InvalidValueError
from function2widgets.widgets._sourcecodeedit import DEFAULT_CONFIGS
from function2widgets.widgets.codeeditor import (
    BaseSourceCodeEditor,
    BaseSourceCodeEditDialog,
)

_NoneType = type(None)
JsonTopLevelTypes = (dict, list, tuple, int, str, float, bool, _NoneType)


class JsonEditDialog(BaseSourceCodeEditDialog):
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
            raise InvalidValueError(self.tr(f"json deserialization error: {e}"))
        if not isinstance(obj, self._top_level_types):
            raise InvalidValueError(
                self.tr(
                    f"current source is not one of the following types: {self._top_level_types}"
                )
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


class JsonEditor(BaseSourceCodeEditor):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        top_level_types: tuple = JsonTopLevelTypes,
        default: Any = "",
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):

        if configs is None:
            configs = DEFAULT_CONFIGS.copy()
        configs["Lexer"] = "JSON"

        if default is not None:
            self._top_level_types = remove_tuple_element(top_level_types, _NoneType)
        else:
            self._top_level_types = top_level_types

        if not isinstance(default, self._top_level_types):
            raise InvalidValueError(
                QApplication.tr(
                    f"default value '{default}' is not one of the following types: {self._top_level_types}"
                )
            )

        super().__init__(
            default=default,
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )

    def source_code_dialog(self) -> JsonEditDialog:
        dialog = JsonEditDialog(
            top_level_types=self._top_level_types,
            configs=self._configs,
            window_title=self._window_title,
            parent=self,
        )
        dialog.set_value(self._current_value)
        return dialog

    def fetch_result_from_dialog(self, dialog: JsonEditDialog):
        return dialog.current_value

    def get_value(self, *args, **kwargs) -> Any:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: Any, *args, **kwargs):
        super().set_value(value, *args, **kwargs)
