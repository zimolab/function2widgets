import inspect
import warnings
from typing import Type, Any

from PyQt6 import Qsci
from PyQt6.Qsci import QsciScintilla, QsciLexer
from PyQt6.QtGui import QFont

AUTO_INDENT = True
INDENT_WIDTH = 4
SUPPORT_UTF8 = True
DEFAULT_LANGUAGE = "Python"
EOL = "Unix"
WRAP_MODE = "WrapWord"
FOLD_STYLE = "BoxTree"
FONT = "Consolas"
FONT_SIZE = 12


DEFAULT_CONFIGS = {
    "AutoIndent": AUTO_INDENT,
    "IndentationWidth": INDENT_WIDTH,
    "Utf8": SUPPORT_UTF8,
    "Lexer": DEFAULT_LANGUAGE,
    "EolMode": EOL,
    "WrapMode": WRAP_MODE,
    "AutoCompletionSource": "Document",
    "AutoCompletionCaseSensitivity": False,
    "AutoCompletionThreshold": 3,
    "Folding": FOLD_STYLE,
    "Font": "Consolas",
    "_FontSize": FONT_SIZE,
}


def _all_lexers() -> dict[str, Type[QsciLexer]]:
    all_lexers = {}
    baseclass_name = "QsciLexer"
    b_len = len(baseclass_name)
    for name in dir(Qsci):
        if name.startswith("QsciLexer") and len(name) > b_len:
            clazz = getattr(Qsci, name, None)
            if inspect.isclass(clazz) and issubclass(clazz, QsciLexer):
                all_lexers[name[b_len:]] = clazz
    return all_lexers


EolModes = {
    "Unix": QsciScintilla.EolMode.EolUnix,
    "Windows": QsciScintilla.EolMode.EolWindows,
    "Mac": QsciScintilla.EolMode.EolMac,
}

WrapModes = {
    "None": QsciScintilla.WrapMode.WrapNone,
    "Word": QsciScintilla.WrapMode.WrapWord,
    "Character": QsciScintilla.WrapMode.WrapCharacter,
    "WhiteSpace": QsciScintilla.WrapMode.WrapWhitespace,
}

FoldStyles = {
    "None": QsciScintilla.FoldStyle.NoFoldStyle,
    "Plain": QsciScintilla.FoldStyle.PlainFoldStyle,
    "Circle": QsciScintilla.FoldStyle.CircledFoldStyle,
    "CircleTree": QsciScintilla.FoldStyle.CircledTreeFoldStyle,
    "Box": QsciScintilla.FoldStyle.BoxedFoldStyle,
    "BoxTree": QsciScintilla.FoldStyle.BoxedTreeFoldStyle,
}
AutoCompletionSources = {
    "None": QsciScintilla.AutoCompletionSource.AcsNone,
    "All": QsciScintilla.AutoCompletionSource.AcsAll,
    "Document": QsciScintilla.AutoCompletionSource.AcsDocument,
    "APIs": QsciScintilla.AutoCompletionSource.AcsAPIs,
}

Lexers = _all_lexers()


# noinspection PyMethodMayBeStatic,PyUnusedLocal
class _CodeEditConfigurator(object):
    def __init__(self, target: "_SourceCodeEdit", raise_exception: bool = False):
        self._target = target
        self._raise_exception = raise_exception

        self.configvalue_mappers = {
            "EolMode": self.map_eol_mode,
            "WrapMode": self.map_wrap_mode,
            "Lexer": self.map_lexer,
            "Folding": self.map_folding,
            "Font": self.map_font,
            "AutoCompletionSource": self.map_acs,
        }

    def apply_configs(self, configs: dict[str, Any]):
        for configname, configvalue in configs.items():
            if configname.startswith("_"):
                continue
            if configname not in self.configvalue_mappers:
                self.apply_config(configname, configvalue)
                continue
            map_func = self.configvalue_mappers[configname]
            configvalue = map_func(configvalue, configs)
            self.apply_config(configname, configvalue)

    def apply_config(self, configname: str, configvalue: Any):
        if configvalue is None:
            return
        config_func = getattr(self._target, f"set{configname}", None)
        if not callable(config_func):
            message = f"unknown config: {configname}"
            if self._raise_exception:
                raise ValueError(message)
            else:
                warnings.warn(f"unknown config: {configname}")
            return
        config_func(configvalue)

    def map_eol_mode(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.EolMode:
        return EolModes.get(raw_value, None)

    def map_wrap_mode(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.WrapMode:
        return WrapModes.get(raw_value, None)

    def map_lexer(self, raw_value: str, configs: dict = None) -> QsciLexer | None:
        lexer = Lexers.get(raw_value, None)
        if not lexer:
            return None
        return lexer(parent=self._target)

    def map_folding(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.FoldStyle:
        return FoldStyles.get(raw_value, None)

    def map_font(self, raw_value: str, configs: dict = None) -> QFont:
        font_size = configs.get("_FontSize", 12)
        return QFont(raw_value, font_size)

    def map_acs(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.AutoCompletionSource:
        return AutoCompletionSources.get(raw_value, None)


class _SourceCodeEdit(QsciScintilla):

    def __init__(self, configs: dict = None, parent=None):

        if configs is None:
            configs = DEFAULT_CONFIGS

        super().__init__(parent=parent)

        self._configurator = _CodeEditConfigurator(self)
        self.apply_configs(configs)

    def apply_configs(self, configs: dict):
        self._configurator.apply_configs(configs)


def __test_main():
    from PyQt6.QtWidgets import QApplication

    print(_all_lexers())

    my_configs = DEFAULT_CONFIGS.copy()
    my_configs["EolMode"] = "Windows"
    my_configs["Lexer"] = "JSON"

    app = QApplication([])
    code_edit = _SourceCodeEdit(configs=my_configs)
    code_edit.resize(800, 600)
    code_edit.show()

    app.exec()


if __name__ == "__main__":
    __test_main()
