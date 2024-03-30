import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget, QDoubleSpinBox, QVBoxLayout

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class FloatSpinBoxArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[float] = 0.0
    min_value: float = None
    max_value: float = None
    step: float = None
    decimals: int = None
    prefix: str = None
    suffix: str = None
    accelerated: bool = False


class FloatSpinBox(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = FloatSpinBoxArgs

    def __init__(self, args: FloatSpinBoxArgs, parent: Optional[QWidget] = None):

        if args.step is not None and args.step <= 0:
            raise ValueError("step must be greater than 0")

        self._value_widget: Optional[QDoubleSpinBox] = None

        super().__init__(args=args, parent=parent)
        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> FloatSpinBoxArgs:
        return cast(FloatSpinBoxArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QDoubleSpinBox(center_widget)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget.setLayout(center_widget_layout)
        center_widget.setContentsMargins(0, 0, 0, 0)
        center_widget_layout.addWidget(self._value_widget)

        min_value = self._args.min_value
        max_value = self._args.max_value
        step = self._args.step
        prefix = self._args.prefix
        suffix = self._args.suffix
        decimals = self._args.decimals
        accelerated = self._args.accelerated

        if min_value is not None:
            self._value_widget.setMinimum(min_value)
        if max_value is not None:
            self._value_widget.setMaximum(max_value)
        if step is not None:
            self._value_widget.setSingleStep(step)
        if prefix is not None:
            self._value_widget.setPrefix(prefix)
        if suffix:
            self._value_widget.setSuffix(suffix)
        if decimals is not None:
            self._value_widget.setDecimals(decimals)
        self._value_widget.setAccelerated(accelerated is True)

    def get_value(self) -> Optional[float]:
        return super().get_value()

    def set_value(self, value: Optional[float]):
        super().set_value(value)

    def set_value_to_widget(self, value: float):
        if self._value_widget is not None:
            self._value_widget.setValue(value)

    def get_value_from_widget(self) -> float:
        return self._value_widget.value()
