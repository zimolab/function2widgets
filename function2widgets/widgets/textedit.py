from typing import Any

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPlainTextEdit

from function2widgets.widgets._sourcecodeedit import _SourceCodeEdit
from function2widgets.widgets.base import CommonParameterWidget


class PlainTextEdit(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        self._value_widget: QPlainTextEdit | None = None

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        if self.SET_DEFAULT_ON_INIT:
            self.set_value(default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        self._value_widget = QPlainTextEdit(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget_layout.addWidget(self._value_widget)
        center_widget.setLayout(center_widget_layout)

    def get_value(self, *args, **kwargs) -> str | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.toPlainText()

    def set_value(self, value: Any, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setPlainText(str(value))


class SourceCodeEdit(CommonParameterWidget):
    SET_DEFAULT_ON_INIT = False

    def __init__(
        self,
        configs: dict = None,
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: _SourceCodeEdit | None = None
        self._configs = configs

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        if self.SET_DEFAULT_ON_INIT:
            self.set_value(default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._value_widget = _SourceCodeEdit(configs=self._configs)
        center_widget_layout.addWidget(self._value_widget)

    def get_value(self, *args, **kwargs) -> str | None:
        if self._is_use_default():
            return self._default
        return self._value_widget.text()

    def set_value(self, value: Any, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._value_widget.setText(str(value))


def __test_main():
    from PyQt6.QtWidgets import QApplication

    app = QApplication([])
    win = QWidget()
    layout = QVBoxLayout(win)
    win.setLayout(layout)

    edit = PlainTextEdit(default=None, parent=win)
    print(f"value: {edit.get_value()}")
    edit.set_value(123)
    print(f"value: {edit.get_value()}")
    edit.set_value(0.00001)
    print(f"value: {edit.get_value()}")
    edit.set_value("abc")
    print(f"value: {edit.get_value()}")
    edit.set_value(globals())
    print(f"value: {edit.get_value()}")
    edit.set_value(None)
    print(f"value: {edit.get_value()}")
    print()

    edit2 = PlainTextEdit(default=None, parent=win)

    code_edit = SourceCodeEdit(default=None, parent=win)
    print(f"value: {code_edit.get_value()}")
    code_edit.set_value("print('hello world')")
    print(f"value: {code_edit.get_value()}")
    print()

    code_edit2 = SourceCodeEdit(default=None, parent=win)

    layout.addWidget(edit)
    layout.addWidget(edit2)
    layout.addWidget(code_edit)
    layout.addWidget(code_edit2)

    win.show()

    app.exec()


if __name__ == "__main__":
    __test_main()
