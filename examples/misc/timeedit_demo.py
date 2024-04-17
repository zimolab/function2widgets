from examples.context import ExampleContext
from function2widgets import TimeEditArgs, TimeEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = TimeEditArgs(
            parameter_name="arg1",
        )
        edit = TimeEdit(args)

        ctx.add_widget(edit)
        # start the qt application
        ctx.exec()
