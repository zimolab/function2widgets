import dataclasses
from typing import Optional, cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider, QWidget, QLabel, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

TickPosition = {
    "None": QSlider.TickPosition.NoTicks,
    "Above": QSlider.TickPosition.TicksAbove,
    "Below": QSlider.TickPosition.TicksBelow,
    "Both": QSlider.TickPosition.TicksBothSides,
    "Left": QSlider.TickPosition.TicksLeft,
    "Right": QSlider.TickPosition.TicksRight,
}


@dataclasses.dataclass(frozen=True)
class SliderArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[int] = 0
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    step: Optional[int] = None
    page_step: Optional[int] = None
    tracking: bool = False
    tick_position: Optional[str] = None
    tick_interval: Optional[int] = None
    inverted_appearance: bool = False
    inverted_control: bool = False
    show_value_label: bool = False
    value_prefix: Optional[str] = None
    value_suffix: Optional[str] = None


class Slider(CommonParameterWidget):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = SliderArgs

    def __init__(self, args: SliderArgs, parent: Optional[QWidget] = None):

        if args.step is not None and args.step <= 0:
            raise ValueError("step must be greater than 0")

        if args.page_step is not None and args.page_step <= 0:
            raise ValueError("page_step must be greater than 0")

        self._value_widget: Optional[QSlider] = None
        self._value_label: Optional[QLabel] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> SliderArgs:
        return cast(SliderArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QSlider(center_widget)
        self._value_widget.setOrientation(Qt.Orientation.Horizontal)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)
        center_widget_layout.addWidget(self._value_widget)

        min_value = self._args.min_value
        max_value = self._args.max_value
        step = self._args.step
        page_step = self._args.page_step
        tracking = self._args.tracking
        tick_position = self._args.tick_position
        tick_interval = self._args.tick_interval
        show_value_label = self._args.show_value_label
        inverted_appearance = self._args.inverted_appearance
        inverted_control = self._args.inverted_control

        if min_value is not None:
            self._value_widget.setMinimum(min_value)
        if max_value is not None:
            self._value_widget.setMaximum(max_value)
        if step is not None:
            self._value_widget.setSingleStep(step)
        if page_step is not None:
            self._value_widget.setPageStep(page_step)
        if tracking is not None:
            self._value_widget.setTracking(tracking)

        if isinstance(tick_position, str):
            pos = TickPosition.get(
                tick_position.capitalize(), QSlider.TickPosition.NoTicks
            )
            self._value_widget.setTickPosition(pos)

        if tick_interval is not None:
            self._value_widget.setTickInterval(tick_interval)

        self._value_widget.setInvertedControls(inverted_control is True)
        self._value_widget.setInvertedAppearance(inverted_appearance is True)

        if show_value_label:
            self._setup_value_label(center_widget_layout)
            self._update_value_label(self._value_widget.value())

    def get_value(self) -> Optional[int]:
        return super().get_value()

    def set_value(self, value: Optional[int]):
        if not isinstance(value, int) and value is not None:
            raise InvalidValueError(f"value must be an int number, got {type(value)}")
        super().set_value(value)

    def set_value_to_widget(self, value: int):
        self._value_widget.setValue(value)

    def get_value_from_widget(self) -> int:
        return self._value_widget.value()

    def _setup_value_label(self, center_widget_layout: QVBoxLayout):
        self._value_label = QLabel(self._center_widget)
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_widget_layout.addWidget(self._value_label)

        # noinspection PyUnresolvedReferences
        self._value_widget.valueChanged.connect(self._update_value_label)

    def _update_value_label(self, value: int):
        if self._value_label is None:
            return
        prefix = self._args.value_prefix or ""
        suffix = self._args.value_suffix or ""
        self._value_label.setText(f"{prefix}{value}{suffix}")
