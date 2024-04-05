import dataclasses
from typing import Optional, Literal, cast, Any

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtWidgets import QWidget, QLineEdit, QVBoxLayout

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

ECHO_MODES = {
    "Normal": QLineEdit.EchoMode.Normal,
    "Password": QLineEdit.EchoMode.Password,
    "NoEcho": QLineEdit.EchoMode.NoEcho,
    "PasswordEchoOnEdit": QLineEdit.EchoMode.PasswordEchoOnEdit,
}


@dataclasses.dataclass(frozen=True)
class LineEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = ""
    placeholder: Optional[str] = ""
    clear_button: bool = False
    echo_mode: Literal["Normal", "Password", "NoEcho", "PasswordEchoOnEdit"] = "Normal"
    regex: Optional[str] = None
    input_mask: Optional[str] = None


class LineEdit(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = True
    HIDE_DEFAULT_WIDGET = True

    _WidgetArgsClass = LineEditArgs

    def __init__(self, args: LineEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: QLineEdit = QLineEdit()

        super().__init__(args=args, parent=parent)

        self._setup_value_widget()

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    def get_value(self) -> str:
        return super().get_value()

    def set_value(self, value: Any):
        if not isinstance(value, str) and value is not None:
            value = str(value)
        super().set_value(value)

    def set_value_to_widget(self, value: str):
        if value is None:
            value = ""
        self._value_widget.setText(value)

    def get_value_from_widget(self) -> str:
        return self._value_widget.text()

    @property
    def _args(self) -> LineEditArgs:
        return cast(LineEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget.setParent(center_widget)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)
        center_widget_layout.addWidget(self._value_widget)

    def _setup_value_widget(self):
        if self._args.placeholder:
            self._value_widget.setPlaceholderText(self._args.placeholder)

        self._value_widget.setClearButtonEnabled(self._args.clear_button or False)
        echo_mode = self._args.echo_mode
        self._value_widget.setEchoMode(
            ECHO_MODES.get(echo_mode.capitalize(), QLineEdit.EchoMode.Normal)
        )
        regex = self._args.regex
        if regex:
            exp = QRegularExpression(regex)
            regex_validator = QRegularExpressionValidator(exp)
            regex_validator.setParent(self)
            self._value_widget.setValidator(regex_validator)
        input_mask = self._args.input_mask
        if input_mask:
            self._value_widget.setInputMask(input_mask)
