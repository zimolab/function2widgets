from examples.context import ExampleContext
from function2widgets.widgets import LineEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        lineedit_1 = LineEdit(default=None, placeholder="input some text here")
        lineedit_1.set_label("lineedit_1")
        lineedit_1.set_docstring("<b>this is a line edit!</b>")

        lineedit_2 = LineEdit(
            default="aBcD12345",
            placeholder="input password here",
            clear_button=True,
            echo_mode="Password",
            regex=r"^[a-zA-Z0-9]{10}$",
        )
        lineedit_2.set_label("Password")
        lineedit_2.set_docstring(
            "<b>This is a line edit for password input</b><br>"
            "<b><font color='red'>Password regex: ^[a-zA-Z0-9]{10}$</font></b>"
        )
        # add parameter widgets to the layout
        ctx.add_widget(lineedit_1)
        ctx.add_widget(lineedit_2)
        # start the qt application
        ctx.exec()
