from function2widgets.widgets.editor.codeeditor import CodeEditor
from function2widgets.widgets.editor.dicteditor import DictEditor
from function2widgets.widgets.lineedit import IntLineEdit, FloatLineEdit, LineEdit
from function2widgets.widgets.editor.jsoneditor import JsonEditor
from function2widgets.widgets.editor.listeditor import ListEditor
from function2widgets.widgets.numberinput import IntSpinBox, FloatSpinBox, Dial, Slider
from function2widgets.widgets.pathedit import PathEdit, FilePathEdit, DirPathEdit
from function2widgets.widgets.selectwidget.combobox import ComboBox
from function2widgets.widgets.selectwidget import (
    ComboBoxEdit,
    RadioButtonGroup,
    CheckBoxGroup,
    CheckBox,
)
from function2widgets.widgets.textedit import PlainTextEdit, CodeEdit
from function2widgets.widgets.editor.tupleeditor import TupleEditor
from function2widgets.widgets.misc import DateTimeEdit, DateEdit, TimeEdit, ColorEdit

BASIC_PARAMETER_WIDGETS = {
    LineEdit.__name__: LineEdit,
    IntLineEdit.__name__: IntLineEdit,
    FloatLineEdit.__name__: FloatLineEdit,
    PathEdit.__name__: PathEdit,
    FilePathEdit.__name__: FilePathEdit,
    DirPathEdit.__name__: DirPathEdit,
    PlainTextEdit.__name__: PlainTextEdit,
    CodeEdit.__name__: CodeEdit,
    CodeEditor.__name__: CodeEditor,
    JsonEditor.__name__: JsonEditor,
    DictEditor.__name__: DictEditor,
    ListEditor.__name__: ListEditor,
    TupleEditor.__name__: TupleEditor,
    ComboBox.__name__: ComboBox,
    ComboBoxEdit.__name__: ComboBoxEdit,
    CheckBox.__name__: CheckBox,
    RadioButtonGroup.__name__: RadioButtonGroup,
    CheckBoxGroup.__name__: CheckBoxGroup,
    IntSpinBox.__name__: IntSpinBox,
    FloatSpinBox.__name__: FloatSpinBox,
    Dial.__name__: Dial,
    Slider.__name__: Slider,
    DateEdit.__name__: DateEdit,
    TimeEdit.__name__: TimeEdit,
    DateTimeEdit.__name__: DateTimeEdit,
    ColorEdit.__name__: ColorEdit,
}
