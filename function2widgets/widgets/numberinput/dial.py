import dataclasses
from typing import Optional, cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDial, QLabel, QWidget, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class DialArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[int] = 0
    min_value: int = None
    max_value: int = None
    step: int = None
    page_step: int = None
    tracking: bool = False
    wrapping: bool = False
    notches_visible: bool = True
    notches_target: float = None
    inverted_appearance: bool = False
    inverted_control: bool = False
    show_value_label: bool = False
    value_prefix: str = None
    value_suffix: str = None


class Dial(CommonParameterWidget):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = DialArgs

    def __init__(self, args: DialArgs, parent: Optional[QWidget] = None):

        if args.step is not None and args.step <= 0:
            raise ValueError("step must be greater than 0")

        if args.page_step is not None and args.page_step <= 0:
            raise ValueError("page_step must be greater than 0")

        self._value_widget: Optional[QDial] = None
        self._value_label: Optional[QLabel] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> DialArgs:
        return cast(DialArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._value_widget = QDial(center_widget)
        center_widget_layout.addWidget(self._value_widget)

        min_value = self._args.min_value
        max_value = self._args.max_value
        step = self._args.step
        page_step = self._args.page_step
        tracking = self._args.tracking
        wrapping = self._args.wrapping
        notches_visible = self._args.notches_visible
        notches_target = self._args.notches_target
        inverted_appearance = self._args.inverted_appearance
        inverted_control = self._args.inverted_control
        show_value_label = self._args.show_value_label

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
        if wrapping is not None:
            self._value_widget.setWrapping(wrapping)
        self._value_widget.setNotchesVisible(notches_visible is True)
        if notches_target is not None:
            self._value_widget.setNotchTarget(notches_target)
        self._value_widget.setInvertedAppearance(inverted_appearance is True)
        self._value_widget.setInvertedControls(inverted_control is True)

        if show_value_label:
            self._setup_value_label(center_widget_layout)
            self._update_value_label(self._value_widget.value())

    def get_value(self) -> Optional[int]:
        return super().get_value()

    def set_value(self, value: Optional[int]):
        if not isinstance(value, int) and value is not None:
            raise InvalidValueError(f"value must be int, got {type(value)}")
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
