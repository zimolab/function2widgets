from examples.context import ExampleContext
from function2widgets.widgets.pathedit import (
    PathEdit,
    PathEditArgs,
    PATH_TYPE_OPEN_FILES,
)

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = PathEditArgs(
            parameter_name="arg1",
            button_text="Select",
            path_type=PATH_TYPE_OPEN_FILES,
            filters="All Files (*)",
            init_filter="",
            start_path="./",
            path_delimiter="",
            placeholder="",
            clear_button=True,
            dialog_title="Select Path",
        )
        edit1 = PathEdit(args)

        args2 = PathEditArgs(
            parameter_name="arg2",
            default=None,
        )

        edit2 = PathEdit(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(edit1)
        ctx.add_widget(edit2)
        # start the qt application
        ctx.exec()
