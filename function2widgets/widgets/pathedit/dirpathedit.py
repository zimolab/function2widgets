import dataclasses
from typing import Optional

from PyQt6.QtWidgets import QWidget

from .base import PathEditArgs, PathEdit, PATH_TYPE_SAVE_DIR, PATH_TYPE_OPEN_DIR


@dataclasses.dataclass(frozen=True)
class DirPathEditArgs(PathEditArgs):
    parameter_name: str
    default: Optional[str] = ""
    save_dir: bool = False


class DirPathEdit(PathEdit):
    HIDE_DEFAULT_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = DirPathEditArgs

    def __init__(self, args: DirPathEditArgs, parent: Optional[QWidget] = None):
        if args.save_dir:
            path_type = PATH_TYPE_SAVE_DIR
        else:
            path_type = PATH_TYPE_OPEN_DIR

        args = dataclasses.replace(
            args,
            path_type=path_type,
            filters="",
            init_filter=None,
            path_delimiter="",
        )

        super().__init__(args=args, parent=parent)
