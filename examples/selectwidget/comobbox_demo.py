from examples.context import ExampleContext
from function2widgets import ComboBoxArgs, ComboBox

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        # set label to "" to hide label widget
        # if label is None, the label text will be the parameter_name
        args = ComboBoxArgs(
            parameter_name="arg1",
            items=["a", "b", "c"],
            default="c",
            description="this is combobox with some text items",
        )
        combo1 = ComboBox(args)
        # checkbox_group.set_value("a")

        args2 = ComboBoxArgs(
            parameter_name="arg2",
            items=[("a", 1), ("b", 2), ("c", 3)],
            description="this is combobox with some text-with-data items",
        )
        combo2 = ComboBox(args2)

        ctx.add_widget(combo1)
        ctx.add_widget(combo2)
        # start the qt application
        ctx.exec()
