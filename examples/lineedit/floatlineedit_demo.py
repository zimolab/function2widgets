from examples.context import ExampleContext
from function2widgets.widgets.lineedit import FloatLineEdit

with ExampleContext() as ctx:
    # create parameter widgets
    args1 = FloatLineEdit._WidgetArgsClass(
        parameter_name="arg1",
        default=10.0,
        max_value=100.0,
        min_value=0.0,
        decimals=5,
        scientific_notation=False,
        placeholder="Enter an integer",
    )
    float_lineedit = FloatLineEdit(args1)
    float_lineedit.set_label("float_lineedit")
    float_lineedit.set_description("This is an float number line edit.")

    args2 = FloatLineEdit._WidgetArgsClass(
        parameter_name="arg2",
        default=1.0,
        max_value=100.0,
        min_value=0.0,
        decimals=5,
        scientific_notation=False,
        placeholder="Enter an integer",
        hide_default_widget=False,
    )
    float_lineedit2 = FloatLineEdit(args2)
    float_lineedit2.set_label("float_lineedit2")
    float_lineedit2.set_description("This is an float number line edit.")

    # add parameter widgets to the layout
    ctx.add_widget(float_lineedit)
    ctx.add_widget(float_lineedit2)
    # start the qt application
    ctx.exec()
