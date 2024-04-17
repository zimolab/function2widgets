from examples.context import ExampleContext
from function2widgets import CheckBoxArgs

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        # set label to "" to hide label widget
        # if label is None, the label text will be the parameter_name
        args = CheckBoxArgs(parameter_name="arg1", label="")
        checkbox = CheckBox(args)
        checkbox.set_description("<b>this is a checkbox!</b>")

        args_2 = CheckBoxArgs(
            parameter_name="arg2",
            default=None,
            text="enable this option?",
            label="",
            set_default_on_init=True,
        )
        checkbox2 = CheckBox(args_2)

        ctx.add_widget(checkbox)
        ctx.add_widget(checkbox2)
        # start the qt application
        ctx.exec()
