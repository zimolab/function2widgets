from examples.context import ExampleContext
from function2widgets import ComboBoxEditArgs, ComboBoxEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        # set label to "" to hide label widget
        # if label is None, the label text will be the parameter_name
        args = ComboBoxEditArgs(
            parameter_name="arg1",
            items=["a", "b", "c"],
            default="c",
            description="this is editable combobox with some text items",
        )
        combo1 = ComboBoxEdit(args)
        # checkbox_group.set_value("a")

        args2 = ComboBoxEditArgs(
            parameter_name="arg2",
            items=["apple", "banana", "pearl"],
            default="orange",
            description="this is editable combobox",
        )
        combo2 = ComboBoxEdit(args2)

        ctx.add_widget(combo1)
        ctx.add_widget(combo2)
        # start the qt application
        ctx.exec()
