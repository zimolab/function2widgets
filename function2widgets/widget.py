import abc
from typing import Any

from PyQt6.QtWidgets import QWidget


class InvalidValueError(ValueError):
    pass


class BaseParameterWidget(QWidget):

    def __init__(self, default: Any, parent: QWidget | None, stylesheet: str | None):
        super().__init__(parent)
        self._default = default
        self._parameter_name: str | None = None

        if stylesheet is not None:
            self.setStyleSheet(stylesheet)

    @property
    def parameter_name(self) -> str | None:
        return self._parameter_name

    @parameter_name.setter
    def parameter_name(self, parameter_name: str | None):
        self._parameter_name = parameter_name

    @abc.abstractmethod
    def get_value(self, *args, **kwargs) -> Any:
        pass

    @abc.abstractmethod
    def set_value(self, value: Any, *args, **kwargs):
        pass

    @property
    def default(self) -> Any:
        return self._default

    @abc.abstractmethod
    def set_label(self, label_text: str):
        pass

    @abc.abstractmethod
    def get_label(self, label_text) -> str:
        pass

    @abc.abstractmethod
    def set_docstring(self, docstring: str):
        pass

    @abc.abstractmethod
    def get_docstring(self) -> str:
        pass

    @abc.abstractmethod
    def show_label(self, show: bool):
        pass

    @abc.abstractmethod
    def show_docstring(self, show: bool):
        pass
