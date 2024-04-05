import abc
import dataclasses
from typing import Any, Optional, cast

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QWidget,
    QPlainTextEdit,
    QApplication,
)

from function2widgets.widgets._sourcecodeedit import _SourceCodeEdit, DEFAULT_CONFIGS
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

BUTTON_TEXT = QApplication.translate("BaseCodeEditor", "View/Edit")
DISPLAY_WIDGET_TEXT = QApplication.translate("BaseCodeEditor", "{}\n\n{}")


class BaseCodeEditorDialog(QDialog):
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
            self.tr("All changes will be lost! Continue to quit?"),
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


@dataclasses.dataclass(frozen=True)
class BaseCodeEditorArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = ""
    configs: dict = dataclasses.field(default_factory=DEFAULT_CONFIGS.copy)
    button_text: str = BUTTON_TEXT
    window_title: str = ""
    display_current_value: bool = True
    display_widget_text: str = DISPLAY_WIDGET_TEXT


class BaseCodeEditor(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = BaseCodeEditorArgs

    def __init__(self, args: BaseCodeEditorArgs, parent: Optional[QWidget] = None):

        self._value_widget: Optional[QPushButton] = None
        self._display_widget: Optional[QPlainTextEdit] = None
        self._display_widget_text_tpl: str = "{}"

        self._current_value = args.default

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> BaseCodeEditorArgs:
        return cast(BaseCodeEditorArgs, super()._args)

    # noinspection PyUnresolvedReferences
    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)

        self._display_widget = QPlainTextEdit(parent=center_widget)
        self._display_widget.setReadOnly(True)
        display_current_value = self._args.display_current_value
        if display_current_value:
            self._update_current_value_display(self._current_value)
            self._display_widget.show()
        else:
            self._display_widget.hide()

        button_text = self._args.button_text or BUTTON_TEXT
        self._value_widget = QPushButton(button_text, parent=center_widget)
        self._value_widget.clicked.connect(self.open_edit_dialog)

        center_widget_layout.addWidget(self._display_widget)
        center_widget_layout.addWidget(self._value_widget)

    def _on_default_widget_state_changed(self, checked):
        super()._on_default_widget_state_changed(checked)
        # if checked:
        #     self._update_current_value_display(self.default)

    def _update_current_value_display(self, value):
        text = self._args.display_widget_text
        self._display_widget.setPlainText(text.format(type(value), str(value)))

    def get_value(self) -> Any:
        return super().get_value()

    def set_value(self, value: Any):
        if self._args.display_current_value:
            self._update_current_value_display(value)
        super().set_value(value)

    def get_value_from_widget(self) -> Any:
        return self._current_value

    def set_value_to_widget(self, value: Any):
        self._current_value = value

    @abc.abstractmethod
    def source_code_dialog(self) -> BaseCodeEditorDialog:
        pass

    def fetch_result_from_dialog(self, dialog: BaseCodeEditorDialog):
        return dialog.get_value()

    def open_edit_dialog(self):
        dialog = self.source_code_dialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            value = self.fetch_result_from_dialog(dialog)
        else:
            value = self._current_value
        self.set_value(value)
