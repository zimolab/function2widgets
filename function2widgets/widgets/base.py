import abc
from typing import Any

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox, QHBoxLayout

from function2widgets.widget import BaseParameterWidget, InvalidValueError


class CommonParameterWidget(BaseParameterWidget):
    def __init__(self, default: Any, parent: QWidget | None):
        super().__init__(default=default, parent=parent)

        self._layout_main = QGridLayout(self)
        self._label_widget = QLabel(self)
        self._label_widget.setText(self.tr("parameter name"))
        self._docstring_widget = QLabel(self)
        self._center_widget = QWidget(self)
        self._checkbox_use_default = QCheckBox(self)
        self._checkbox_use_default.setText(self.tr("use default value"))

        self.setup_use_default_checkbox()
        self.setup_layout()
        self.setup_center_widget(self._center_widget)

    def setup_use_default_checkbox(self):
        self._checkbox_use_default.setText(self.tr("default(%s)" % repr(self.default)))
        self._checkbox_use_default.setEnabled(True)
        # noinspection PyUnresolvedReferences
        self._checkbox_use_default.toggled.connect(
            self._on_use_default_checkbox_toggled
        )

    def _on_use_default_checkbox_toggled(self, checked):
        if checked:
            self._center_widget.setEnabled(False)
        else:
            self._center_widget.setEnabled(True)

    @property
    def label_widget(self) -> QLabel:
        return self._label_widget

    @property
    def docstring_widget(self) -> QLabel:
        return self._docstring_widget

    def setup_layout(self):
        self._layout_main.setObjectName("layout_main")
        self._label_widget.setObjectName("label_widget")
        self._docstring_widget.setObjectName("docstring_widget")
        self._center_widget.setObjectName("center_widget")

        self._checkbox_use_default.setObjectName("checkbox_use_default")
        checkboxes_layout = QHBoxLayout(self)
        checkboxes_layout.addWidget(self._checkbox_use_default)
        self._checkbox_use_default.setChecked(False)

        # label_widget在第一行第一列
        self._layout_main.addWidget(self._label_widget, 0, 0, 1, 1)
        # checkboxes_layout在第一行第二列
        self._layout_main.addLayout(checkboxes_layout, 0, 1, 1, 1)
        # center_widget占满第二行
        self._layout_main.addWidget(self._center_widget, 1, 0, 1, 2)
        # docstring_widget占满第三行
        self._layout_main.addWidget(self._docstring_widget, 2, 0, 1, 2)
        self.setLayout(self._layout_main)

    @abc.abstractmethod
    def setup_center_widget(self, center_widget: QWidget):
        pass

    def _is_use_default(self) -> bool:
        return self._checkbox_use_default.isChecked()

    def _set_use_default(self):
        self._checkbox_use_default.setChecked(True)

    def _pre_set_value(self, value: Any) -> bool:

        if value is None:
            if self.default is None:
                self._set_use_default()
                return False
            else:
                raise InvalidValueError(
                    self.tr(
                        "invalid value: value cannot be None unless default value is None"
                    )
                )

        if value == self.default:
            self._set_use_default()
        else:
            self._unset_use_default()
        return True

    def _unset_use_default(self):
        self._checkbox_use_default.setChecked(False)

    def set_label(self, label_text):
        self.label_widget.setText(label_text)

    def get_label(self, label_text):
        return self.label_widget.text()

    def set_docstring(self, docstring: str):
        self.docstring_widget.setText(docstring)

    def get_docstring(self) -> str:
        return self.docstring_widget.text()

    def show_label(self, show: bool):
        self.label_widget.setVisible(show is True)

    def show_docstring(self, show):
        self.docstring_widget.setVisible(show is True)
