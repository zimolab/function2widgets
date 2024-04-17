from examples.context import ExampleContext
from function2widgets import LineEdit, LineEditArgs

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = LineEditArgs(
            default="1234",
            parameter_name="arg1",
            hide_default_value_widget=False,
            description="hello world，<a href='https://www.baidu.com'>baidu</a>",
            open_external_link=False,
        )
        lineedit_1 = LineEdit(args)
        lineedit_1.set_label("lineedit_1")

        args2 = LineEditArgs(
            parameter_name="arg2",
            default="aBcD12345",
            description="hello world，<a href='https://www.baidu.com'>baidu</a>",
            placeholder="input password here",
            clear_button=True,
            echo_mode="Password",
            regex=r"^[a-zA-Z0-9]{10}$",
            open_external_link=True,
        )

        lineedit_2 = LineEdit(args2)
        lineedit_2.set_label("Password")
        # # add parameter widgets to the layout
        ctx.add_widget(lineedit_1)
        ctx.add_widget(lineedit_2)
        # start the qt application
        ctx.exec()
