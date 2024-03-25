from examples.context import ExampleContext
from function2widgets.widgets import IntLineEdit

with ExampleContext() as ctx:
    # create parameter widgets
    int_lineedit = IntLineEdit(
        default=10,
        max_value=100,
        min_value=0,
        placeholder="Enter an integer",
    )
    int_lineedit.set_label("int_lineedit")
    int_lineedit.set_docstring("This is an integer line edit.")

    int_lineedit2 = IntLineEdit(
        default=None,
        max_value=100,
        min_value=0,
        placeholder="Enter an integer",
    )
    int_lineedit.set_label("int_lineedit")
    int_lineedit.set_docstring("This is an integer line edit.")

    # add parameter widgets to the layout
    ctx.add_widget(int_lineedit)
    ctx.add_widget(int_lineedit2)
    # start the qt application
    ctx.exec()
