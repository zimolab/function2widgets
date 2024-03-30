from examples.context import ExampleContext
from function2widgets.widgets.selectwidget import CheckBoxGroupArgs, CheckBoxGroup

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        # set label to "" to hide label widget
        # if label is None, the label text will be the parameter_name
        args = CheckBoxGroupArgs(
            parameter_name="arg1",
            column_count=2,
            items=["a", "b", "c"],
            description="this is a group of checkboxes",
        )
        checkbox_group = CheckBoxGroup(args)
        checkbox_group.set_value(["d", "c"])

        ctx.add_widget(checkbox_group)
        # start the qt application
        ctx.exec()
