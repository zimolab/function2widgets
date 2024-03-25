from examples.context import ExampleContext
from function2widgets.widgets import FloatLineEdit

with ExampleContext() as ctx:
    # create parameter widgets
    float_lineedit = FloatLineEdit(
        default=10.0,
        max_value=100.0,
        min_value=0.0,
        decimals=5,
        scientific_notation=False,
        placeholder="Enter an integer",
    )
    float_lineedit.set_label("float_lineedit")
    float_lineedit.set_docstring("This is an float number line edit.")

    float_lineedit2 = FloatLineEdit(
        default=1.0,
        max_value=100.0,
        min_value=0.0,
        decimals=5,
        scientific_notation=False,
        placeholder="Enter an integer",
        hide_use_default_checkbox=False,
    )
    float_lineedit2.set_label("float_lineedit2")
    float_lineedit2.set_docstring("This is an float number line edit.")

    # add parameter widgets to the layout
    ctx.add_widget(float_lineedit)
    ctx.add_widget(float_lineedit2)
    # start the qt application
    ctx.exec()
