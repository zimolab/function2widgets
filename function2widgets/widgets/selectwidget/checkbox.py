import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget, QCheckBox, QApplication, QVBoxLayout

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

DEFAULT_TEXT = QApplication.translate("CheckBox", "enabled")


@dataclasses.dataclass(frozen=True)
class CheckBoxArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[bool] = False
    text: str = DEFAULT_TEXT


class CheckBox(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = True
    HIDE_DEFAULT_WIDGET = True

    _WidgetArgsClass = CheckBoxArgs

    def __init__(self, args: CheckBoxArgs, parent: Optional[QWidget] = None):
        self._checkbox: Optional[QCheckBox] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            default = self._args.default
            self.set_value(default)

    @property
    def _args(self) -> CheckBoxArgs:
        return cast(CheckBoxArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._checkbox = QCheckBox(center_widget)
        self._checkbox.setText(self._args.text)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        center_widget_layout.addWidget(self._checkbox)

    def set_value_to_widget(self, value: bool):
        self._checkbox.setChecked(value is True)

    def get_value_from_widget(self) -> bool:
        return self._checkbox.isChecked()
