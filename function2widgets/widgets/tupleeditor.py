from typing import Optional

from PyQt6.QtWidgets import QWidget

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.jsoneditor import _NoneType, JsonEditor


class TupleEditor(JsonEditor):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    TYPE_RESTRICTIONS = (list, tuple, _NoneType)

    def __init__(
        self,
        default: tuple = None,
        configs: dict = None,
        edit_button_text: str = None,
        window_title: str = None,
        display_current_value: bool = True,
        stylesheet: Optional[str] = None,
        set_default_on_init: Optional[bool] = None,
        hide_use_default_checkbox: Optional[bool] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(
            top_level_types=self.TYPE_RESTRICTIONS,
            configs=configs,
            default=default,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )

    def set_value(self, value: Optional[tuple], *args, **kwargs):
        if isinstance(value, list):
            value = tuple(value)
        super().set_value(value, *args, **kwargs)

    def get_value(self, *args, **kwargs) -> Optional[tuple]:
        value = super().get_value(*args, **kwargs)
        if value is None:
            return None
        elif isinstance(value, list):
            return tuple(value)
        elif isinstance(value, tuple):
            return value
        else:
            raise InvalidValueError(
                self.tr(
                    f"value '{value}' is not one of the following types: {self._top_level_types}"
                )
            )
