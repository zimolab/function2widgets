from examples.context import ExampleContext
from function2widgets import LineEditArgs, LineEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = LineEditArgs(
            default="1234", parameter_name="arg1", hide_default_value_widget=False
        )
        lineedit_1 = LineEdit(args)
        lineedit_1.set_label("lineedit_1")
        lineedit_1.set_description("<b>this is a line edit!</b>")

        args2 = LineEditArgs(
            parameter_name="arg2",
            default="aBcD12345",
            placeholder="input password here",
            clear_button=True,
            echo_mode="Password",
            regex=r"^[a-zA-Z0-9]{10}$",
        )

        lineedit_2 = LineEdit(args2)
        lineedit_2.set_label("Password")
        lineedit_2.set_description(
            "<b>This is a line edit for password input</b><br>"
            "<b><font color='red'>Password regex: ^[a-zA-Z0-9]{10}$</font></b>"
        )
        # # add parameter widgets to the layout
        ctx.add_widget(lineedit_1)
        ctx.add_widget(lineedit_2)
        # start the qt application
        ctx.exec()
