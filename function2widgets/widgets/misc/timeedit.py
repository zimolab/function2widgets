import dataclasses
from datetime import datetime, time
from typing import Optional, cast, Union

from PyQt6.QtCore import Qt, QTime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTimeEdit

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)
from function2widgets.widgets.misc.datetimeedit import DEFAULT_TIME_SPEC, TIME_SPECS

DEFAULT_DISPLAY_FORMAT = "H:mm"


@dataclasses.dataclass(frozen=True)
class TimeEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[time] = datetime.now().time()
    display_format: str = DEFAULT_DISPLAY_FORMAT
    min_time: Optional[time] = None
    max_time: Optional[time] = None
    time_spec: str = DEFAULT_TIME_SPEC


class TimeEdit(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = TimeEditArgs

    def __init__(self, args: TimeEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: Optional[QTimeEdit] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> TimeEditArgs:
        return cast(TimeEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QTimeEdit(center_widget)

        display_format = self._args.display_format
        if display_format:
            self._value_widget.setDisplayFormat(display_format)

        time_spec = self._args.time_spec
        if not time_spec:
            time_spec = DEFAULT_TIME_SPEC
        time_spec = TIME_SPECS.get(time_spec, Qt.TimeSpec.LocalTime)
        self._value_widget.setTimeSpec(time_spec)

        min_time = self._args.min_time
        if min_time:
            self._value_widget.setMinimumTime(min_time)

        max_time = self._args.max_time
        if max_time:
            self._value_widget.setMaximumTime(max_time)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        center_widget_layout.addWidget(self._value_widget)

    def set_value(self, value: Union[time, QTime, None]):
        if not isinstance(value, (time, QTime)) and value is not None:
            raise TypeError(f"value must be time or QTime, got {type(value)}")
        super().set_value(value)

    def get_value(self) -> Optional[time]:
        return super().get_value()

    def set_value_to_widget(self, value: Union[time, QTime]):
        self._value_widget.setTime(value)

    def get_value_from_widget(self) -> time:
        return self._value_widget.time().toPyTime()
