import traceback
from typing import Any

from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator, QDoubleValidator
from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import CommonParameterWidget

ECHO_MODES = {
    "Normal": QLineEdit.EchoMode.Normal,
    "Password": QLineEdit.EchoMode.Password,
    "NoEcho": QLineEdit.EchoMode.NoEcho,
    "PasswordEchoOnEdit": QLineEdit.EchoMode.PasswordEchoOnEdit,
}


class LineEdit(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: str | None = None,
        placeholder: str = "",
        clear_button: bool = False,
        echo_mode: str = "Normal",
        regex: str = None,
        input_mask: str = None,
        stylesheet: str | None = "",
        parent: QWidget | None = None,
    ):
        self._value_widget: QLineEdit | None = None

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        if placeholder:
            self._value_widget.setPlaceholderText(placeholder)
        self._value_widget.setClearButtonEnabled(clear_button)
        self._value_widget.setEchoMode(
            ECHO_MODES.get(echo_mode.capitalize(), QLineEdit.EchoMode.Normal)
        )
        if regex:
            regex_validator = QRegularExpressionValidator(regex)
            regex_validator.setParent(self)
            self._value_widget.setValidator(regex_validator)
        if input_mask:
            self._value_widget.setInputMask(input_mask)
        if self.SET_DEFAULT_ON_INIT:
            self.set_value(self.default)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QLineEdit(center_widget)
        center_widget_layout = QHBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget_layout.setObjectName("value_widget_layout")
        center_widget_layout.addWidget(self._value_widget)
        center_widget.setLayout(center_widget_layout)

    @property
    def value_widget(self) -> QLineEdit:
        return self._value_widget

    def set_value(self, value: Any, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setText(str(value))

    def get_value(self, *args, **kwargs) -> str | None:
        if self._is_use_default():
            return self.default
        return self._value_widget.text()


class IntLineEdit(LineEdit):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: int | None = None,
        max_value: int = None,
        min_value: int = None,
        placeholder: str = "",
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            default=default,
            placeholder=placeholder,
            clear_button=False,
            echo_mode="Normal",
            regex=None,
            input_mask=None,
            stylesheet=stylesheet,
            parent=parent,
        )

        edit_validator = QIntValidator(self._value_widget)
        if min_value is not None:
            edit_validator.setBottom(min_value)
        if max_value is not None:
            edit_validator.setTop(max_value)
        self._value_widget.setValidator(edit_validator)

    def get_value(self, *args, **kwargs) -> int | None:
        raw_value = super().get_value()

        if raw_value is None or raw_value == "":
            return None

        try:
            return int(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(
                self.tr(f"invalid value: value must be int (value={raw_value})")
            ) from e

    def set_value(self, value: int | None, strict: bool = False, *args, **kwargs):
        if value is None:
            super().set_value(None)
            return

        if strict and not isinstance(value, int):
            raise InvalidValueError(self.tr("value must be int"))
        super().set_value(value)


class FloatLineEdit(LineEdit):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: float | None = None,
        max_value: float = None,
        min_value: float = None,
        decimals: float = None,
        scientific_notation: bool = False,
        placeholder: str = "",
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(
            default=default,
            placeholder=placeholder,
            clear_button=False,
            echo_mode="Normal",
            regex=None,
            input_mask=None,
            stylesheet=stylesheet,
            parent=parent,
        )

        edit_validator = QDoubleValidator(self._value_widget)
        if min_value is not None:
            edit_validator.setBottom(min_value)
        if max_value is not None:
            edit_validator.setTop(max_value)
        if decimals is not None:
            edit_validator.setDecimals(decimals)
        if scientific_notation:
            edit_validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        self._value_widget.setValidator(edit_validator)

    def get_value(self, *args, **kwargs) -> float | None:
        raw_value = super().get_value()
        if raw_value is None or raw_value == "":
            return None
        try:
            return float(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(self.tr("value must be float")) from e

    def set_value(self, value: float | None, strict: bool = False, *args, **kwargs):
        if value is None:
            super().set_value(None)
            return
        if strict and not isinstance(value, float):
            raise InvalidValueError(self.tr("value must be float"))
        super().set_value(value)


def __test_main():
    from PyQt6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout(window)
    window.setLayout(layout)

    line_edit = LineEdit(default=None, placeholder="Enter value", parent=window)
    line_edit.set_label("LineEdit")
    # print("LineEdit:")
    # print(f"value: {line_edit.get_value()}")
    # line_edit.set_value(None)
    # print(f"value: {line_edit.get_value()}")
    # line_edit.set_value("hello world")
    # print(f"value: {line_edit.get_value()}")
    # line_edit.set_value(123)
    # print(f"value: {line_edit.get_value()}")
    # line_edit.set_value(None)
    print()
    # print(f"value: {line_edit.get_value()}")
    # line_edit.set_value(UNSET)
    # line_edit.set_value(line_edit._default)

    int_edit = IntLineEdit(default=0, placeholder="Enter value", parent=window)
    int_edit.set_label("IntLineEdit")
    print("IntLineEdit:")
    print(f"value: {int_edit.get_value()}")
    # print(f"value: {int_edit.get_value()}")
    int_edit.set_value(123)
    print(f"value: {int_edit.get_value()}")
    int_edit.set_value(-1)
    print(f"value: {int_edit.get_value()}")
    try:
        int_edit.set_value(None)
    except InvalidValueError as e:
        print(f"error: {e}")
    int_edit.set_value(0)
    print(f"value: {int_edit.get_value()}")
    print()

    float_edit = FloatLineEdit(default=0.0, placeholder="Enter value", parent=window)
    float_edit.set_label("FloatLineEdit")
    print("FloatLineEdit:")
    print(f"value: {float_edit.get_value()}")
    try:
        print(f"value: {float_edit.get_value()}")
    except ValueError as e:
        print(f"error: {e}")
        traceback.print_exc()
    # print(f"value: {float_edit.get_value()}")
    float_edit.set_value(123.456)
    print(f"value: {float_edit.get_value()}")
    float_edit.set_value(-1.23456)
    print(f"value: {float_edit.get_value()}")
    try:
        float_edit.set_value(None)
    except InvalidValueError as e:
        print(f"error: {e}")

    float_edit2 = FloatLineEdit(parent=window)
    print(f"float_edit2: {float_edit2.get_value()}")

    int_edit2 = IntLineEdit(parent=window)
    print(f"int_edit2: {int_edit2.get_value()}")

    layout.addWidget(line_edit)
    layout.addWidget(int_edit)
    layout.addWidget(float_edit)
    layout.addWidget(float_edit2)
    layout.addWidget(int_edit2)

    window.show()
    app.exec()


if __name__ == "__main__":
    __test_main()
