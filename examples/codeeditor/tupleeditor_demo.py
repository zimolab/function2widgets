from examples.context import ExampleContext
from function2widgets.widgets.editor import TupleEditorArgs, TupleEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = TupleEditorArgs(
            parameter_name="arg1",
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=False,
        )
        editor = TupleEditor(args)

        args_2 = TupleEditorArgs(
            parameter_name="arg2",
            default=None,
            button_text="Edit/View",
            window_title="Editor",
            display_current_value=True,
        )

        editor2 = TupleEditor(args_2)

        # add parameter widgets to the layout
        ctx.add_widget(editor)
        ctx.add_widget(editor2)
        # start the qt application
        ctx.exec()
