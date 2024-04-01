from examples.context import ExampleContext
from function2widgets.widgets.misc import DateEditArgs, DateEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = DateEditArgs(parameter_name="arg1", calendar_popup=True)
        edit = DateEdit(args)

        ctx.add_widget(edit)
        # start the qt application
        ctx.exec()
