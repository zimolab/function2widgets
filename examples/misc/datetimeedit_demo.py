from examples.context import ExampleContext
from function2widgets import DateTimeEditArgs, DateTimeEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = DateTimeEditArgs(
            parameter_name="arg1",
            calendar_popup=True,
        )
        edit = DateTimeEdit(args)

        ctx.add_widget(edit)
        # start the qt application
        ctx.exec()
