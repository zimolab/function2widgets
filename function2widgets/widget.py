import abc
import dataclasses
from typing import Any, Optional, Type, Dict

from PyQt6.QtWidgets import QWidget


class InvalidValueError(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class BaseWidgetArgs(object):
    parameter_name: str
    default: Any
    label: Optional[str]
    description: Optional[str]
    stylesheet: Optional[str]
    set_default_on_init: Optional[bool]
    hide_default_value_widget: Optional[bool]
    default_value_description: Optional[str]

    @classmethod
    def new(cls, kwargs: Dict[str, Any]) -> "BaseWidgetArgs":
        return cls(**kwargs)


class BaseParameterWidget(QWidget):
    """
    base class of all parameter widgets
    """

    SET_DEFAULT_ON_INIT: bool = True
    HIDE_DEFAULT_VALUE_WIDGET: bool = False

    _WidgetArgsClass = BaseWidgetArgs

    def __init__(self, args: BaseWidgetArgs, parent: Optional[QWidget]):
        super().__init__(parent)

        """
        Note:
        1. if 'set_default_on_init' is None, it will be set to class field SET_DEFAULT_ON_INIT
        2. if 'hide_default_value_widget' is None, it will be set to class field HIDE_DEFAULT_VALUE_WIDGET
        3. 'set_default_on_init' will be set to True if 'default' is not None and 'hide_default_value_widget' is True
        4. 'hide_value_default_widget' will be set to False if 'default' is None
        5. 'label' will be set to 'parameter_name', if it is set to None
        """
        # 1
        if args.set_default_on_init is None:
            set_default_on_init = self.__class__.SET_DEFAULT_ON_INIT
        else:
            set_default_on_init = args.set_default_on_init
        # 2
        if args.hide_default_value_widget is None:
            hide_default_value_widget = self.__class__.HIDE_DEFAULT_VALUE_WIDGET
        else:
            hide_default_value_widget = args.hide_default_value_widget
        # 3
        if args.default is not None and hide_default_value_widget is True:
            set_default_on_init = True
        # 4
        if args.default is None:
            hide_default_value_widget = False
        # 5
        if args.label is None:
            label = args.parameter_name
        else:
            label = args.label

        self.__args = dataclasses.replace(
            args,
            label=label,
            set_default_on_init=set_default_on_init,
            hide_default_value_widget=hide_default_value_widget,
        )

        if self.__args.stylesheet is not None:
            self.setStyleSheet(self.__args.stylesheet)

    @property
    def _args(self) -> BaseWidgetArgs:
        """
        this is for internal use, do not access in user code
        :return:
        """
        return self.__args

    @property
    def parameter_name(self) -> Optional[str]:
        """
        get the parameter name
        :return:
        """
        return self._args.parameter_name

    @abc.abstractmethod
    def get_value(self) -> Any:
        """
        abstract method: get the value of the parameter
        :return:
        """
        pass

    @abc.abstractmethod
    def set_value(self, value: Any):
        """
        abstract method: get the value to the parameter
        :param value:
        :return:
        """
        pass

    @property
    def default(self) -> Any:
        """
        get the default value of the parameter
        :return:
        """
        return self._args.default

    @abc.abstractmethod
    def set_label(self, label: Optional[str]):
        """
        set the label of the parameter
        :param label:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_label(self) -> Optional[str]:
        """
        get the label of the parameter
        :return:
        """
        pass

    @abc.abstractmethod
    def set_description(self, desc: Optional[str]):
        """
        set the description of the parameter
        :param desc:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_description(self) -> Optional[str]:
        """
        get the description of the parameter
        :return:
        """
        pass

    @classmethod
    def widget_args_class(cls) -> Type[BaseWidgetArgs]:
        """
        get the WidgetArgs class which can be used to initialize the parameter widget
        :return:
        """
        return cls._WidgetArgsClass
