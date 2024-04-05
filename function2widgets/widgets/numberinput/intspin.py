import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget, QSpinBox, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class IntSpinBoxArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[int] = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None


class IntSpinBox(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = IntSpinBoxArgs

    def __init__(self, args: IntSpinBoxArgs, parent: Optional[QWidget] = None):

        if args.step is not None and args.step <= 0:
            raise ValueError("step must be greater than 0")

        self._value_widget: Optional[QSpinBox] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> IntSpinBoxArgs:
        return cast(IntSpinBoxArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QSpinBox(center_widget)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget.setLayout(center_widget_layout)
        center_widget.setContentsMargins(0, 0, 0, 0)
        center_widget_layout.addWidget(self._value_widget)

        min_value = self._args.min_value
        max_value = self._args.max_value
        step = self._args.step
        prefix = self._args.prefix
        suffix = self._args.suffix

        if min_value is not None:
            self._value_widget.setMinimum(min_value)
        if max_value is not None:
            self._value_widget.setMaximum(max_value)
        if step is not None:
            self._value_widget.setSingleStep(step)
        if prefix:
            self._value_widget.setPrefix(prefix)
        if suffix:
            self._value_widget.setSuffix(suffix)

    def get_value(self) -> Optional[int]:
        return super().get_value()

    def set_value(self, value: Optional[int]):
        if not isinstance(value, int) and value is not None:
            raise InvalidValueError(f"value must be a int, got {type(value)}")
        super().set_value(value)

    def set_value_to_widget(self, value: int):
        if value is None:
            self._value_widget.setValue(0)
        else:
            self._value_widget.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._value_widget.value()
