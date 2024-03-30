from examples.context import ExampleContext
from function2widgets.widgets.editor import JsonEditorArgs, JsonEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = JsonEditorArgs(
            parameter_name="arg1",
            default="",
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=False,
        )
        editor = JsonEditor(args)

        args_2 = JsonEditorArgs(
            parameter_name="arg2",
            default=None,
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=True,
        )

        editor2 = JsonEditor(args_2)

        # add parameter widgets to the layout
        ctx.add_widget(editor)
        ctx.add_widget(editor2)
        # start the qt application
        ctx.exec()
