from examples.context import ExampleContext
from function2widgets.widgets.misc import ColorEdit, ColorEditArgs
from function2widgets.widgets import Color

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = ColorEditArgs(
            parameter_name="arg1",
            default=Color.from_color_name("red"),
            with_alpha=True,
            display_format="hex",
        )
        edit = ColorEdit(args)

        args_2 = ColorEditArgs(
            parameter_name="arg2", default=None, with_alpha=False, display_format="rgb"
        )
        edit_2 = ColorEdit(args_2)

        ctx.add_widget(edit)
        ctx.add_widget(edit_2)
        # start the qt application
        ctx.exec()
