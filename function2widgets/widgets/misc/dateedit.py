import dataclasses
from datetime import datetime, date
from typing import Optional, cast, Union

from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDateEdit

from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)
from function2widgets.widgets.misc.datetimeedit import DEFAULT_TIME_SPEC, TIME_SPECS

DEFAULT_DISPLAY_FORMAT = "yyyy/M/d"


@dataclasses.dataclass(frozen=True)
class DateEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[date] = datetime.now().date()
    display_format: str = DEFAULT_DISPLAY_FORMAT
    min_date: Optional[date] = None
    max_date: Optional[date] = None
    calendar_popup: bool = False
    time_spec: str = DEFAULT_TIME_SPEC


class DateEdit(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = DateEditArgs

    def __init__(self, args: DateEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: Optional[QDateEdit] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> DateEditArgs:
        return cast(DateEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QDateEdit(center_widget)

        display_format = self._args.display_format
        if display_format:
            self._value_widget.setDisplayFormat(display_format)

        time_spec = self._args.time_spec
        if not time_spec:
            time_spec = DEFAULT_TIME_SPEC
        time_spec = TIME_SPECS.get(time_spec, Qt.TimeSpec.LocalTime)
        self._value_widget.setTimeSpec(time_spec)

        min_date = self._args.min_date
        if min_date:
            self._value_widget.setMinimumDate(min_date)

        max_date = self._args.max_date
        if max_date:
            self._value_widget.setMaximumDate(max_date)

        self._value_widget.setCalendarPopup(self._args.calendar_popup is True)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        center_widget_layout.addWidget(self._value_widget)

    def set_value(self, value: Union[date, QDate, None]):
        if not isinstance(value, (date, QDate)) and value is not None:
            raise TypeError(f"value must be date or QDate, got {type(value)}")
        super().set_value(value)

    def get_value(self) -> Optional[date]:
        return super().get_value()

    def set_value_to_widget(self, value: Union[date, QDate]):
        self._value_widget.setDate(value)

    def get_value_from_widget(self) -> date:
        return self._value_widget.date().toPyDate()
