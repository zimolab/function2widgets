from typing import Optional

from PyQt6.QtWidgets import QWidget

from function2widgets.widgets.jsoneditor import _NoneType, JsonEditor


class ListEditor(JsonEditor):
    HIDE_USE_DEFAULT_CHECKBOX = True
    SET_DEFAULT_ON_INIT = True

    TYPE_RESTRICTIONS = (list, _NoneType)

    def __init__(
        self,
        default: list = None,
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
            default=default,
            configs=configs,
            edit_button_text=edit_button_text,
            window_title=window_title,
            display_current_value=display_current_value,
            stylesheet=stylesheet,
            set_default_on_init=set_default_on_init,
            hide_use_default_checkbox=hide_use_default_checkbox,
            parent=parent,
        )

    def get_value(self, *args, **kwargs) -> Optional[list]:
        return super().get_value(*args, **kwargs)

    def set_value(self, value: Optional[list], *args, **kwargs):
        if isinstance(value, (tuple, set)):
            value = list(value)
        super().set_value(value, *args, **kwargs)
