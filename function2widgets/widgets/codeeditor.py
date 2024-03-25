import abc
import copy
from typing import Any, Optional

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

from function2widgets.widget import InvalidValueError
from function2widgets.widgets._sourcecodeedit import _SourceCodeEdit, DEFAULT_CONFIGS
from function2widgets.widgets.base import CommonParameterWidget


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

    def set_value(self, obj: Optional[str], *args, **kwargs):
        if obj is None:
            obj = ""
        self._code_edit.setText(obj)

    def get_value(self, *args, **kwargs) -> str:
        return self._code_edit.text()


class BaseSourceCodeEditor(CommonParameterWidget):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        default: Any = None,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):

        if configs is None:
            configs = DEFAULT_CONFIGS.copy()

        self._value_widget: Optional[QPushButton] = None
        self._display_widget: Optional[QPlainTextEdit] = None
        self._display_current_value = display_current_value
        self._display_widget_text_tpl: str = QApplication.tr("{}")

        self._current_value = default

        self._configs = configs
        self._edit_button_text = edit_button_text or QApplication.tr("Edit/View")
        self._window_title = window_title or QApplication.tr("Editor")

        super().__init__(
            default=default,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )

        if self._set_default_on_init:
            self.set_value(self.default)

    # noinspection PyUnresolvedReferences
    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)

        self._display_widget = QPlainTextEdit(parent=center_widget)
        self._display_widget.setReadOnly(True)
        if self._display_current_value:
            self._update_current_value_display(self._current_value)
            self._display_widget.show()
        else:
            self._display_widget.hide()

        self._value_widget = QPushButton(self._edit_button_text, parent=center_widget)
        self._value_widget.clicked.connect(self.open_edit_dialog)

        center_widget_layout.addWidget(self._display_widget)
        center_widget_layout.addWidget(self._value_widget)

    def _on_use_default_checkbox_toggled(self, checked):
        super()._on_use_default_checkbox_toggled(checked)
        # if checked:
        #     self._update_current_value_display(self.default)

    def _update_current_value_display(self, value):
        self._display_widget.setPlainText(
            self._display_widget_text_tpl.format(str(value))
        )

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
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        default: Optional[str] = "",
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):
        if default is not None and not isinstance(default, str):
            raise InvalidValueError(
                QApplication.tr(f"default must be str, got {type(default)}")
            )
        super().__init__(
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            default=default,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )

    def get_value(self, *args, **kwargs) -> Optional[str]:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: Optional[str], *args, **kwargs):
        if value is not None and not isinstance(value, str):
            raise TypeError(self.tr(f"value must be None or str, got {type(value)}"))
        super().set_value(value, *args, **kwargs)

    def source_code_dialog(self) -> UniversalSourceCodeEditDialog:
        dialog = UniversalSourceCodeEditDialog(
            configs=self._configs, window_title=self._window_title, parent=self
        )
        dialog.set_value(self._current_value)
        return dialog
