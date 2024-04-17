from examples.context import ExampleContext
from function2widgets import FunctionInfoParser, ParameterWidgetFactory


def demo1(
    a: int, b: float, c: bool, d: str, e: list, f: tuple, g: dict = None, h: any = 100
):
    """

    :param a: the output destination of encoded output file.the output destination of encoded output file
    :param b:  <b>param b</b><br><font color=red><b>rich text here</b></font>
    :param c:
    :param d:
    :param e:
    :param f:
    :param g:
    :param h:
    :return:
    """
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
