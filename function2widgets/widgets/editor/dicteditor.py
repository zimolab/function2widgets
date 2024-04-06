import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget

from function2widgets.widgets._sourcecodeedit import DEFAULT_CONFIGS
from .jsoneditor import _NoneType, JsonEditor, JsonEditorArgs


@dataclasses.dataclass(frozen=True)
class DictEditorArgs(JsonEditorArgs):
    parameter_name: str
    default: Optional[dict] = dataclasses.field(default_factory=dict)
    configs: dict = dataclasses.field(default_factory=DEFAULT_CONFIGS.copy)


class DictEditor(JsonEditor):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    TYPE_RESTRICTIONS = (dict, _NoneType)

    _WidgetArgsClass = DictEditorArgs

    @property
    def _args(self) -> DictEditorArgs:
        return cast(DictEditorArgs, super()._args)

    def __init__(self, args: JsonEditorArgs, parent: Optional[QWidget] = None):

        args = dataclasses.replace(args, top_level_types=self.TYPE_RESTRICTIONS)

        super().__init__(args=args, parent=parent)

    def get_value(self) -> Optional[dict]:
        return super().get_value()

    def set_value(self, value: Optional[dict]):
        super().set_value(value)
