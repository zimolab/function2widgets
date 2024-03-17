import abc
import copy
import json
from types import NoneType
from typing import Any

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QDialog,
    QMessageBox,
    QApplication,
    QPlainTextEdit,
)

from function2widgets.common import remove_tuple_element
from function2widgets.widget import InvalidValueError
from function2widgets.widgets._sourcecodeedit import _SourceCodeEdit, DEFAULT_CONFIGS
from function2widgets.widgets.base import CommonParameterWidget

JsonTopLevelTypes = (dict, list, tuple, int, str, float, bool, NoneType)


class BaseSourceCodeEditDialog(QDialog):
    def __init__(self, configs: dict = None, window_title: str = "", parent=None):
        super().__init__(parent)

        self._main_layout = QVBoxLayout(self)

        self._window_title = window_title
        self._code_edit = _SourceCodeEdit(configs=configs, parent=self)

        self._button_cancel = QPushButton(self.tr("Cancel"))
        self._button_confirm = QPushButton(self.tr("Confirm"))

        self.setup_ui()

    def apply_configs(self, configs: dict):
        if not configs:
            return
        self._code_edit.apply_configs(configs)

    # noinspection PyUnresolvedReferences
    def setup_ui(self):
        self.resize(800, 600)
        self.setLayout(self._main_layout)
        self._main_layout.addWidget(self._code_edit)

        button_layout = QHBoxLayout(self)
        button_layout.addSpacerItem(
            QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )
        button_layout.addWidget(self._button_confirm)
        button_layout.addWidget(self._button_cancel)
        self._button_cancel.clicked.connect(self.on_cancel)
        self._button_confirm.clicked.connect(self.on_confirm)

        self.setWindowTitle(self._window_title)
        self._main_layout.addLayout(button_layout)

    @abc.abstractmethod
    def set_value(self, obj: Any, *args, **kwargs):
        pass

    @abc.abstractmethod
    def get_value(self, *args, **kwargs) -> Any:
        pass

    def closeEvent(self, event):
        answer = QMessageBox.question(
            self,
            self.tr("Quit?"),
            self.tr("All changes will be lost!"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

    def on_confirm(self):
        self.accept()

    def on_cancel(self):
        self.close()


class UniversalSourceCodeEditDialog(BaseSourceCodeEditDialog):
    def __init__(self, configs: dict = None, window_title: str = "", parent=None):
        super().__init__(configs=configs, window_title=window_title, parent=parent)

    def set_value(self, obj: str | None, none_as_empty: bool = False, *args, **kwargs):
        if obj is None:
            if none_as_empty:
                obj = ""
            else:
                return
        self._code_edit.setText(obj)

    def get_value(self, empty_as_none: bool = False, *args, **kwargs) -> str | None:
        text = self._code_edit.text()
        if not text and empty_as_none:
            return None
        else:
            return text


class BaseSourceCodeEditor(CommonParameterWidget):
    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: Any = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        if configs is None:
            configs = DEFAULT_CONFIGS.copy()

        self._value_widget: QPushButton | None = None
        self._display_widget: QPlainTextEdit | None = None
        self._display_current_value = display_current_value

        self._current_value = default

        self._configs = configs
        self._edit_button_text = edit_button_text or QApplication.tr("Edit/View")
        self._window_title = window_title or QApplication.tr("Code Editor")

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self.default)

    # noinspection PyUnresolvedReferences
    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)

        self._display_widget = QPlainTextEdit(parent=center_widget)
        self._display_widget.setReadOnly(True)
        if self._display_current_value:
            self._display_widget.show()
        else:
            self._display_widget.hide()

        self._value_widget = QPushButton(self._edit_button_text, parent=center_widget)
        self._value_widget.clicked.connect(self.open_edit_dialog)

        center_widget_layout.addWidget(self._display_widget)
        center_widget_layout.addWidget(self._value_widget)

    def _on_use_default_checkbox_toggled(self, checked):
        super()._on_use_default_checkbox_toggled(checked)
        if checked:
            self._update_current_value_display(self.default)

    def _update_current_value_display(self, value):
        self._display_widget.setPlainText(f"value: {value}\n" f"type: {type(value)}")

    def get_value(self, *args, **kwargs) -> Any:
        if self._is_use_default():
            return self._default
        else:
            return copy.deepcopy(self._current_value)

    def set_value(self, value: Any, *args, **kwargs):
        value = copy.deepcopy(value)
        self._update_current_value_display(value)
        if not self._pre_set_value(value):
            return
        self._current_value = value

    @abc.abstractmethod
    def source_code_dialog(self) -> BaseSourceCodeEditDialog:
        pass

    def fetch_result_from_dialog(self, dialog: BaseSourceCodeEditDialog):
        return dialog.get_value()

    def open_edit_dialog(self):
        dialog = self.source_code_dialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            value = self.fetch_result_from_dialog(dialog)
        else:
            value = self._current_value
        self.set_value(value)


class UniversalSourceCodeEditor(BaseSourceCodeEditor):
    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
            parent=parent,
        )

    def get_value(self, *args, **kwargs) -> str | None:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: str | None, *args, **kwargs):
        if value is not None and not isinstance(value, str):
            raise TypeError(self.tr("value must be None or str"))
        super().set_value(value, *args, **kwargs)

    def source_code_dialog(self) -> UniversalSourceCodeEditDialog:
        dialog = UniversalSourceCodeEditDialog(
            configs=self._configs, window_title=self._window_title, parent=self
        )
        dialog.set_value(self._current_value)
        return dialog


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
    def __init__(
        self,
        top_level_types: tuple = JsonTopLevelTypes,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: Any = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        if configs is None:
            configs = DEFAULT_CONFIGS.copy()
        configs["Lexer"] = "JSON"

        if default is not None:
            self._top_level_types = remove_tuple_element(top_level_types, NoneType)
        else:
            self._top_level_types = top_level_types

        if not isinstance(default, self._top_level_types):
            raise InvalidValueError(
                QApplication.tr(
                    f"default value '{default}' is not one of the following types: {self._top_level_types}"
                )
            )

        super().__init__(
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
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

    def get_value(self, *args, **kwargs) -> Any | None:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: Any | None, *args, **kwargs):
        super().set_value(value, *args, **kwargs)


class ListEditor(JsonEditor):
    TYPE_RESTRICTIONS = (list, NoneType)

    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: list = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            top_level_types=self.TYPE_RESTRICTIONS,
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
            parent=parent,
        )

    def get_value(self, *args, **kwargs) -> list | None:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: list | None, *args, **kwargs):
        if isinstance(value, (tuple, set)):
            value = list(value)
        super().set_value(value, *args, **kwargs)


class TupleEditor(JsonEditor):
    TYPE_RESTRICTIONS = (list, tuple, NoneType)

    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: tuple = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
            parent=parent,
        )

    def set_value(self, value: tuple | None, *args, **kwargs):
        if isinstance(value, list):
            value = tuple(value)
        super().set_value(value, *args, **kwargs)

    def get_value(self, *args, **kwargs) -> tuple | None:
        value = super().get_value(*args, **kwargs)
        if value is None:
            return None
        elif isinstance(value, list):
            return tuple(value)
        elif isinstance(value, tuple):
            return value
        else:
            raise InvalidValueError(
                self.tr(
                    f"value '{value}' is not one of the following types: {self._top_level_types}"
                )
            )


class DictEditor(JsonEditor):
    TYPE_RESTRICTIONS = (dict, NoneType)

    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: dict = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            top_level_types=self.TYPE_RESTRICTIONS,
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
            parent=parent,
        )

    def get_value(self, *args, **kwargs) -> dict | None:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: dict | None, *args, **kwargs):
        super().set_value(value, *args, **kwargs)


def __test_main():
    from PyQt6.QtWidgets import QApplication, QWidget

    app = QApplication([])
    wind = QWidget()
    layout = QVBoxLayout(wind)
    wind.setLayout(layout)

    source_code_editor = UniversalSourceCodeEditor(
        default=None, stylesheet="QCheckBox{background-color: red}", parent=wind
    )
    source_code_editor.set_label("UniversalSourceCodeEditor")

    json_editor = JsonEditor(display_current_value=False, default=None, parent=wind)
    json_editor.set_label("JsonEditor")

    json_editor2 = ListEditor(display_current_value=False, default=[], parent=wind)
    json_editor2.set_label("ListEditor")
    a = [1, 2, 3]
    print(id(a))
    json_editor2.set_value(a)
    b = json_editor2.get_value()
    print(id(b))

    json_editor3 = DictEditor(default=None, parent=wind)
    json_editor3.set_label("DictEditor")

    json_editor4 = TupleEditor(default=(1, 2, 3), parent=wind)
    json_editor4.set_label("TupleEditor")

    layout.addWidget(source_code_editor)
    layout.addWidget(json_editor)
    layout.addWidget(json_editor2)
    layout.addWidget(json_editor3)
    layout.addWidget(json_editor4)
    wind.show()
    app.exec()


if __name__ == "__main__":
    __test_main()
