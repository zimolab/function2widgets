import dataclasses
from typing import Optional, cast

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.lineedit.stredit import LineEditArgs, LineEdit


@dataclasses.dataclass(frozen=True)
class IntLineEditArgs(LineEditArgs):
    parameter_name: str
    default: Optional[int] = 0
    max_value: Optional[int] = None
    min_value: Optional[int] = None


class IntLineEdit(LineEdit):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = IntLineEditArgs

    def __init__(self, args: IntLineEditArgs, parent: Optional[QWidget] = None):
        super().__init__(args=args, parent=parent)

        edit_validator = QIntValidator(self._value_widget)

        min_value = self._args.min_value
        max_value = self._args.max_value

        if min_value is not None:
            edit_validator.setBottom(min_value)
        if max_value is not None:
            edit_validator.setTop(max_value)
        self._value_widget.setValidator(edit_validator)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> IntLineEditArgs:
        return cast(IntLineEditArgs, super()._args)

    def get_value(self) -> Optional[int]:
        raw_value = super().get_value()
        # when the input line edit is empty, return None
        if raw_value is None or raw_value == "":
            return None
        try:
            return int(raw_value)
        except (TypeError, ValueError) as e:
            raise InvalidValueError(self.tr(f"not a int: {raw_value}")) from e

    def set_value(self, value: Optional[int]):
        if value is None:
            super().set_value(None)
            return
        if not isinstance(value, int):
            raise InvalidValueError(self.tr(f"not a int: {value}"))
        super().set_value(value)
