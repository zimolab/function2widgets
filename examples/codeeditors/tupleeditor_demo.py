from examples.context import ExampleContext
from function2widgets.widgets import TupleEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        editor = TupleEditor(
            default=None,
        )
        editor.set_label("editor1")

        editor2 = TupleEditor(
            default=(),
        )
        editor2.set_label("editor2")

        # add parameter widgets to the layout
        ctx.add_widget(editor)
        ctx.add_widget(editor2)
        # start the qt application
        ctx.exec()
