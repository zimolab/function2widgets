from examples.context import ExampleContext
from function2widgets.widgets.lineedit import IntLineEdit

with ExampleContext() as ctx:
    args = IntLineEdit._WidgetArgsClass(
        parameter_name="arg1",
        default=10,
        max_value=100,
        min_value=0,
        placeholder="Enter an integer",
    )
    # create parameter widgets
    int_lineedit = IntLineEdit(args)
    int_lineedit.set_label("int_lineedit")
    int_lineedit.set_description("This is an integer line edit.")

    args_2 = IntLineEdit._WidgetArgsClass(
        parameter_name="arg2",
        default=10,
        max_value=100,
        min_value=0,
        placeholder="Enter an integer",
    )
    int_lineedit2 = IntLineEdit(args_2)
    int_lineedit.set_description("This is an integer line edit.")

    # add parameter widgets to the layout
    ctx.add_widget(int_lineedit)
    ctx.add_widget(int_lineedit2)
    # start the qt application
    ctx.exec()
