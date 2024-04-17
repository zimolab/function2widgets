from typing import Optional, List, Tuple

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLayout,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QMessageBox,
)

from function2widgets import BaseParameterWidget


class ExampleContext(object):
    def __init__(
        self,
        argv: List[str] = None,
        window_title: str = None,
        window_size: Tuple[int, int] = None,
    ):
        self._application: Optional[QApplication] = None
        self._example_window: Optional[QWidget] = None
        self._layout: Optional[QLayout] = None

        self._scrollarea: Optional[QScrollArea] = None
        self._widget_parameters: Optional[QWidget] = None
        self._layout_parameters: Optional[QLayout] = None
        self._button_get_parameter_values: Optional[QPushButton] = None

        self._argv = argv or []
        self._window_size = window_size
        self._window_title = window_title or "Parameter Widget Example"

    def prepare(self):
        if isinstance(self._application, QApplication):
            return
        self._application = QApplication(self._argv)
        if self._example_window is not None:
            self._example_window.close()
            self._example_window.deleteLater()
            self._example_window = None
        self._example_window = QWidget()
        if self._window_size is not None:
            self._example_window.resize(*self._window_size)
        if self._window_title is not None:
            self._example_window.setWindowTitle(self._window_title)
        self._layout = QVBoxLayout(self._example_window)
        self._example_window.setLayout(self._layout)

        self._scrollarea = QScrollArea(self._example_window)
        self._scrollarea.setWidgetResizable(True)
        self._widget_parameters = QWidget(self._scrollarea)
        self._scrollarea.setWidget(self._widget_parameters)

        self._layout_parameters = QVBoxLayout(self._widget_parameters)
        self._widget_parameters.setLayout(self._layout_parameters)

        self._button_get_parameter_values = QPushButton(
            "Get Parameter Values", self._example_window
        )
        # noinspection PyUnresolvedReferences
        self._button_get_parameter_values.clicked.connect(self.get_parameter_values)

        self._layout.addWidget(self._scrollarea)
        self._layout.addWidget(self._button_get_parameter_values)

    def dispose(self):
        if self._example_window is not None:
            self._example_window.close()
            self._example_window.deleteLater()
            self._example_window = None

        if self._application is not None:
            self._application.quit()
            self._application = None

        self._layout = None
        self._layout_parameters = None
        self._widget_parameters = None
        self._button_get_parameter_values = None

    def add_widget(self, widget: BaseParameterWidget):
        self._layout_parameters.addWidget(widget)

    def exec(self):
        self._example_window.show()
        self._application.exec()

    def get_parameter_values(self):
        values = {}
        # 遍历布局中的所有控件，获取其值
        for i in range(self._layout_parameters.count()):
            item = self._layout_parameters.itemAt(i)
            widget = item.widget()
            if not isinstance(widget, BaseParameterWidget):
                continue
            values[widget.parameter_name] = widget.get_value()
        msg = "current parameter values:\n\n"
        for key, value in values.items():
            msg += f"{key}: {value}\n"
        msg += "\n"
        QMessageBox.information(self._example_window, "Parameter Values", msg)

    def __enter__(self):
        self.prepare()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dispose()
