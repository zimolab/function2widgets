from examples.context import ExampleContext
from function2widgets.widgets import UniversalSourceCodeEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        codeeditor = UniversalSourceCodeEditor(
            default=None,
            edit_button_text="Edit/View",
            window_title="Code Editor",
        )
        print(codeeditor.get_value())

        # add parameter widgets to the layout
        ctx.add_widget(codeeditor)
        # start the qt application
        ctx.exec()
