from typing import Type, Dict

from PyQt6.QtWidgets import QApplication

from function2widgets.common import (
    AlreadyRegisteredError,
    NotRegisteredError,
)
from function2widgets.info import ParameterInfo, FunctionInfo
from function2widgets.parser.function_parser import FunctionInfoParser
from function2widgets.widget import BaseParameterWidget, WidgetArgs
from function2widgets.widgets.allwidgets import BASIC_PARAMETER_WIDGETS


class ParameterWidgetFactory(object):
    def __init__(self, register_basic_parameter_widgets: bool = True):
        self._widget_classes = {}

        if register_basic_parameter_widgets:
            self.register_all(BASIC_PARAMETER_WIDGETS)

    def register(self, widget_class_name: str, widget_class: Type[BaseParameterWidget]):
        if widget_class_name in self._widget_classes:
            raise AlreadyRegisteredError(
                QApplication.tr(f"widget type {widget_class_name} already registered")
            )
        self._widget_classes[widget_class_name] = widget_class

    def register_all(self, widgets: Dict[str, Type[BaseParameterWidget]]):
        for widget_class_name, widget_class in widgets.items():
            self.register(widget_class_name, widget_class)

    def unregister(self, widget_class_name: str):
        if widget_class_name not in self._widget_classes:
            raise NotRegisteredError(
                QApplication.tr(f"widget type {widget_class_name} not registered")
            )
        del self._widget_classes[widget_class_name]

    def is_registered(self, widget_class_name: str) -> bool:
        return widget_class_name in self._widget_classes

    def get_widget_class(self, widget_class_name: str) -> Type[BaseParameterWidget]:
        if not self.is_registered(widget_class_name):
            raise NotRegisteredError(
                QApplication.tr(f"widget type {widget_class_name} not registered")
            )
        return self._widget_classes[widget_class_name]

    def clear(self):
        self._widget_classes.clear()

    def create_widget_for_parameter(
        self, param_info: ParameterInfo
    ) -> BaseParameterWidget:
        param_widget_info = param_info.widget
        if not param_widget_info:
            param_widget_info = FunctionInfoParser.make_default_param_widget_info(
                param_info
            )

        widget = self._create_widget(
            widget_class_name=param_widget_info.widget_class,
            **param_widget_info.widget_args,
        )
        return widget

    def create_widgets_for_function(
        self, func_info: FunctionInfo
    ) -> Dict[str, BaseParameterWidget]:
        widgets = {}
        for param_info in func_info.parameters:
            widget = self.create_widget_for_parameter(param_info)
            widgets[param_info.name] = widget
        return widgets

    def _create_widget(self, widget_class_name: str, **kwargs) -> BaseParameterWidget:
        widget_class = self.get_widget_class(widget_class_name)
        widget_args_class: Type[WidgetArgs] = widget_class.widget_args_class()
        widget_args = widget_args_class.new(kwargs=kwargs)
        return widget_class(args=widget_args, parent=None)
