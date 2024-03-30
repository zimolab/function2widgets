from examples.context import ExampleContext
from function2widgets.widgets.editor import CodeEditor, CodeEditorArgs

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = CodeEditorArgs(
            parameter_name="arg1",
            default="",
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=False,
        )
        editor = CodeEditor(args)

        args_2 = CodeEditorArgs(
            parameter_name="arg2",
            default=None,
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=True,
        )

        editor2 = CodeEditor(args_2)

        # add parameter widgets to the layout
        ctx.add_widget(editor)
        ctx.add_widget(editor2)
        # start the qt application
        ctx.exec()
