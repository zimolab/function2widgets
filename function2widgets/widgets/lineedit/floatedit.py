import dataclasses
from typing import Optional, cast

from PyQt6.QtGui import QDoubleValidator
from PyQt6.QtWidgets import QWidget

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.lineedit.stredit import LineEditArgs, LineEdit


@dataclasses.dataclass(frozen=True)
class FloatLineEditArgs(LineEditArgs):
    parameter_name: str
    default: Optional[float] = 0.0
    max_value: Optional[float] = None
    min_value: Optional[float] = None
    decimals: Optional[float] = None
    scientific_notation: bool = False


class FloatLineEdit(LineEdit):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = FloatLineEditArgs

    def __init__(self, args: FloatLineEditArgs, parent: Optional[QWidget] = None):
        super().__init__(args=args, parent=parent)

        edit_validator = QDoubleValidator(self._value_widget)
        min_value = self._args.min_value
        max_value = self._args.max_value
        decimals = self._args.decimals
        scientific_notation = self._args.scientific_notation
        if min_value is not None:
            edit_validator.setBottom(min_value)
        if max_value is not None:
            edit_validator.setTop(max_value)
        if decimals is not None:
            edit_validator.setDecimals(decimals)
        if scientific_notation:
            edit_validator.setNotation(QDoubleValidator.Notation.ScientificNotation)
        self._value_widget.setValidator(edit_validator)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> FloatLineEditArgs:
        return cast(FloatLineEditArgs, super()._args)

    def get_value(self) -> Optional[float]:
        raw_value = super().get_value()
        # when the input line edit is empty, return None
        if raw_value is None or raw_value == "":
            return None
        try:
            return float(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(self.tr(f"not a number: {raw_value}")) from e

    def set_value(self, value: Optional[float]):
        if value is None:
            super().set_value(None)
            return
        if not isinstance(value, (float, int)):
            raise InvalidValueError(self.tr(f"not a number: {value}"))
        super().set_value(float(value))
