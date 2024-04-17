from examples.context import ExampleContext
from function2widgets import PlainTextEditArgs, PlainTextEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = PlainTextEditArgs(parameter_name="arg1")
        edit1 = PlainTextEdit(args)

        args2 = PlainTextEditArgs(
            parameter_name="arg2",
            default=None,
        )

        edit2 = PlainTextEdit(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(edit1)
        ctx.add_widget(edit2)
        # start the qt application
        ctx.exec()
