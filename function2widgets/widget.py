import abc
from typing import Any, Optional

from PyQt6.QtWidgets import QWidget


class InvalidValueError(ValueError):
    pass


class BaseParameterWidget(QWidget):
    """
    参数控件基类：函数参数所对应的控件类型均必须继承自此类，用于实现参数控件的通用功能
    """

    SET_DEFAULT_ON_INIT: bool = False

    def __init__(
        self,
        default: Any,
        stylesheet: Optional[str],
        set_default_on_init: Optional[bool],
        parent: Optional[QWidget],
    ):
        super().__init__(parent)
        self._default = default
        self._parameter_name: Optional[str] = None
        if set_default_on_init is None:
            self._set_default_on_init = self.SET_DEFAULT_ON_INIT
        else:
            self._set_default_on_init = set_default_on_init

        if stylesheet is not None:
            self.setStyleSheet(stylesheet)

    @property
    def parameter_name(self) -> Optional[str]:
        """
        获取参数名称
        :return:
        """
        return self._parameter_name

    @parameter_name.setter
    def parameter_name(self, parameter_name: Optional[str]):
        """
        设置参数名称
        :param parameter_name:
        :return:
        """
        self._parameter_name = parameter_name

    @abc.abstractmethod
    def get_value(self, *args, **kwargs) -> Any:
        """
        抽象方法：获取参数值
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abc.abstractmethod
    def set_value(self, value: Any, *args, **kwargs):
        """
        抽象方法：设置参数值
        :param value:
        :param args:
        :param kwargs:
        :return:
        """
        pass

    @property
    def default(self) -> Any:
        """
        获取参数默认值
        :return:
        """
        return self._default

    @abc.abstractmethod
    def set_label(self, label_text: str):
        """
        设置参数标签文本
        :param label_text:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_label(self) -> str:
        """
        获取参数标签文本
        :return:
        """
        pass

    @abc.abstractmethod
    def set_docstring(self, docstring: str):
        """
        设置参数文档字符串
        :param docstring:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_docstring(self) -> str:
        """
        获取参数文档字符串
        :return:
        """
        pass

    @abc.abstractmethod
    def show_label(self, show: bool):
        """
        设置是否显示参数的标签
        :param show:
        :return:
        """
        pass

    @abc.abstractmethod
    def show_docstring(self, show: bool):
        """
        设置是否显示参数的文档字符串、
        :param show:
        :return:
        """
        pass
