import dataclasses
from typing import Optional, List, cast

from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidgetArgs,
    CommonParameterWidget,
)


@dataclasses.dataclass(frozen=True)
class ComboBoxEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = None
    items: List[str] = dataclasses.field(default_factory=list)


class ComboBoxEdit(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = ComboBoxEditArgs

    def __init__(self, args: ComboBoxEditArgs, parent: Optional[QWidget] = None):
        if args.items is None:
            raise ValueError(f"items must be specified")

        self._value_widget: Optional[QComboBox] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> ComboBoxEditArgs:
        return cast(ComboBoxEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QComboBox(center_widget)
        self._value_widget.setEditable(True)
        for text in self._args.items:
            self._value_widget.addItem(text)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.addWidget(self._value_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

    def set_value(self, value: str):
        if value is not None and not isinstance(value, str):
            raise InvalidValueError(f"value must be str, got {type(value)}")
        super().set_value(value)

    def get_value(self) -> Optional[str]:
        return super().get_value()

    def set_value_to_widget(self, value: str):
        if value is None:
            return
        if value not in self._args.items:
            self._value_widget.addItem(value)
        self._value_widget.setCurrentText(value)

    def get_value_from_widget(self) -> str:
        return self._value_widget.currentText()
