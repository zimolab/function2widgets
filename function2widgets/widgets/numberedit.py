"""
主要包含数值输入类控件，如：IntSpinBox, FloatSpanBox、DialWidget、SliderWidget
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QSpinBox,
    QWidget,
    QVBoxLayout,
    QDoubleSpinBox,
    QDial,
    QLabel,
    QSlider,
)

from function2widgets.widgets.base import CommonParameterWidget


class IntSpinBox(CommonParameterWidget):
    def __init__(
        self,
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        prefix: str = None,
        suffix: str = None,
        default: int | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: QSpinBox | None = None
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._prefix = prefix
        self._suffix = suffix

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self._default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget.setLayout(center_widget_layout)
        center_widget.setContentsMargins(0, 0, 0, 0)

        self._value_widget = QSpinBox(center_widget)
        center_widget_layout.addWidget(self._value_widget)

        if self._min_value is not None:
            self._value_widget.setMinimum(self._min_value)
        if self._max_value is not None:
            self._value_widget.setMaximum(self._max_value)
        if self._step is not None:
            self._value_widget.setSingleStep(self._step)
        if self._prefix:
            self._value_widget.setPrefix(self._prefix)
        if self._suffix:
            self._value_widget.setSuffix(self._suffix)

    def get_value(self, *args, **kwargs) -> int | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.value()

    def set_value(self, value: int | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setValue(value)


class FloatSpinBox(CommonParameterWidget):
    def __init__(
        self,
        min_value: float = None,
        max_value: float = None,
        step: float = None,
        decimals: int = None,
        prefix: str = None,
        suffix: str = None,
        accelerated: bool = False,
        default: float | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: QDoubleSpinBox | None = None
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._decimals = decimals
        self._prefix = prefix
        self._suffix = suffix
        self._accelerated = accelerated

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self._default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget.setLayout(center_widget_layout)
        center_widget.setContentsMargins(0, 0, 0, 0)

        self._value_widget = QDoubleSpinBox(center_widget)
        center_widget_layout.addWidget(self._value_widget)

        if self._min_value is not None:
            self._value_widget.setMinimum(self._min_value)
        if self._max_value is not None:
            self._value_widget.setMaximum(self._max_value)
        if self._step is not None:
            self._value_widget.setSingleStep(self._step)
        if self._prefix:
            self._value_widget.setPrefix(self._prefix)
        if self._suffix:
            self._value_widget.setSuffix(self._suffix)
        if self._decimals is not None:
            self._value_widget.setDecimals(self._decimals)
        self._value_widget.setAccelerated(self._accelerated is True)

    def get_value(self, *args, **kwargs) -> float | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.value()

    def set_value(self, value: float | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setValue(value)


class Dial(CommonParameterWidget):
    def __init__(
        self,
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        page_step: int = None,
        tracking: bool = False,
        wrapping: bool = False,
        notches_visible: bool = True,
        notches_target: float = None,
        inverted_appearance: bool = False,
        inverted_control: bool = False,
        show_value_label: bool = False,
        value_prefix: str = None,
        value_suffix: str = None,
        default: float | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: QDial | None = None
        self._value_label: QLabel | None = None

        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._page_step = page_step
        self._tracking = tracking
        self._wrapping = wrapping
        self._notches_visible = notches_visible
        self._notches_target = notches_target
        self._inverted_appearance = inverted_appearance
        self._inverted_control = inverted_control
        self._show_value_label = show_value_label
        self._value_prefix = value_prefix
        self._value_suffix = value_suffix

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self._default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._value_widget = QDial(center_widget)
        center_widget_layout.addWidget(self._value_widget)

        if self._min_value is not None:
            self._value_widget.setMinimum(self._min_value)
        if self._max_value is not None:
            self._value_widget.setMaximum(self._max_value)
        if self._step is not None:
            self._value_widget.setSingleStep(self._step)
        if self._page_step is not None:
            self._value_widget.setPageStep(self._page_step)
        if self._tracking is not None:
            self._value_widget.setTracking(self._tracking)
        if self._wrapping is not None:
            self._value_widget.setWrapping(self._wrapping)
        self._value_widget.setNotchesVisible(self._notches_visible is True)
        if self._notches_target is not None:
            self._value_widget.setNotchTarget(self._notches_target)
        self._value_widget.setInvertedAppearance(self._inverted_appearance is True)
        self._value_widget.setInvertedControls(self._inverted_control is True)

        if self._show_value_label:
            self._setup_value_label(center_widget_layout)
            self._update_value_label(self._value_widget.value())

    def get_value(self, *args, **kwargs) -> int | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.value()

    def set_value(self, value: int | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setValue(value)

    def _setup_value_label(self, center_widget_layout: QVBoxLayout):
        self._value_label = QLabel(self._center_widget)
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_widget_layout.addWidget(self._value_label)

        # noinspection PyUnresolvedReferences
        self._value_widget.valueChanged.connect(self._update_value_label)

    def _update_value_label(self, value: int):
        if self._value_label is None:
            return
        prefix = self._value_prefix or ""
        suffix = self._value_suffix or ""
        self._value_label.setText(f"{prefix}{value}{suffix}")


class Slider(CommonParameterWidget):
    TickPosition = {
        "None": QSlider.TickPosition.NoTicks,
        "Above": QSlider.TickPosition.TicksAbove,
        "Below": QSlider.TickPosition.TicksBelow,
        "Both": QSlider.TickPosition.TicksBothSides,
        "Left": QSlider.TickPosition.TicksLeft,
        "Right": QSlider.TickPosition.TicksRight,
    }

    def __init__(
        self,
        min_value: int = None,
        max_value: int = None,
        step: int = None,
        page_step: int = None,
        tracking: bool = False,
        tick_position: str = None,
        tick_interval: int = None,
        inverted_appearance: bool = False,
        inverted_control: bool = False,
        show_value_label: bool = False,
        value_prefix: str = None,
        value_suffix: str = None,
        default: float | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: QSlider | None = None
        self._value_label: QLabel | None = None

        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._page_step = page_step
        self._tracking = tracking
        self._tick_position = tick_position
        self._tick_interval = tick_interval
        self._inverted_appearance = inverted_appearance
        self._inverted_control = inverted_control
        self._show_value_label = show_value_label
        self._value_prefix = value_prefix
        self._value_suffix = value_suffix

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self._default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._value_widget = QSlider(center_widget)
        self._value_widget.setOrientation(Qt.Orientation.Horizontal)
        center_widget_layout.addWidget(self._value_widget)

        if self._min_value is not None:
            self._value_widget.setMinimum(self._min_value)
        if self._max_value is not None:
            self._value_widget.setMaximum(self._max_value)
        if self._step is not None:
            self._value_widget.setSingleStep(self._step)
        if self._page_step is not None:
            self._value_widget.setPageStep(self._page_step)
        if self._tracking is not None:
            self._value_widget.setTracking(self._tracking)

        if isinstance(self._tick_position, str):
            pos = self.TickPosition.get(
                self._tick_position.capitalize(), QSlider.TickPosition.NoTicks
            )
            self._value_widget.setTickPosition(pos)

        if self._tick_interval is not None:
            self._value_widget.setTickInterval(self._tick_interval)

        if self._show_value_label:
            self._setup_value_label(center_widget_layout)
            self._update_value_label(self._value_widget.value())

    def get_value(self, *args, **kwargs) -> int | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.value()

    def set_value(self, value: int | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setValue(value)

    def _setup_value_label(self, center_widget_layout: QVBoxLayout):
        self._value_label = QLabel(self._center_widget)
        self._value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        center_widget_layout.addWidget(self._value_label)

        # noinspection PyUnresolvedReferences
        self._value_widget.valueChanged.connect(self._update_value_label)

    def _update_value_label(self, value: int):
        if self._value_label is None:
            return
        prefix = self._value_prefix or ""
        suffix = self._value_suffix or ""
        self._value_label.setText(f"{prefix}{value}{suffix}")


def __test_main():
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    widget = QWidget()
    layout = QVBoxLayout(widget)
    widget.setLayout(layout)

    int_spin = IntSpinBox(min_value=0, max_value=100, step=1, default=None)
    int_spin.set_label("IntSpinBox")
    print(f"{int_spin.get_value()}")
    int_spin.set_value(10)
    print(f"{int_spin.get_value()}")
    int_spin.set_value(None)
    print()

    float_spin = FloatSpinBox(
        min_value=-100000.0, max_value=100000.0, step=1.5, decimals=5, default=10.01
    )
    float_spin.set_label("FloatSpinBox")
    print(f"{float_spin.get_value()}")
    float_spin.set_value(10.255555)
    print(f"{float_spin.get_value()}")
    float_spin.set_value(10.01)
    print()

    dial = Dial(
        min_value=0,
        max_value=360,
        step=1,
        page_step=10,
        notches_visible=True,
        notches_target=2.0,
        show_value_label=True,
        value_suffix="°",
        default=None,
    )
    dial.set_label("DialWidget")
    print(f"{dial.get_value()}")
    dial.set_value(180)
    print(f"{dial.get_value()}")
    dial.set_value(None)
    print()

    slider = Slider(
        min_value=0,
        max_value=360,
        step=1,
        page_step=10,
        tick_position="Above",
        tick_interval=0,
        show_value_label=True,
        value_suffix="°",
        default=None,
    )
    slider.set_label("SliderWidget")
    print(f"{slider.get_value()}")
    slider.set_value(180)
    print(f"{slider.get_value()}")
    slider.set_value(None)
    print()

    layout.addWidget(int_spin)
    layout.addWidget(float_spin)
    layout.addWidget(dial)
    layout.addWidget(slider)
    widget.show()
    app.exec()


if __name__ == "__main__":
    __test_main()
