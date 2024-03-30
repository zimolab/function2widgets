import warnings

import docstring_parser

from function2widgets.info import FunctionDocstringInfo
from function2widgets.parser.widgetconfigs_parser import WidgetConfigsParser


class ParseException(Exception):
    pass


class FunctionDocstringParser(object):

    def __init__(self):
        self._widget_configs_parser = WidgetConfigsParser()

    def parse(self, raw_docstring_text: str) -> FunctionDocstringInfo:
        docstring_text = WidgetConfigsParser.remove_widget_configs_block(
            raw_docstring_text
        )
        docstring_obj = self._get_docstring_obj(docstring_text)
        try:
            widget_configs = self._widget_configs_parser.parse(raw_docstring_text)
        except BaseException as e:
            raise ParseException("failed to parse widget configs block") from e
        docstring_info = FunctionDocstringInfo(
            docstring_text=docstring_text,
            docstring_obj=docstring_obj,
            widget_configs=widget_configs,
        )

        return docstring_info

    @staticmethod
    def _get_docstring_obj(docstring_text: str) -> docstring_parser.Docstring:
        try:
            return docstring_parser.parse(docstring_text)
        except BaseException as e:
            warnings.warn(f"cannot parse docstring: {e}")
            return docstring_parser.Docstring()

    # def _to_param_widgets_infos(
    #     self, widget_configs: Dict[str, Any]
    # ) -> Dict[str, ParameterWidgetInfo]:
    #     param_widget_infos = OrderedDict()
    #     for param_name, param_widget_config in widget_configs.items():
    #         if not isinstance(param_widget_config, dict) or not param_widget_config:
    #             continue
    #         param_widget_infos[param_name] = self._to_param_widget_info(
    #             param_name, param_widget_config
    #         )
    #
    #     return param_widget_infos
    #
    # @staticmethod
    # def _to_param_widget_info(
    #     param_name: str, param_widget_config: Dict[str, Any]
    # ) -> Optional[ParameterWidgetInfo]:
    #     param_widget_config = {**param_widget_config}
    #     widget_class = param_widget_config.get("widget_class")
    #     if not widget_class:
    #         widget_class = param_widget_config.get("type")
    #     if not widget_class:
    #         widget_class = param_widget_config.get("widget_type")
    #
    #     if not widget_class:
    #         return None
    #
    #     widget_args = safe_pop(
    #         param_widget_config, "type", "widget_class", "widget_type"
    #     )
    #
    #     return ParameterWidgetInfo(
    #         widget_class=widget_class,
    #         widget_args=widget_args,
    #     )
