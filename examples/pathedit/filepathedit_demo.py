from examples.context import ExampleContext
from function2widgets.widgets.pathedit import (
    FilePathEditArgs,
    FilePathEdit,
)

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = FilePathEditArgs(
            parameter_name="arg1",
            save_file=True,
        )
        edit1 = FilePathEdit(args)

        args2 = FilePathEditArgs(
            parameter_name="arg2",
            default=None,
        )

        edit2 = FilePathEdit(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(edit1)
        ctx.add_widget(edit2)
        # start the qt application
        ctx.exec()
