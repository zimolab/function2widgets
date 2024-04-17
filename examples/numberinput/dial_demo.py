from examples.context import ExampleContext
from function2widgets import DialArgs, Dial

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = DialArgs(
            parameter_name="arg1",
            min_value=0,
            max_value=100,
            step=1,
            page_step=10,
            tracking=True,
            wrapping=True,
            notches_visible=True,
            notches_target=0.5,
            inverted_appearance=False,
            inverted_control=False,
            show_value_label=True,
            value_prefix="Value: ",
            value_suffix=" %",
        )
        dial1 = Dial(args)
        # dial1.set_value(50)
        # value should be int
        # dial1.set_value("50")

        args2 = DialArgs(
            parameter_name="arg2",
            default=None,
        )

        dial2 = Dial(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(dial1)
        ctx.add_widget(dial2)
        # start the qt application
        ctx.exec()
