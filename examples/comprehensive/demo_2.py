from typing import Literal

from examples.context import ExampleContext
from function2widgets.factory import ParameterWidgetFactory
from function2widgets.parser.function_parser import FunctionInfoParser


def demo2(
    a: int = 10,
    b: int = 180,
    c: int = 50,
    d: float = 0.1,
    f: Literal["opt1", "opt2", "opt3"] = "opt2",
    g: str = "",
):
    """

    :param a:
    :param b:
    :param c:
    :param d:
    :param f:
    :param g:
    :return:

    @widgets
    [a]
    widget_class="IntSpinBox"
    min_value=10
    max_value=15

    [b]
    widget_class="Dial"
    show_value_label=true

    [c]
    widget_class="Slider"
    show_value_label=true
    tracking=true

    [d]
    widget_class="FloatSpinBox"
    decimals=5
    step=0.00001

    [f]
    label="label for f"
    default="opt1"

    [g]
    widget_class="ComboBoxEdit"

    @end

    """
    pass


if __name__ == "__main__":
    with ExampleContext() as ctx:
        parser = FunctionInfoParser()
        func_info = parser.parse(demo2)
        factory = ParameterWidgetFactory()
        widgets = factory.create_widgets_for_function(func_info)
        # start the qt application
        for widget in widgets.values():
            ctx.add_widget(widget)
        ctx.exec()
