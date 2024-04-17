from examples.context import ExampleContext
from function2widgets import ListEditorArgs, ListEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = ListEditorArgs(
            parameter_name="arg1",
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=False,
        )
        editor = ListEditor(args)

        args_2 = ListEditorArgs(
            parameter_name="arg2",
            default=None,
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=True,
        )

        editor2 = ListEditor(args_2)
        # editor2.set_value({})

        # add parameter widgets to the layout
        ctx.add_widget(editor)
        ctx.add_widget(editor2)
        # start the qt application
        ctx.exec()
