from examples.context import ExampleContext
from function2widgets import RadioButtonGroupArgs, RadioButtonGroup

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        # set label to "" to hide label widget
        # if label is None, the label text will be the parameter_name
        args = RadioButtonGroupArgs(
            parameter_name="arg1",
            column_count=2,
            items=["a", "b", "c"],
            description="this is radio button group",
        )
        radio_group_1 = RadioButtonGroup(args)

        args2 = RadioButtonGroupArgs(
            parameter_name="arg2",
            column_count=2,
            items=["a", "b", "c"],
            default=None,
            description="this is radio button group",
        )
        radio_group_2 = RadioButtonGroup(args2)

        ctx.add_widget(radio_group_1)
        ctx.add_widget(radio_group_2)
        # start the qt application
        ctx.exec()
