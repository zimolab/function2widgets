import dataclasses
from typing import Optional, Dict, Any, cast

from PyQt6.QtWidgets import QWidget, QVBoxLayout

from function2widgets.widgets._sourcecodeedit import _SourceCodeEdit
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class CodeEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = ""
    configs: Optional[Dict[str, Any]] = None


class CodeEdit(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = CodeEditArgs

    def __init__(self, args: CodeEditArgs, parent: Optional[QWidget] = None):

        self._value_widget: Optional[_SourceCodeEdit] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> CodeEditArgs:
        return cast(CodeEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = _SourceCodeEdit(configs=self._args.configs)

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
        self._value_widget.setText(value)

    def get_value_from_widget(self) -> str:
        return self._value_widget.text()
