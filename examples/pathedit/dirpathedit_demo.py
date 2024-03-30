from examples.context import ExampleContext
from function2widgets.widgets.pathedit import (
    DirPathEditArgs,
    DirPathEdit,
)

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = DirPathEditArgs(
            parameter_name="arg1",
            save_dir=True,
        )
        edit1 = DirPathEdit(args)

        args2 = DirPathEditArgs(
            parameter_name="arg2",
            button_text="选择目录",
            save_dir=False,
            default=None,
        )

        edit2 = DirPathEdit(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(edit1)
        ctx.add_widget(edit2)
        # start the qt application
        ctx.exec()
