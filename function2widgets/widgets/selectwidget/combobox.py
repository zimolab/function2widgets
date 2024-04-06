import dataclasses
from typing import Optional, List, Union, Tuple, cast, Any

from PyQt6.QtWidgets import QWidget, QComboBox, QVBoxLayout

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)


@dataclasses.dataclass(frozen=True)
class ComboBoxArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = None
    items: List[Union[str, Tuple[str, Any]]] = None


class ComboBox(CommonParameterWidget):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = ComboBoxArgs

    def __init__(self, args: ComboBoxArgs, parent: Optional[QWidget] = None):
        if not args.items:
            raise ValueError(f"items must be specified")

        self._items_with_data = {}
        for item in args.items:
            if isinstance(item, str):
                self._items_with_data[item] = item
            elif isinstance(item, tuple):
                if len(item) != 2:
                    raise ValueError(
                        "if item is a tuple, it mush has exactly 2 elements(one for display, another for data)"
                    )
                self._items_with_data[item[0]] = item[1]
            else:
                raise ValueError("items must be a list of str or Tuple[str, Any]")

        if args.default not in self._items_with_data and args.default is not None:
            raise ValueError(f"default value {args.default} is not in items")

        self._value_widget: Optional[QComboBox] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> ComboBoxArgs:
        return cast(ComboBoxArgs, super()._args)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QComboBox(center_widget)
        for text, data in self._items_with_data.items():
            self._value_widget.addItem(text, data)

        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.addWidget(self._value_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

    def get_value(self) -> Any:
        return super().get_value()

    def set_value(self, value: Optional[str]):
        if value is not None and value not in self._items_with_data.keys():
            raise InvalidValueError(f"value {value} is not in items")
        super().set_value(value)

    def set_value_to_widget(self, value: Optional[str]):
        if value is None:
            self._value_widget.setCurrentIndex(-1)
        else:
            self._value_widget.setCurrentText(value)

    def get_value_from_widget(self) -> Any:
        current_data = self._value_widget.currentData()
        return current_data
