import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget

from function2widgets.widgets._sourcecodeedit import DEFAULT_CONFIGS
from .jsoneditor import _NoneType, JsonEditor, JsonEditorArgs


@dataclasses.dataclass(frozen=True)
class TupleEditorArgs(JsonEditorArgs):
    parameter_name: str
    default: Optional[tuple] = dataclasses.field(default_factory=tuple)
    configs: dict = dataclasses.field(default_factory=DEFAULT_CONFIGS.copy)


class TupleEditor(JsonEditor):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = TupleEditorArgs

    TYPE_RESTRICTIONS = (list, set, tuple, _NoneType)

    def __init__(self, args: TupleEditorArgs, parent: Optional[QWidget] = None):
        args = dataclasses.replace(args, top_level_types=self.TYPE_RESTRICTIONS)

        super().__init__(args=args, parent=parent)

    @property
    def _args(self) -> TupleEditorArgs:
        return cast(TupleEditorArgs, super()._args)

    def set_value(self, value: Optional[tuple]):
        if isinstance(value, (list, set)):
            value = tuple(value)
        super().set_value(value)

    def get_value(self) -> Optional[tuple]:
        value = super().get_value()
        if value is None:
            return None
        elif isinstance(value, (list, set)):
            return tuple(value)
        elif isinstance(value, tuple):
            return value
        else:
            raise ValueError(
                f"value '{value}' is not one of the following types: {self._args.top_level_types}"
            )
