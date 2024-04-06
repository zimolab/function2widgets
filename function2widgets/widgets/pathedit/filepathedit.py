import dataclasses
from typing import Optional, cast

from PyQt6.QtWidgets import QWidget

from .base import (
    PathEditArgs,
    PathEdit,
    PATH_TYPE_OPEN_FILE,
    PATH_TYPE_OPEN_FILES,
    PATH_TYPE_SAVE_FILE,
)


@dataclasses.dataclass(frozen=True)
class FilePathEditArgs(PathEditArgs):
    parameter_name: str
    default: Optional[str] = ""
    save_file: bool = False
    multiple_files: bool = False


class FilePathEdit(PathEdit):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = FilePathEditArgs

    @property
    def _args(self) -> FilePathEditArgs:
        return cast(FilePathEditArgs, super()._args)

    def __init__(self, args: FilePathEditArgs, parent: Optional[QWidget] = None):
        if args.save_file:
            path_type = PATH_TYPE_SAVE_FILE
        elif args.multiple_files:
            path_type = PATH_TYPE_OPEN_FILES
        else:
            path_type = PATH_TYPE_OPEN_FILE

        args = dataclasses.replace(args, path_type=path_type)

        super().__init__(args=args, parent=parent)
