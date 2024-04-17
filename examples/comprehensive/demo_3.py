from datetime import datetime, date, time

from examples.context import ExampleContext
from function2widgets import FunctionInfoParser, ParameterWidgetFactory, Color


def demo3(a: datetime, b: date, c: time, d: Color):
    """
    @widgets
    [a]
    display_format = "yyyy-MM-dd HH:mm"
    calendar_popup = true
    min_datetime = "2021-11-22 10:10"
    max_datetime = "2024-12-21 10:10"

    [b]
    display_format = "yyyy年MM月dd日"
    calendar_popup = true
    min_date = "2021年11月22日"
    max_date = "2024年12月21日"

    [c]
    display_format = "HH:mm"
    min_time = "8:30"
    max_time = "17:30"

    [d]
    with_alpha=false

    @end

    """
    pass


if __name__ == "__main__":
    with ExampleContext() as ctx:
        parser = FunctionInfoParser()
        func_info = parser.parse(demo3)
        factory = ParameterWidgetFactory()
        widgets = factory.create_widgets_for_function(func_info)
        # start the qt application
        for widget in widgets.values():
            ctx.add_widget(widget)
        ctx.exec()
