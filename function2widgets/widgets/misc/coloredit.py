import dataclasses
from typing import Optional, cast, Union, Literal

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette, QCursor
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QColorDialog,
    QPushButton,
)

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


class Color(object):
    def __init__(self, r: int = 255, g: int = 255, b: int = 255, a: int = 255):
        self._r = self.map_value(r)
        self._g = self.map_value(g)
        self._b = self.map_value(b)
        self._a = self.map_value(a)

    @property
    def r(self) -> int:
        return self._r

    @r.setter
    def r(self, value: int):
        self._r = self.map_value(value)

    @property
    def g(self) -> int:
        return self._g

    @g.setter
    def g(self, value: int):
        self._g = self.map_value(value)

    @property
    def b(self) -> int:
        return self._b

    @b.setter
    def b(self, value: int):
        self._b = self.map_value(value)

    @property
    def a(self) -> int:
        return self._a

    @a.setter
    def a(self, value: int):
        self._a = self.map_value(value)

    def get_invert_color(self, invert_alpha: bool = False) -> "Color":
        new_alpha = self.a
        if invert_alpha:
            new_alpha = 255 - self.a
        return Color(255 - self.r, 255 - self.g, 255 - self.b, new_alpha)

    def to_hex_string(self, with_alpha: bool = True) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}" + (
            f"{self.a:02x}" if with_alpha else ""
        )

    def to_rgb_string(self, with_alpha: bool = True) -> str:
        return f"{self.r},{self.g},{self.b}" + (f",{self.a}" if with_alpha else "")

    def to_rgb_tuple(self, with_alpha: bool = True) -> tuple:
        return (
            (self.r, self.g, self.b, self.a) if with_alpha else (self.r, self.g, self.b)
        )

    def to_qt_color(self, with_alpha: bool = True) -> QColor:
        return QColor(*self.to_rgb_tuple(with_alpha=with_alpha))

    def __repr__(self):
        return self.to_hex_string(with_alpha=True)

    def __str__(self):
        return self.to_hex_string(with_alpha=True)

    @classmethod
    def from_hex_string(cls, hex_str: str) -> "Color":
        return cls(*QColor.fromString(hex_str).getRgb())

    @classmethod
    def from_color_name(cls, name: str) -> "Color":
        return cls(*QColor(name).getRgb())

    @classmethod
    def from_string(cls, string: str) -> "Color":
        string = string.strip()
        if string.startswith("#"):
            return cls.from_hex_string(string)
        else:
            return cls.from_color_name(string)

    @classmethod
    def from_qt_color(cls, color: QColor) -> "Color":
        return cls(*color.getRgb())

    @staticmethod
    def map_value(value: Optional[int]):
        if value is None:
            return 255
        if value < 0:
            return 0
        elif value > 255:
            return 255
        else:
            return value


DEFAULT_COLOR = "white"
DEFAULT_DISPLAY_WIDGET_SIZE = 120

_COLOR_WIDGET_STYLE = """QPushButton{
    font-weight:bold;
}
"""


@dataclasses.dataclass(frozen=True)
class ColorEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Union[str, Color, QColor, None] = DEFAULT_COLOR
    with_alpha: bool = True
    display_format: Literal["hex", "rgb"] = "hex"
    display_widget_size: int = DEFAULT_DISPLAY_WIDGET_SIZE
    color_picker_title: Optional[str] = None


class ColorEdit(CommonParameterWidget):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = ColorEditArgs

    def __init__(self, args: ColorEditArgs, parent: Optional[QWidget] = None):
        self._value_widget: Optional[QPushButton] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> ColorEditArgs:
        return cast(ColorEditArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QPushButton(center_widget)
        widget_size = self._args.display_widget_size
        self._value_widget.setMaximumSize(widget_size, widget_size)
        self._value_widget.setMinimumSize(widget_size, widget_size)

        self._value_widget.setStyleSheet(_COLOR_WIDGET_STYLE)
        # important!
        self._value_widget.setAutoFillBackground(True)
        # important!
        self._value_widget.setFlat(True)
        self._value_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self._value_widget.setCheckable(False)
        self._value_widget.setAutoDefault(False)
        self._value_widget.setDefault(False)
        self._value_widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        # noinspection PyUnresolvedReferences
        self._value_widget.clicked.connect(self._on_pick_color)
        init_color = Color().to_qt_color()
        self._set_bg_color(init_color)
        self._update_color_text(init_color)

        center_widget_layout = QHBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        left_spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        center_widget_layout.addSpacerItem(left_spacer)
        center_widget_layout.addWidget(self._value_widget)
        right_spacer = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        center_widget_layout.addSpacerItem(right_spacer)

    def set_value(self, value: Union[str, Color, QColor, None]):
        if not isinstance(value, (str, Color, QColor)) and value is not None:
            raise InvalidValueError(
                f"value must be str or Color or QColor, got {type(value)}"
            )
        if isinstance(value, str):
            value = Color.from_hex_string(value)
        super().set_value(value)

    def get_value(self) -> Optional[Color]:
        return super().get_value()

    def set_value_to_widget(self, value: Union[Color, QColor]):
        if isinstance(value, Color):
            value = value.to_qt_color()
        self._set_bg_color(value)
        self._update_color_text(value)

    # def eventFilter(self, obj, event):
    #     if obj == self._value_widget and event.type() == QEvent.Type.MouseButtonPress:
    #         if event.button() == Qt.MouseButton.LeftButton:
    #             color = self._pick_color()
    #             if color is not None:
    #                 self.set_value(color)
    #         return True
    #
    #     return super().eventFilter(obj, event)

    def get_value_from_widget(self) -> Color:
        return Color.from_qt_color(self._get_bg_color())

    def _on_pick_color(self):
        color = self._pick_color()
        if color is not None:
            self.set_value(color)

    def _pick_color(self) -> Optional[QColor]:
        dialog_title = self._args.color_picker_title
        options = QColorDialog.ColorDialogOption.DontUseNativeDialog
        if self._args.with_alpha:
            options = options | QColorDialog.ColorDialogOption.ShowAlphaChannel
        color = QColorDialog.getColor(self._get_bg_color(), self, dialog_title, options)
        if color.isValid():
            return color
        return None

    def _set_bg_color(self, color: QColor):
        palette = self._value_widget.palette()
        palette.setColor(QPalette.ColorRole.Button, color)
        self._value_widget.setPalette(palette)

    def _get_bg_color(self) -> QColor:
        palette = self._value_widget.palette().button()
        return palette.color()

    def _update_color_text(self, bg_color: QColor):
        color = Color.from_qt_color(bg_color)
        invert_color = color.get_invert_color()
        invert_color.a = 255
        invert_color = invert_color.to_qt_color()
        if self._args.display_format.lower() == "hex":
            color_text = color.to_hex_string(with_alpha=self._args.with_alpha)
        else:
            color_text = color.to_rgb_string(with_alpha=self._args.with_alpha)
        palette = self._value_widget.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, invert_color)
        self._value_widget.setPalette(palette)
        self._value_widget.setText(color_text)
