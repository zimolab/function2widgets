from examples.context import ExampleContext
from function2widgets import SliderArgs, Slider

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = SliderArgs(
            parameter_name="arg1",
            min_value=0,
            max_value=100,
            step=1,
            page_step=10,
            tracking=True,
            tick_position="below",
            tick_interval=10,
            inverted_appearance=False,
            inverted_control=False,
            show_value_label=True,
            value_prefix="Value: ",
            value_suffix="%",
        )
        slider1 = Slider(args)

        args2 = SliderArgs(
            parameter_name="arg2",
            default=None,
        )

        slider2 = Slider(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(slider1)
        ctx.add_widget(slider2)
        # start the qt application
        ctx.exec()
