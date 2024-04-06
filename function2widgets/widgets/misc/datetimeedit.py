import dataclasses
from datetime import datetime
from typing import Optional, cast, Union

from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import QWidget, QDateTimeEdit, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)
from function2widgets.common import to_datetime

DEFAULT_DISPLAY_FORMAT = "yyyy/M/d H:mm"

TIME_SPEC_UTC = "UTC"
TIME_SPEC_LOCAL = "Local"
TIME_SPEC_TIMEZONE = "TimeZone"
TIME_SPEC_OFFSET = "OffsetFromUTC"

TIME_SPECS = {
    TIME_SPEC_UTC: Qt.TimeSpec.UTC,
    TIME_SPEC_LOCAL: Qt.TimeSpec.LocalTime,
    TIME_SPEC_TIMEZONE: Qt.TimeSpec.TimeZone,
    TIME_SPEC_OFFSET: Qt.TimeSpec.OffsetFromUTC,
}

DEFAULT_TIME_SPEC = TIME_SPEC_TIMEZONE


@dataclasses.dataclass(frozen=True)
class DateTimeEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Union[datetime, QDateTime, str, None] = datetime.now()
    min_datetime: Union[datetime, QDateTime, str, None] = None
    max_datetime: Union[datetime, QDateTime, str, None] = None
    display_format: str = DEFAULT_DISPLAY_FORMAT
    calendar_popup: bool = False
    time_spec: str = DEFAULT_TIME_SPEC


class DateTimeEdit(CommonParameterWidget):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = DateTimeEditArgs

    def __init__(self, args: DateTimeEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: Optional[QDateTimeEdit] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> DateTimeEditArgs:
        return cast(DateTimeEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QDateTimeEdit(center_widget)

        display_format = self._args.display_format or DEFAULT_DISPLAY_FORMAT
        self._value_widget.setDisplayFormat(display_format)

        calendar_popup = self._args.calendar_popup
        self._value_widget.setCalendarPopup(calendar_popup is True)

        time_spec = self._args.time_spec
        if not time_spec:
            time_spec = DEFAULT_TIME_SPEC
        time_spec = TIME_SPECS.get(time_spec, Qt.TimeSpec.LocalTime)
        self._value_widget.setTimeSpec(time_spec)

        max_datetime = self._args.max_datetime
        if isinstance(max_datetime, str) and max_datetime:
            max_datetime = to_datetime(max_datetime, display_format)
        if max_datetime:
            self._value_widget.setMaximumDateTime(QDateTime(max_datetime))

        min_datetime = self._args.min_datetime
        if isinstance(min_datetime, str) and min_datetime:
            min_datetime = to_datetime(min_datetime, display_format)
        if min_datetime:
            self._value_widget.setMinimumDateTime(QDateTime(min_datetime))

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        center_widget_layout.addWidget(self._value_widget)

    def set_value(self, value: Union[datetime, QDateTime, None]):
        if not isinstance(value, (datetime, QDateTime, str)) and value is not None:
            raise InvalidValueError(
                f"value must be datetime or QDateTime or a datetime string, got {type(value)}"
            )
        display_format = self._args.display_format or DEFAULT_DISPLAY_FORMAT
        if isinstance(value, str):
            value = to_datetime(value, display_format)
        super().set_value(value)

    def get_value(self) -> Optional[datetime]:
        return super().get_value()

    def set_value_to_widget(self, value: Union[datetime, QDateTime]):
        self._value_widget.setDateTime(value)

    def get_value_from_widget(self) -> datetime:
        return self._value_widget.dateTime().toPyDateTime()
