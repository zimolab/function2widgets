import dataclasses
from typing import Optional, List, cast

from PyQt6.QtWidgets import QWidget, QButtonGroup, QGridLayout, QRadioButton

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

CLEAR_ALL = object()


@dataclasses.dataclass(frozen=True)
class RadioButtonGroupArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[List[str]] = CLEAR_ALL
    items: List[str] = None
    column_count: int = 1


class RadioButtonGroup(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = RadioButtonGroupArgs

    _BTN_PREFIX = "_radio_button_"

    def __init__(self, args: RadioButtonGroupArgs, parent: Optional[QWidget] = None):

        if args.column_count < 1:
            raise ValueError(f"column_count must be greater than 0")

        if not args.items:
            raise ValueError(f"items must be specified")

        self._button_group: Optional[QButtonGroup] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> RadioButtonGroupArgs:
        return cast(RadioButtonGroupArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):

        center_widget_layout = QGridLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        button_group = QButtonGroup(center_widget)
        button_group.setExclusive(True)
        column_count = self._args.column_count
        for i, item in enumerate(self._args.items):
            radio_button = QRadioButton(center_widget)
            btn_id = f"{self._BTN_PREFIX}{item}"
            radio_button.setObjectName(btn_id)
            radio_button.setText(item)

            button_group.addButton(radio_button)
            if i % column_count == 0:
                center_widget_layout.addWidget(radio_button, i // column_count, 0)
            else:
                center_widget_layout.addWidget(
                    radio_button, i // column_count, i % column_count
                )
        self._button_group = button_group

    def get_value(self) -> Optional[str]:
        return super().get_value()

    def set_value(self, value: Optional[str]):
        if value is CLEAR_ALL:
            self._button_group.setExclusive(False)
            for btn in self._button_group.buttons():
                btn.setChecked(False)
            self._button_group.setExclusive(True)
            return

        if value is not None and value not in self._args.items:
            raise InvalidValueError(f"value must be one of {self._args.items}")
        super().set_value(value)

    def set_value_to_widget(self, value: str):
        radio_btn = self._get_radio_button(value)
        if radio_btn is None:
            return
        radio_btn.setChecked(True)

    def get_value_from_widget(self) -> Optional[str]:
        radio_btn = self._button_group.checkedButton()
        if not radio_btn:
            return None
        return radio_btn.text()

    def _get_radio_button(self, item: Optional[str]) -> Optional[QRadioButton]:
        if item is None:
            return None
        btn_id = f"{self._BTN_PREFIX}{item}"
        return self._center_widget.findChild(QRadioButton, btn_id)
