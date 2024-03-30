from examples.context import ExampleContext
from function2widgets.widgets.numberinput import IntSpinBox, IntSpinBoxArgs

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = IntSpinBoxArgs(
            parameter_name="arg1",
            min_value=-100,
            max_value=100,
            step=1,
            prefix="prefix: ",
            suffix=" suffix",
        )
        spin_1 = IntSpinBox(args)

        args2 = IntSpinBoxArgs(
            parameter_name="arg2",
            default=None,
        )

        spin_2 = IntSpinBox(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(spin_1)
        ctx.add_widget(spin_2)
        # start the qt application
        ctx.exec()
