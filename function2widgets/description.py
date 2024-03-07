import dataclasses
from typing import Any, OrderedDict


@dataclasses.dataclass
class WidgetDescription(object):
    type: str
    label: str = ""
    docstring: str = ""
    show_label: bool = True
    show_docstring: bool = True
    init_args: dict = dataclasses.field(default_factory=OrderedDict)


@dataclasses.dataclass
class ParameterDescription(object):
    name: str
    type: str
    type_extras: Any = None
    default: Any = None
    docstring: str | None = None
    widget: WidgetDescription | None = None


@dataclasses.dataclass
class FunctionDescription(object):
    """A description of a function."""
    name: str
    docstring: str
    parameters: list[ParameterDescription] = dataclasses.field(default_factory=list)
