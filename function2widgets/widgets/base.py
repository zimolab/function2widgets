import abc
import logging
from typing import Any, Optional

from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QCheckBox, QHBoxLayout

from function2widgets.widget import BaseParameterWidget, InvalidValueError


class CommonParameterWidget(BaseParameterWidget):
    HIDE_USE_DEFAULT_CHECKBOX = False

    def __init__(
        self,
        default: Any,
        stylesheet: str,
        set_default_on_init: Optional[bool],
        hide_use_default_checkbox: Optional[bool],
        parent: Optional[QWidget],
    ):
        """
        Note:
        1. if 'set_default_on_init' is None, it will be set to class field SET_DEFAULT_ON_INIT
        2. if 'hide_use_default_checkbox' is None, it will be set to class field HIDE_USE_DEFAULT_CHECKBOX
        3. 'set_default_on_init' will be set to True if 'default' is not None and 'hide_use_default_checkbox' is True
        4. 'hide_use_default_checkbox' will be set to False if 'default' is None

        :param default:
        :param stylesheet:
        :param set_default_on_init:
        :param hide_use_default_checkbox:
        :param parent:
        """
        if set_default_on_init is None:
            logging.debug("set_default_on_init will be set to SET_DEFAULT_ON_INIT")
            set_default_on_init = self.SET_DEFAULT_ON_INIT

        if hide_use_default_checkbox is None:
            logging.debug(
                "hide_use_default_checkbox will be set to HIDE_USE_DEFAULT_CHECKBOX"
            )
            hide_use_default_checkbox = self.HIDE_USE_DEFAULT_CHECKBOX

        self._hide_use_default_checkbox = hide_use_default_checkbox

        if default is None:
            logging.debug(
                "hide_use_default_checkbox will be set to False because default is None"
            )
            self._hide_use_default_checkbox = False

        if self._hide_use_default_checkbox and default is not None:
            logging.debug(
                "set_set_default_on_init will be set to True because hide_use_default_checkbox is True and default is not None"
            )
            set_default_on_init = True

        super().__init__(
            default=default,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            parent=parent,
        )

        self._layout_main = QGridLayout(self)
        self._label_widget = QLabel(self)
        self._label_widget.setText(self.tr("parameter name"))
        self._docstring_widget = QLabel(self)
        self._center_widget = QWidget(self)
        self._use_default_checkbox = QCheckBox(self)

        self.setup_use_default_checkbox()
        self.setup_layout()
        self.setup_center_widget(self._center_widget)

    def set_label(self, label_text):
        self.label_widget.setText(label_text)

    def get_label(self):
        return self.label_widget.text()

    def set_docstring(self, docstring: str):
        self.docstring_widget.setText(docstring)

    def get_docstring(self) -> str:
        return self.docstring_widget.text()

    def show_label(self, show: bool):
        self.label_widget.setVisible(show is True)

    def show_docstring(self, show):
        self.docstring_widget.setVisible(show is True)

    def setup_use_default_checkbox(self):
        self._use_default_checkbox.setText(
            self.tr("default({})".format(repr(self.default)))
        )
        self._use_default_checkbox.setEnabled(True)
        # noinspection PyUnresolvedReferences
        self._use_default_checkbox.toggled.connect(
            self._on_use_default_checkbox_toggled
        )
        if self._hide_use_default_checkbox:
            self._use_default_checkbox.setVisible(False)

    def _on_use_default_checkbox_toggled(self, checked):
        if self._hide_use_default_checkbox:
            return
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

        self._use_default_checkbox.setObjectName("checkbox_use_default")
        checkboxes_layout = QHBoxLayout(self)
        checkboxes_layout.addWidget(self._use_default_checkbox)
        self._use_default_checkbox.setChecked(False)

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
        return self._use_default_checkbox.isChecked()

    def _set_use_default(self):
        self._use_default_checkbox.setChecked(True)

    def _unset_use_default(self):
        self._use_default_checkbox.setChecked(False)

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
