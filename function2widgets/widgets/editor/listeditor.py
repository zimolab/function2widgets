import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget

from function2widgets.widgets._sourcecodeedit import DEFAULT_CONFIGS
from .jsoneditor import JsonEditorArgs, JsonEditor, _NoneType


@dataclasses.dataclass(frozen=True)
class ListEditorArgs(JsonEditorArgs):
    parameter_name: str
    default: Optional[list] = dataclasses.field(default_factory=list)
    configs: dict = dataclasses.field(default_factory=DEFAULT_CONFIGS.copy)


class ListEditor(JsonEditor):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = ListEditorArgs

    TYPE_RESTRICTIONS = (list, _NoneType)

    @property
    def _args(self) -> ListEditorArgs:
        return cast(ListEditorArgs, super()._args)

    def __init__(self, args: ListEditorArgs, parent: Optional[QWidget] = None):
        args = dataclasses.replace(args, top_level_types=self.TYPE_RESTRICTIONS)

        super().__init__(args=args, parent=parent)

    def set_value(self, value: Optional[list]):
        if isinstance(value, (tuple, set)):
            value = list(value)
        super().set_value(value)

    def get_value(self) -> Optional[list]:
        return super().get_value()
