import inspect
import warnings
from typing import Type, Any, Dict, Optional

from PyQt6 import Qsci
from PyQt6.Qsci import QsciScintilla, QsciLexer
from PyQt6.QtGui import QFont, QColor

AUTO_INDENT = True
INDENT_WIDTH = 4
SUPPORT_UTF8 = True
DEFAULT_LANGUAGE = "Python"
EOL = "Unix"
WRAP_MODE = "WrapWord"
FOLD_STYLE = "BoxTree"
FONT = "Consolas"
FONT_SIZE = 12
ENABLE_LINE_NUMBER = True

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
    "ShowLineNumber": ENABLE_LINE_NUMBER,
}


def _all_lexers() -> Dict[str, Type[QsciLexer]]:
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

        self.config_value_mappers = {
            "EolMode": self.map_eol_mode,
            "WrapMode": self.map_wrap_mode,
            "Lexer": self.map_lexer,
            "Folding": self.map_folding,
            "Font": self.map_font,
            "AutoCompletionSource": self.map_acs,
        }

    def apply_configs(self, configs: Dict[str, Any]):
        for config_name, config_value in configs.items():
            if config_name.startswith("_"):
                continue
            if config_name not in self.config_value_mappers:
                self.apply_config(config_name, config_value)
                continue

            map_func = self.config_value_mappers[config_name]
            config_value = map_func(config_value, configs)
            self.apply_config(config_name, config_value)

    def apply_config(self, config_name: str, config_value: Any):
        if config_value is None:
            return
        config_func = getattr(self._target, f"set{config_name}", None)
        if not callable(config_func):
            message = f"unknown config: {config_name}"
            if self._raise_exception:
                raise ValueError(message)
            else:
                warnings.warn(f"unknown config: {config_name}")
            return
        config_func(config_value)

    def map_eol_mode(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.EolMode:
        return EolModes.get(raw_value, None)

    def map_wrap_mode(
        self, raw_value: str, configs: dict = None
    ) -> QsciScintilla.WrapMode:
        return WrapModes.get(raw_value, None)

    def map_lexer(self, raw_value: str, configs: dict = None) -> Optional[QsciLexer]:
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
        super().__init__(parent=parent)
        if configs is None:
            configs = DEFAULT_CONFIGS
        self._configurator = _CodeEditConfigurator(self)
        self.apply_configs(configs)

    # noinspection PyPep8Naming
    def setShowLineNumber(self, show: bool):
        if show:
            self.setMarginsFont(QFont("Courier New", 10))  # 行号字体
            self.setMarginLineNumbers(0, True)  # 设置标号为0的页边显示行号
            self.setMarginWidth(0, "0000")  # 行号宽度
            self.setMarkerForegroundColor(QColor("#FFFFFF"), 0)
        else:
            self.setMarginLineNumbers(0, False)  # 设置标号为0的页边显示行号

    def apply_configs(self, configs: dict):
        self._configurator.apply_configs(configs)
