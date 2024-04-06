import dataclasses
import os.path
from typing import Optional, cast, Any

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QApplication,
)

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import (
    CommonParameterWidget,
    CommonParameterWidgetArgs,
)

PATH_TYPE_OPEN_FILE = 0
PATH_TYPE_OPEN_FILES = 1
PATH_TYPE_OPEN_DIR = 2
PATH_TYPE_SAVE_FILE = 3
PATH_TYPE_SAVE_DIR = 4

FILTER_ALL_FILES = QApplication.translate("PathEdit", "All Files (*)")

PATH_DELIMITER = ";"

BUTTON_TEXT = QApplication.translate("PathEdit", "Select")


@dataclasses.dataclass(frozen=True)
class PathEditArgs(CommonParameterWidgetArgs):
    parameter_name: str
    default: Optional[str] = ""
    path_type: int = PATH_TYPE_OPEN_FILE
    filters: str = FILTER_ALL_FILES
    init_filter: Optional[str] = None
    start_path: Optional[str] = None
    path_delimiter: str = PATH_DELIMITER
    button_text: str = BUTTON_TEXT
    placeholder: str = ""
    clear_button: bool = False
    dialog_title: Optional[str] = None


class PathEdit(CommonParameterWidget):
    HIDE_DEFAULT_VALUE_WIDGET = True
    SET_DEFAULT_ON_INIT = True

    _WidgetArgsClass = PathEditArgs

    def __init__(self, args: PathEditArgs, parent: Optional[QWidget] = None):

        self._value_widget: Optional[QLineEdit] = None
        self._select_button: Optional[QPushButton] = None

        super().__init__(args=args, parent=parent)

        if self._args.set_default_on_init:
            self.set_value(self._args.default)

    @property
    def _args(self) -> PathEditArgs:
        return cast(PathEditArgs, super()._args)

    # noinspection PyUnresolvedReferences
    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QLineEdit(center_widget)

        button_text = self._args.button_text or BUTTON_TEXT
        self._select_button = QPushButton(button_text, center_widget)

        center_widget_layout = QHBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        placeholder = self._args.placeholder or ""
        clear_button = self._args.clear_button is True

        self._value_widget.setPlaceholderText(placeholder)
        self._value_widget.setClearButtonEnabled(clear_button)

        self._select_button.clicked.connect(self._select_path)
        center_widget_layout.addWidget(self._value_widget)
        center_widget_layout.addWidget(self._select_button)
        center_widget_layout.setStretch(0, 8)
        center_widget_layout.setStretch(1, 2)

    def get_value(self) -> Optional[str]:
        return super().get_value()

    def set_value(self, value: Optional[str]):
        if value is not None and not isinstance(value, str):
            raise InvalidValueError(f"value must be str, not {type(value)}")
        super().set_value(value)

    def set_value_to_widget(self, value: str):
        self._value_widget.setText(value)

    def get_value_from_widget(self) -> Any:
        return self._value_widget.text()

    def _select_path(self):
        path_type = self._args.path_type
        if path_type == PATH_TYPE_OPEN_FILE:
            path = self._get_open_file_path()
        elif path_type == PATH_TYPE_OPEN_FILES:
            path = self._get_open_files_path()
        elif path_type == PATH_TYPE_OPEN_DIR:
            path = self._get_open_dir_path()
        elif path_type == PATH_TYPE_SAVE_FILE:
            path = self._get_save_file_path()
        elif path_type == PATH_TYPE_SAVE_DIR:
            path = self._get_save_dir_path()
        else:
            path = None
        if not path:
            return
        self.set_value(path)

    def _get_open_file_path(self) -> str:
        dialog_title = self._args.dialog_title
        start_path = self._args.start_path
        filters = self._args.filters
        init_filter = self._args.init_filter

        path, _ = QFileDialog.getOpenFileName(
            caption=dialog_title,
            directory=start_path,
            filter=filters,
            initialFilter=init_filter,
        )
        if not path:
            return ""
        return os.path.abspath(path)

    def _get_save_file_path(self) -> Optional[str]:
        dialog_title = self._args.dialog_title
        start_path = self._args.start_path
        filters = self._args.filters
        init_filter = self._args.init_filter

        path, _ = QFileDialog.getSaveFileName(
            caption=dialog_title,
            directory=start_path,
            filter=filters,
            initialFilter=init_filter,
        )
        if not path:
            return None
        return os.path.abspath(path)

    def _get_open_dir_path(self) -> Optional[str]:
        dialog_title = self._args.dialog_title
        start_path = self._args.start_path
        path = QFileDialog.getExistingDirectory(
            caption=dialog_title, directory=start_path
        )
        if not path:
            return None
        return os.path.abspath(path)

    def _get_open_files_path(self) -> Optional[str]:
        dialog_title = self._args.dialog_title
        start_path = self._args.start_path
        filters = self._args.filters
        init_filter = self._args.init_filter
        path_delimiter = self._args.path_delimiter or PATH_DELIMITER

        paths, _ = QFileDialog.getOpenFileNames(
            caption=dialog_title,
            directory=start_path,
            filter=filters,
            initialFilter=init_filter,
        )
        if not paths:
            return None
        return path_delimiter.join((os.path.abspath(path) for path in paths))

    def _get_save_dir_path(self) -> Optional[str]:
        dialog_title = self._args.dialog_title
        start_path = self._args.start_path
        path = QFileDialog.getExistingDirectory(
            caption=dialog_title, directory=start_path
        )
        if not path:
            return None
        return os.path.abspath(path)
