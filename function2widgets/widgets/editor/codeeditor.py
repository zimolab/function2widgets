import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget

from .base import BaseCodeEditor, BaseCodeEditorDialog, BaseCodeEditorArgs


class CodeEditorDialog(BaseCodeEditorDialog):
    def __init__(self, configs: dict = None, window_title: str = "", parent=None):
        super().__init__(configs=configs, window_title=window_title, parent=parent)

    def set_value(self, obj: Optional[str], *args, **kwargs):
        if obj is None:
            obj = ""
        self._code_edit.setText(obj)

    def get_value(self, *args, **kwargs) -> str:
        return self._code_edit.text()


@dataclasses.dataclass(frozen=True)
class CodeEditorArgs(BaseCodeEditorArgs):
    parameter_name: str
    default: Optional[str] = ""
    configs: dict = dataclasses.field(default_factory=dict)


class CodeEditor(BaseCodeEditor):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = CodeEditorArgs

    def __init__(self, args: CodeEditorArgs, parent: Optional[QWidget] = None):
        if args.default is not None and not isinstance(args.default, str):
            raise ValueError("default must be str, got {type(default)}")

        super().__init__(args=args, parent=parent)

    @property
    def _args(self) -> CodeEditorArgs:
        return cast(CodeEditorArgs, super()._args)

    def get_value(self) -> Optional[str]:
        return super().get_value()

    def set_value(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise ValueError(self.tr(f"value must be str, got {type(value)}"))
        super().set_value(value)

    def source_code_dialog(self) -> CodeEditorDialog:
        configs = self._args.configs or {}
        window_title = self._args.window_title or ""
        dialog = CodeEditorDialog(
            configs=configs, window_title=window_title, parent=self
        )
        dialog.set_value(self._current_value)
        return dialog
