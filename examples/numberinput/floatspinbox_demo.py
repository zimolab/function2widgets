from examples.context import ExampleContext
from function2widgets import FloatSpinBoxArgs, FloatSpinBox

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = FloatSpinBoxArgs(
            parameter_name="arg1",
            min_value=-100,
            max_value=100,
            step=0.1,
            decimals=5,
            accelerated=True,
            prefix="prefix: ",
            suffix=" suffix",
        )
        spin_1 = FloatSpinBox(args)

        args2 = FloatSpinBoxArgs(
            parameter_name="arg2",
            default=None,
        )

        spin_2 = FloatSpinBox(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(spin_1)
        ctx.add_widget(spin_2)
        # start the qt application
        ctx.exec()
