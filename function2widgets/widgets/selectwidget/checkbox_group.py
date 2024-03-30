import dataclasses
from typing import Optional, List, cast

from PyQt6.QtWidgets import QWidget, QGridLayout, QCheckBox

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class CheckBoxGroupArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[List[str]] = dataclasses.field(default_factory=list)
    items: List[str] = None
    column_count: int = 1


class CheckBoxGroup(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = True
    HIDE_DEFAULT_WIDGET = True

    _WidgetArgsClass = CheckBoxGroupArgs

    def __init__(self, args: CheckBoxGroupArgs, parent: Optional[QWidget] = None):

        if args.column_count < 1:
            raise ValueError(f"column_count must be greater than 0")

        if not args.items:
            raise ValueError(f"items must be specified")

        self._checkbox_buttons = []

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> CheckBoxGroupArgs:
        return cast(CheckBoxGroupArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QGridLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)
        column_count = self._args.column_count
        for i, item in enumerate(self._args.items):
            checkbox_btn = QCheckBox(center_widget)
            checkbox_btn.setText(item)
            self._checkbox_buttons.append(checkbox_btn)
            if i % column_count == 0:
                center_widget_layout.addWidget(checkbox_btn, i // column_count, 0)
            else:
                center_widget_layout.addWidget(
                    checkbox_btn, i // column_count, i % column_count
                )

    def get_value_from_widget(self) -> List[str]:
        return [
            checkbox.text()
            for checkbox in self._checkbox_buttons
            if checkbox.isChecked()
        ]

    def set_value_to_widget(self, value: List[str]):
        for checkbox in self._checkbox_buttons:
            if checkbox.text() in value:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def set_value(self, value: Optional[List[str]]):
        if value is not None and not isinstance(value, list):
            raise ValueError(f"value must be a list, got {type(value)}")
        super().set_value(value)

    def get_value(self) -> Optional[List[str]]:
        return super().get_value()
