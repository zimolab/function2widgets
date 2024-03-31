from examples.context import ExampleContext
from function2widgets.factory import ParameterWidgetFactory
from function2widgets.parser.function_parser import FunctionInfoParser


def demo1(a: int, b: float, c: bool, d: str, e: list, f: tuple, g: dict, h: any):
    pass


if __name__ == "__main__":
    with ExampleContext() as ctx:
        parser = FunctionInfoParser()
        func_info = parser.parse(demo1)
        factory = ParameterWidgetFactory()
        widgets = factory.create_widgets_for_function(func_info)
        # start the qt application
        for widget in widgets.values():
            ctx.add_widget(widget)
        ctx.exec()
