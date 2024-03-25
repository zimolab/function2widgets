from examples.context import ExampleContext
from function2widgets.widgets import JsonEditor

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        jsoneditor = JsonEditor(default=None, set_default_on_init=False)
        jsoneditor.set_label("editor1")

        jsoneditor2 = JsonEditor(
            default=1234,
        )
        jsoneditor.set_label("editor2")

        # add parameter widgets to the layout
        ctx.add_widget(jsoneditor)
        ctx.add_widget(jsoneditor2)
        # start the qt application
        ctx.exec()
