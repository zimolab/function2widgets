import dataclasses
from typing import Optional, Any, cast

from PyQt6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class PlainTextEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = ""
    placeholder: Optional[str] = None
    readonly: bool = False
    overwrite_mode: bool = False
    line_wrap_mode: bool = False


class PlainTextEdit(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = PlainTextEditArgs

    def __init__(self, args: PlainTextEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: Optional[QPlainTextEdit] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> PlainTextEditArgs:
        return cast(PlainTextEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QPlainTextEdit(center_widget)

        if self._args.placeholder:
            self._value_widget.setPlaceholderText(self._args.placeholder)

        self._value_widget.setReadOnly(self._args.readonly is True)
        self._value_widget.setOverwriteMode(self._args.overwrite_mode is True)
        if self._args.line_wrap_mode:
            self._value_widget.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        else:
            self._value_widget.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        center_widget_layout.addWidget(self._value_widget)

    def get_value(self) -> Optional[str]:
        return super().get_value()

    def set_value(self, value: Any):
        if value is not None:
            value = str(value)
        super().set_value(value)

    def set_value_to_widget(self, value: str):
        self._value_widget.setPlainText(value)

    def get_value_from_widget(self) -> str:
        return self._value_widget.toPlainText()
