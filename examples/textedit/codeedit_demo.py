from examples.context import ExampleContext
from function2widgets.widgets.textedit import CodeEditArgs, CodeEdit

if __name__ == "__main__":
    with ExampleContext() as ctx:
        # create parameter widgets
        args = CodeEditArgs(
            parameter_name="arg1",
            default="""
            #!/usr/bin/env python3
            # -*- coding: utf-8 -*-
            # File: codeedit_demo.py
            # Description:
            #       This is a demo of codeedit widget.
            #       You can use it to edit python code.
            #       You can also use it to edit other languages.
            print("hello world")
            """,
            configs={
                "AutoIndent": True,
                "IndentationWidth": 4,
                "Utf8": True,
                "Lexer": "Python",
                "EolMode": "Unix",
                "WrapMode": "WrapWord",
                "AutoCompletionSource": "Document",
                "AutoCompletionCaseSensitivity": False,
                "AutoCompletionThreshold": 3,
                "Folding": "BoxTree",
                "Font": "Consolas",
                "_FontSize": 12,
            },
        )
        edit1 = CodeEdit(args)

        args2 = CodeEditArgs(
            parameter_name="arg2",
            default=None,
        )

        edit2 = CodeEdit(args2)
        # # add parameter widgets to the layout
        ctx.add_widget(edit1)
        ctx.add_widget(edit2)
        # start the qt application
        ctx.exec()
