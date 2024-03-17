from typing import Iterable, List, OrderedDict

from PyQt6.QtWidgets import (
    QWidget,
    QComboBox,
    QVBoxLayout,
    QGridLayout,
    QRadioButton,
    QButtonGroup,
    QCheckBox,
    QApplication,
)

from function2widgets.widget import InvalidValueError
from function2widgets.widgets.base import CommonParameterWidget


def _uid(prefix: str, item: str):
    return f"{prefix}{hash(item)}"


class ComboBox(CommonParameterWidget):
    def __init__(
        self,
        items: Iterable[str],
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._value_widget: QComboBox | None = None
        self._items = [item for item in items]

        if default not in self._items and default is not None:
            raise InvalidValueError(
                QApplication.tr(f"invalid default value: {default}")
            )

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self.default)

    def setup_center_widget(self, center_widget: QWidget):
        self._value_widget = QComboBox(center_widget)
        for item in self._items:
            self._value_widget.addItem(item)
        if isinstance(self.default, str) and self.default in self._items:
            self._value_widget.setCurrentText(self.default)
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.addWidget(self._value_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

    def get_value(self, *args, **kwargs) -> str | None:
        if self._is_use_default():
            return self.default
        return self._value_widget.currentText()

    def set_value(self, value: str | None, *args, **kwargs):
        if value is not None and value not in self._items:
            raise InvalidValueError(
                self.tr(f"invalid value: '{value}' is not in combobox items")
            )
        if not self._pre_set_value(value):
            return
        self._value_widget.setCurrentText(value)


class ComboBoxEdit(ComboBox):
    def __init__(
        self,
        items: Iterable[str],
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        items = [items for items in items]
        if isinstance(default, str) and default not in items:
            items.append(default)
        super().__init__(
            items=items, default=default, stylesheet=stylesheet, parent=parent
        )
        self.set_value(default)

    def setup_center_widget(self, center_widget: QWidget):
        super().setup_center_widget(center_widget)
        self._value_widget.setEditable(True)

    def _has_item(self, item: str) -> bool:
        for i in range(self._value_widget.count()):
            if item == self._value_widget.itemText(i):
                return True
        return False

    def set_value(self, value: str | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        if value and not self._has_item(value):
            self._value_widget.addItem(value)
        self._value_widget.setCurrentText(value)


class RadioButtonGroup(CommonParameterWidget):
    BTN_PREFIX = "_radio_btn"

    def __init__(
        self,
        items: Iterable[str],
        column_count: int = 1,
        default: str | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._button_group: QButtonGroup | None = None

        if column_count < 1:
            raise InvalidValueError(
                self.tr(f"invalid column count: {column_count} must be greater than 0")
            )
        self._column_count = column_count

        self._items = list(OrderedDict.fromkeys(items))

        if default not in self._items and default is not None:
            raise InvalidValueError(self.tr(f"invalid default value: '{default}'"))

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)

        self.set_value(self.default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QGridLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        self._button_group = QButtonGroup(center_widget)
        self._button_group.setExclusive(True)
        for i, item in enumerate(self._items):
            btn_id = _uid(self.BTN_PREFIX, item)
            radio_button = QRadioButton(center_widget)
            radio_button.setObjectName(btn_id)
            radio_button.setText(item)
            self._button_group.addButton(radio_button)
            if i % self._column_count == 0:
                center_widget_layout.addWidget(radio_button, i // self._column_count, 0)
            else:
                center_widget_layout.addWidget(
                    radio_button, i // self._column_count, i % self._column_count
                )

    def get_value(self, *args, **kwargs) -> str | None:
        if self._is_use_default():
            return self.default
        radio_btn = self._button_group.checkedButton()
        if not radio_btn:
            return None
        return radio_btn.text()

    def set_value(self, value: str | None, *args, **kwargs):
        if value is not None and value not in self._items:
            raise InvalidValueError(
                self.tr(f"invalid value: '{value}' is not in combobox items")
            )
        if not self._pre_set_value(value):
            return
        radio_btn = self._get_radio_button(value)
        radio_btn.setChecked(True)

    def _get_radio_button(self, item: str | None) -> QRadioButton | None:
        if item is None:
            return None
        btn_id = _uid(self.BTN_PREFIX, item)
        return self._center_widget.findChild(QRadioButton, btn_id)


class CheckBoxGroup(CommonParameterWidget):
    BTN_PREFIX = "_checkbox"

    def __init__(
        self,
        items: Iterable[str],
        column_count: int = 1,
        default: List[str] | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):

        self._checkbox_buttons = []

        if column_count < 1:
            raise InvalidValueError(
                QApplication.tr(
                    f"invalid column count: {column_count} must be greater than 0"
                )
            )
        self._column_count = column_count

        self._items = list(OrderedDict.fromkeys(items))

        super().__init__(default=default, stylesheet=stylesheet, parent=parent)
        self.set_value(self.default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QGridLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)

        for i, item in enumerate(self._items):
            btn_id = _uid(self.BTN_PREFIX, item)
            checkbox_btn = QCheckBox(center_widget)
            checkbox_btn.setObjectName(btn_id)
            checkbox_btn.setText(item)
            self._checkbox_buttons.append(checkbox_btn)
            if i % self._column_count == 0:
                center_widget_layout.addWidget(checkbox_btn, i // self._column_count, 0)
            else:
                center_widget_layout.addWidget(
                    checkbox_btn, i // self._column_count, i % self._column_count
                )

    def get_value(self, *args, **kwargs) -> List[str]:
        if self._is_use_default():
            return self.default
        return [
            checkbox.text()
            for checkbox in self._checkbox_buttons
            if checkbox.isChecked()
        ]

    def set_value(self, value: List[str], *args, **kwargs):
        if not self._pre_set_value(value):
            return
        for checkbox in self._checkbox_buttons:
            if checkbox.text() in value:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)


class CheckBox(CommonParameterWidget):
    def __init__(
        self,
        text: str = None,
        default: bool | None = None,
        stylesheet: str | None = None,
        parent: QWidget | None = None,
    ):
        self._text = text or QApplication.tr("ENABLE")
        self._checkbox: QCheckBox | None = None
        super().__init__(default=default, stylesheet=stylesheet, parent=parent)
        self.set_value(default)

    def setup_center_widget(self, center_widget: QWidget):
        center_widget_layout = QVBoxLayout(center_widget)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        center_widget.setLayout(center_widget_layout)
        self._checkbox = QCheckBox(center_widget)
        self._checkbox.setText(self._text)
        center_widget_layout.addWidget(self._checkbox)

    def get_value(self, *args, **kwargs) -> bool | None:
        if self._is_use_default():
            return self.default
        return self._checkbox.isChecked()

    def set_value(self, value: bool | None, *args, **kwargs):
        if not self._pre_set_value(value):
            return
        self._checkbox.setChecked(value is True)


def __test_main():
    from PyQt6.QtWidgets import QApplication, QWidget

    app = QApplication([])
    wind = QWidget()
    layout = QVBoxLayout(wind)
    wind.setLayout(layout)

    combo = ComboBox(["a", "b", "c"], default=None, parent=wind)
    combo.set_label("ComboBoxWidget")
    print("current value:", combo.get_value())
    combo.set_value("c")
    try:
        combo.set_value("d")
    except InvalidValueError as e:
        print(e)
    print("current value:", combo.get_value())
    # combo.set_value(None)
    # print("current value:", combo.get_value())

    combo_edit = ComboBoxEdit(["a", "b", "c"], default="b", parent=wind)
    combo_edit.set_label("ComboBoxEdit")
    combo_edit.set_value("new1")
    combo_edit.set_value("new2")
    combo_edit.set_value("new3")

    options = ["a", "b", "c"]
    radio_group = RadioButtonGroup(options, column_count=3, default="c", parent=wind)
    radio_group.set_label("RadioButtonGroup")
    # for opt in options:
    #     print(radio_group._get_radio_button(opt))
    radio_group.set_value("c")
    # radio_group.set_value("a")

    checkbox_group = CheckBoxGroup(options, column_count=3, default=None, parent=wind)
    checkbox_group.set_label("CheckBoxGroup")
    print()

    checkbox = CheckBox()

    layout.addWidget(combo)
    layout.addWidget(combo_edit)
    layout.addWidget(radio_group)
    layout.addWidget(checkbox_group)
    layout.addWidget(checkbox)
    wind.show()

    app.exec()


if __name__ == "__main__":
    __test_main()
