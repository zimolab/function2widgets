import re
from typing import Dict, Any

from function2widgets.common import load_toml

WIDGET_CONFIGS_START_TAG = "@widgets"
WIDGET_CONFIGS_END_TAG = "@end"

WIDGET_CONFIGS_BLOCK_PATTERN = (
    rf"^(\s*{WIDGET_CONFIGS_START_TAG}\s*(.*\n.+)^\s*{WIDGET_CONFIGS_END_TAG}\s*\n)"
)


class WidgetConfigsParser(object):
    def parse(self, raw_docstring_text: str) -> Dict[str, Any]:
        widget_configs_block = self._extract_widget_configs_block(
            raw_docstring_text
        ).strip()
        return self._parse_widget_configs(widget_configs_block)

    @staticmethod
    def remove_widget_configs_block(raw_docstring_text: str) -> str:
        match_result = re.search(
            pattern=WIDGET_CONFIGS_BLOCK_PATTERN,
            string=raw_docstring_text,
            flags=re.MULTILINE | re.DOTALL,
        )
        if match_result:
            return re.sub(
                pattern=WIDGET_CONFIGS_BLOCK_PATTERN,
                repl="",
                string=raw_docstring_text,
                flags=re.MULTILINE | re.DOTALL,
            )
        return raw_docstring_text

    @staticmethod
    def _extract_widget_configs_block(raw_docstring_text: str) -> str:
        match_result = re.search(
            WIDGET_CONFIGS_BLOCK_PATTERN, raw_docstring_text, re.MULTILINE | re.DOTALL
        )
        if match_result:
            return match_result.group(2)
        return ""

    @staticmethod
    def _parse_widget_configs(widget_configs_block: str) -> Dict[str, Any]:
        if not widget_configs_block:
            return {}
        return load_toml(widget_configs_block, error_on_fail=True)
