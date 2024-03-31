import abc
import copy
import dataclasses
from typing import Any, Optional, cast

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QCheckBox,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
)

from function2widgets.widget import BaseParameterWidget, WidgetArgs


@dataclasses.dataclass(frozen=True)
class CommonParameterWidgetArgs(WidgetArgs):
    parameter_name: str
    default: Any
    label: Optional[str] = None
    description: Optional[str] = None
    stylesheet: Optional[str] = None
    set_default_on_init: Optional[bool] = None
    hide_default_widget: Optional[bool] = None
    default_widget_text: Optional[str] = None
    separate_line: bool = True


class CommonParameterWidget(BaseParameterWidget):

    _WidgetArgsClass = CommonParameterWidgetArgs

    OBJ_ID_LAYOUT = "_CPW_main_layout"
    OBJ_ID_CENTER_WIDGET = "_CPW_center_widget"
    OBJ_ID_LABEL_WIDGET = "_CPW_label_widget"
    OBJ_ID_DESCRIPTION_WIDGET = "_CPW_description_widget"
    OBJ_ID_DEFAULT_WIDGET = "_CPW_default_widget"
    OBJ_ID_SEPARATE_LINE = "_CPW_separate_line_widget"

    def __init__(self, args: CommonParameterWidgetArgs, parent: Optional[QWidget]):

        super().__init__(args=args, parent=parent)

        self._layout = QVBoxLayout(self)
        self._center_widget = QWidget(self)
        self._label_widget = QLabel(self)
        self._description_widget = QLabel(self)
        self._default_widget = QCheckBox(self)

        self._setup_label_widget()
        self._setup_description_widget()
        self._setup_default_widget()
        self._setup_layout()
        self.setup_center_widget(self._center_widget)
        self.set_label(self._args.label)
        self.set_description(self._args.description)

    def set_value(self, value: Any):
        value = copy.deepcopy(value)
        if not self._pre_set_value(value):
            return
        self.set_value_to_widget(value)

    def get_value(self) -> Any:
        if self._is_use_default():
            return self._args.default
        return copy.deepcopy(self.get_value_from_widget())

    @abc.abstractmethod
    def setup_center_widget(self, center_widget: QWidget):
        pass

    @abc.abstractmethod
    def set_value_to_widget(self, value: Any):
        pass

    @abc.abstractmethod
    def get_value_from_widget(self) -> Any:
        pass

    @property
    def _args(self) -> CommonParameterWidgetArgs:
        return cast(CommonParameterWidgetArgs, super()._args)

    def set_label(self, label: str):
        if not label:
            self._label_widget.setText("")
            self._label_widget.hide()
        else:
            self._label_widget.setText(label)
            self._label_widget.show()

    def get_label(self) -> str:
        return self._label_widget.text()

    def set_description(self, desc: str):
        if not desc:
            self._description_widget.setText("")
            self._description_widget.hide()
        else:
            self._description_widget.setText(desc)
            self._description_widget.show()

    def get_description(self) -> str:
        return self._description_widget.text()

    def _setup_default_widget(self):
        if self._args.default_widget_text is None:
            text = "{}"
        else:
            text = self._args.default_widget_text
        self._default_widget.setText(text.format(self._args.default))
        # noinspection PyUnresolvedReferences
        self._default_widget.toggled.connect(self._on_default_widget_state_changed)
        self._default_widget.setHidden(self._args.hide_default_widget)

    def _setup_label_widget(self):
        self._label_widget.setWordWrap(True)
        self._label_widget.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

    def _setup_description_widget(self):
        self._description_widget.setWordWrap(True)
        self._description_widget.setAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )

    def _on_default_widget_state_changed(self, checked: bool):
        if self._args.hide_default_widget:
            return
        self._center_widget.setEnabled(not checked)

    def _setup_layout(self):
        cls = self.__class__
        self.setLayout(self._layout)

        self._layout.setObjectName(cls.OBJ_ID_LAYOUT)
        self._label_widget.setObjectName(cls.OBJ_ID_LABEL_WIDGET)
        self._description_widget.setObjectName(cls.OBJ_ID_DESCRIPTION_WIDGET)
        self._center_widget.setObjectName(cls.OBJ_ID_CENTER_WIDGET)
        self._default_widget.setObjectName(cls.OBJ_ID_DEFAULT_WIDGET)

        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self._label_widget)
        self._layout.addWidget(self._center_widget)
        self._layout.addWidget(self._default_widget)
        self._layout.addWidget(self._description_widget)
        if self._args.separate_line:
            line = self._create_separate_line()
            self._layout.addWidget(line)
        # spacer = QSpacerItem(
        #     0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        # )
        # self._layout.addSpacerItem(spacer)

    def _is_use_default(self) -> bool:
        if self._args.hide_default_widget or self._default_widget.isHidden():
            return False
        return self._default_widget.isChecked()

    def _use_default(self):
        if self._args.hide_default_widget or self._default_widget.isHidden():
            return
        self._default_widget.setChecked(True)

    def _unuse_default(self):
        if self._args.hide_default_widget or self._default_widget.isHidden():
            return
        self._default_widget.setChecked(False)

    def _pre_set_value(self, value: Any) -> bool:
        if value is None and self._args.default is not None:
            raise ValueError(
                f"value cannot be None unless the default value is set to None(default={self.default})"
            )

        if value is None and self._args.default is None:
            self._use_default()
            return False

        if value == self._args.default:
            self._use_default()
        else:
            self._unuse_default()
        return True

    def _create_separate_line(self) -> QFrame:
        separate_line = QFrame(self)
        separate_line.setObjectName(self.__class__.OBJ_ID_SEPARATE_LINE)
        separate_line.setFrameShape(QFrame.Shape.HLine)
        separate_line.setFrameShadow(QFrame.Shadow.Sunken)
        return separate_line
