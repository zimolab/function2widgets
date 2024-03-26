import os.path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QFileDialog,
    QApplication,
)

from function2widgets.widgets.base import CommonParameterWidget

PATH_TYPE_OPEN_FILE = 0
PATH_TYPE_OPEN_FILES = 1
PATH_TYPE_OPEN_DIR = 2
PATH_TYPE_SAVE_FILE = 3
PATH_TYPE_SAVE_DIR = 4

FILTER_ALL_FILES = QApplication.tr("All Files (*)")

PATH_DELIMITER = ";"


class PathEdit(CommonParameterWidget):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        default: Optional[str] = "",
        select_button_text: str = None,
        path_type: int = PATH_TYPE_OPEN_FILE,
        filters: str = FILTER_ALL_FILES,
        init_filter: str = None,
        start_path: str = None,
        path_delimiter: str = PATH_DELIMITER,
        placeholder: str = None,
        clear_button: bool = False,
        dialog_title: str = None,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):

        self._value_widget: Optional[QLineEdit] = None
        self._select_button: Optional[QPushButton] = None

        self._placeholder = placeholder or ""
        self._clear_button = clear_button
        self._button_text = select_button_text or QApplication.tr("Select")
        self._path_type = path_type
        self._filters = filters or FILTER_ALL_FILES
        self._init_filter = init_filter or ""
        self._start_path = start_path or "./"
        self._path_delimiter = path_delimiter or PATH_DELIMITER
        self._dialog_title = dialog_title or QApplication.tr("Select Path")

        super().__init__(
            default=default,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )
        if self._set_default_on_init:
            self.set_value(self.default)

    # noinspection PyUnresolvedReferences
    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QHBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._value_widget = QLineEdit(center_widget)
        self._select_button = QPushButton(self._button_text, center_widget)

        self._value_widget.setPlaceholderText(self._placeholder)
        self._value_widget.setClearButtonEnabled(self._clear_button)

        self._select_button.clicked.connect(self.select_path)

        center_widget_layout.addWidget(self._value_widget)
        center_widget_layout.addWidget(self._select_button)

        center_widget_layout.setStretch(0, 8)
        center_widget_layout.setStretch(1, 2)

    def get_value(self, *args, **kwargs) -> Optional[str]:
        if self._is_use_default():
            return self.default
        return self._value_widget.text()

    def set_value(self, value: Optional[str], *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setText(value or "")

    def select_path(self):
        if self._path_type == PATH_TYPE_OPEN_FILE:
            path = self._get_open_file_path()
        elif self._path_type == PATH_TYPE_OPEN_FILES:
            path = self._get_open_files_path()
        elif self._path_type == PATH_TYPE_OPEN_DIR:
            path = self._get_open_dir_path()
        elif self._path_type == PATH_TYPE_SAVE_FILE:
            path = self._get_save_file_path()
        elif self._path_type == PATH_TYPE_SAVE_DIR:
            path = self._get_save_dir_path()
        else:
            path = None
        if not path:
            return
        self.set_value(path)

    def _get_open_file_path(self) -> str:
        path, _ = QFileDialog.getOpenFileName(
            caption=self._dialog_title,
            directory=self._start_path,
            filter=self._filters,
            initialFilter=self._init_filter,
        )
        if not path:
            return ""
        return os.path.abspath(path)

    def _get_save_file_path(self) -> Optional[str]:
        path, _ = QFileDialog.getSaveFileName(
            caption=self._dialog_title,
            directory=self._start_path,
            filter=self._filters,
            initialFilter=self._init_filter,
        )
        if not path:
            return None
        return os.path.abspath(path)

    def _get_open_dir_path(self) -> Optional[str]:
        path = QFileDialog.getExistingDirectory(
            caption=self._dialog_title, directory=self._start_path
        )
        if not path:
            return None
        return os.path.abspath(path)

    def _get_open_files_path(self) -> Optional[str]:
        paths, _ = QFileDialog.getOpenFileNames(
            caption=self._dialog_title,
            directory=self._start_path,
            filter=self._filters,
            initialFilter=self._init_filter,
        )
        if not paths:
            return None
        return self._path_delimiter.join((os.path.abspath(path) for path in paths))

    def _get_save_dir_path(self) -> Optional[str]:
        path = QFileDialog.getExistingDirectory(
            caption=self._dialog_title, directory=self._start_path
        )
        if not path:
            return None
        return os.path.abspath(path)


class FilePathEdit(PathEdit):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        default: Optional[str] = "",
        select_button_text: str = None,
        save_file: bool = False,
        multiple_files: bool = False,
        filters: str = FILTER_ALL_FILES,
        init_filter: str = None,
        start_path: str = None,
        path_delimiter: str = PATH_DELIMITER,
        placeholder: str = None,
        clear_button: bool = False,
        dialog_title: str = None,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):
        if save_file:
            path_type = PATH_TYPE_SAVE_FILE
        elif multiple_files:
            path_type = PATH_TYPE_OPEN_FILES
        else:
            path_type = PATH_TYPE_OPEN_FILE

        super().__init__(
            default=default,
            select_button_text=select_button_text,
            path_type=path_type,
            filters=filters,
            init_filter=init_filter,
            start_path=start_path,
            path_delimiter=path_delimiter,
            placeholder=placeholder,
            clear_button=clear_button,
            dialog_title=dialog_title,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )


class DirPathEdit(PathEdit):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    def __init__(
        self,
        default: Optional[str] = "",
        select_button_text: str = None,
        save_dir: bool = False,
        start_path: str = None,
        placeholder: str = None,
        clear_button: bool = False,
        dialog_title: str = None,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):
        if save_dir:
            path_type = PATH_TYPE_SAVE_DIR
        else:
            path_type = PATH_TYPE_OPEN_DIR

        super().__init__(
            default=default,
            select_button_text=select_button_text,
            path_type=path_type,
            filters="",
            init_filter=None,
            start_path=start_path,
            path_delimiter="",
            placeholder=placeholder,
            clear_button=clear_button,
            dialog_title=dialog_title,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )


def __test_main():
    from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

    app = QApplication([])
    win = QWidget()
    layout = QVBoxLayout(win)
    win.setLayout(layout)

    path_edit = PathEdit(
        default="./",
        placeholder="select path",
        parent=win,
    )
    path_edit.set_label("PathEdit")
    print(path_edit.get_value())

    file_path_edit = FilePathEdit(
        default="abc",
        save_file=True,
        placeholder="select file path",
        parent=win,
    )
    file_path_edit.set_label("FilePathEdit")

    files_path_edit = FilePathEdit(
        default=None, multiple_files=True, placeholder="select files path", parent=win
    )
    files_path_edit.set_label("FilesPathEdit")

    dir_path_edit = DirPathEdit(placeholder="select dir path", parent=win)
    dir_path_edit.set_label("DirPathEdit")

    save_dir_path_edit = DirPathEdit(
        default=None, save_dir=True, placeholder="select save dir path", parent=win
    )
    save_dir_path_edit.set_label("DirPathEdit")

    layout.addWidget(path_edit)
    layout.addWidget(file_path_edit)
    layout.addWidget(files_path_edit)
    layout.addWidget(dir_path_edit)
    layout.addWidget(save_dir_path_edit)

    win.show()
    app.exec()


if __name__ == "__main__":
    __test_main()
