import typing

from function2widgets.widgets.codeeditor import UniversalSourceCodeEditor, JsonEditor, ListEditor, TupleEditor, DictEditor
from function2widgets.widgets.lineedit import LineEdit, IntLineEdit, FloatLineEdit
from function2widgets.widgets.textedit import PlainTextEdit, SourceCodeEdit
from function2widgets.widgets.selectwidget import ComboBox, ComboBoxEdit, RadioButtonGroup, CheckBoxGroup, CheckBox
from function2widgets.widgets.numberedit import IntSpinBox, FloatSpinBox, Dial, Slider
from function2widgets.widgets.pathedit import PathEdit, FilePathEdit, DirPathEdit

BASIC_PARAMETER_WIDGETS = {
    LineEdit.__name__: LineEdit,
    IntLineEdit.__name__: IntLineEdit,
    FloatLineEdit.__name__: FloatLineEdit,
    PathEdit.__name__: PathEdit,
    FilePathEdit.__name__: FilePathEdit,
    DirPathEdit.__name__: DirPathEdit,
    PlainTextEdit.__name__: PlainTextEdit,
    SourceCodeEdit.__name__: SourceCodeEdit,
    UniversalSourceCodeEditor.__name__: UniversalSourceCodeEditor,
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
    Slider.__name__: Slider
}