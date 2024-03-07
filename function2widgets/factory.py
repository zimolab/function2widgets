from typing import Type

from function2widgets.common import AlreadyRegisteredError, NotRegisteredError
from function2widgets.description import ParameterDescription
from function2widgets.widget import BaseParameterWidget
from function2widgets.widgets.allwidgets import BASIC_PARAMETER_WIDGETS


class ParameterWidgetFactory(object):
    def __init__(self, enable_basic_type_widgets: bool = True):
        self._widget_classes = {}

        if enable_basic_type_widgets:
            self.register_all(BASIC_PARAMETER_WIDGETS)

    def register(self, widget_type: str, widget_class: Type[BaseParameterWidget]):
        if widget_type in self._widget_classes:
            raise AlreadyRegisteredError(f"widget type {widget_type} already registered")
        self._widget_classes[widget_type] = widget_class

    def register_all(self, widgets: dict[str, Type[BaseParameterWidget]]):
        for widget_type, widget_class in widgets.items():
            self.register(widget_type, widget_class)

    def unregister(self, widget_type: str):
        if widget_type not in self._widget_classes:
            raise NotRegisteredError(f"widget type {widget_type} not registered")
        del self._widget_classes[widget_type]

    def is_registered(self, widget_type: str) -> bool:
        return widget_type in self._widget_classes

    def get_widget_class(self, widget_type: str) -> Type[BaseParameterWidget]:
        if not self.is_registered(widget_type):
            raise NotRegisteredError(f"widget type {widget_type} not registered")
        return self._widget_classes[widget_type]

    def clear(self):
        self._widget_classes.clear()

    def create_widget(self, widget_type: str, **kwargs) -> BaseParameterWidget:
        widget_class = self.get_widget_class(widget_type)
        return widget_class(**kwargs)

    def create_widget_from_description(self, param_description: ParameterDescription) -> BaseParameterWidget:
        widget_description = param_description.widget

        if not widget_description:
            widget_type = param_description.type
            widget_label = param_description.name
            widget_docstring = ""
            show_label = True
            show_docstring = True
            widget_init_args = {}
        else:
            widget_type = widget_description.type
            widget_label = widget_description.label
            show_label = widget_description.show_label
            show_docstring = widget_description.show_docstring
            widget_docstring = widget_description.docstring
            widget_init_args = widget_description.init_args

        widget_type = widget_type or param_description.type

        args = {
            "default": param_description.default,
            "parent": None,
            **widget_init_args
        }
        widget = self.create_widget(widget_type, **args)
        widget.parameter_name = param_description.name
        widget.set_label(widget_label or "")
        widget.set_docstring(widget_docstring or "")
        widget.show_label(show_label)
        widget.show_docstring(show_docstring)
        return widget
