import traceback
from typing import Any, Optional, Literal

from PyQt6.QtCore import QRegularExpression
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
        default: Optional[str] = None,
        placeholder: str = "",
        clear_button: bool = False,
        echo_mode: Literal[
            "Normal", "Password", "NoEcho", "PasswordEchoOnEdit"
        ] = "Normal",
        regex: str = None,
        input_mask: str = None,
        stylesheet: Optional[str] = "",
        parent: Optional[QWidget] = None,
    ):
        """
        单行文本输入控件，支持str类型参数。

        :param default: 参数的默认值
        :param placeholder: 占位文本，在无输入时显示
        :param clear_button: 是否显示清除按钮
        :param echo_mode: 回显模式，支持Normal、Password、NoEcho、PasswordEchoOnEdit
        :param regex: 用于验证输入的正则表达式
        :param input_mask: 输入掩码，用以限制输入的内容，具体参考QLineEdit对input mask的描述
        :param stylesheet: 控件的样式表
        :param parent: 控件的父组件
        """
        self._value_widget: Optional[QLineEdit] = None

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        if placeholder:
            self._value_widget.setPlaceholderText(placeholder)
        self._value_widget.setClearButtonEnabled(clear_button)
        self._value_widget.setEchoMode(
            ECHO_MODES.get(echo_mode.capitalize(), QLineEdit.EchoMode.Normal)
        )
        if regex:
            exp = QRegularExpression(regex)
            regex_validator = QRegularExpressionValidator(exp)
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

    def get_value(self, *args, **kwargs) -> Optional[str]:
        if self._is_use_default():
            return self.default
        return self._value_widget.text()


class IntLineEdit(LineEdit):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: Optional[int] = None,
        max_value: int = None,
        min_value: int = None,
        placeholder: str = "",
        stylesheet: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        """
        整数输入控件，支持int类型参数。

        :param default: 参数的默认值
        :param max_value: 参数的最大值
        :param min_value: 参数的最小值
        :param placeholder: 占位文本，在无输入时显示
        :param stylesheet: 控件的样式表
        :param parent: 控件的父组件
        """
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

    def get_value(self, *args, **kwargs) -> Optional[int]:
        raw_value = super().get_value()

        if raw_value is None or raw_value == "":
            return None

        try:
            return int(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(
                self.tr(f"value must be int, got {type(raw_value)}")
            ) from e

    def set_value(self, value: Optional[int], *args, **kwargs):
        if value is None:
            super().set_value(None)
            return

        if not isinstance(value, int):
            raise InvalidValueError(self.tr(f"value must be int, got {type(value)}"))
        super().set_value(value)


class FloatLineEdit(LineEdit):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: Optional[float] = None,
        max_value: float = None,
        min_value: float = None,
        decimals: float = None,
        scientific_notation: bool = False,
        placeholder: str = "",
        stylesheet: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ):
        """
        浮点数输入控件，支持float类型参数。

        :param default: 参数的默认值
        :param max_value: 参数的最大值
        :param min_value: 参数的最小值
        :param decimals: 参数的小数位数
        :param scientific_notation: 是否使用科学计数法
        :param placeholder: 占位文本，在无输入时显示
        :param stylesheet: 控件的样式表
        :param parent: 控件的父组件
        """
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

    def get_value(self, *args, **kwargs) -> Optional[float]:
        raw_value = super().get_value()
        if raw_value is None or raw_value == "":
            return None
        try:
            return float(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(
                self.tr(f"value must be float, got {type(raw_value)}")
            ) from e

    def set_value(self, value: Optional[float], *args, **kwargs):
        if value is None:
            super().set_value(None)
            return
        if not isinstance(value, (float, int)):
            raise InvalidValueError(self.tr(f"value must be float, got {type(value)}"))
        super().set_value(float(value))
