from __future__ import annotations
from typing import Any, Union, List, Literal, TypedDict, overload, Optional, Tuple, Dict
from abc import ABCMeta, abstractmethod
from typing import Generator
from typing import Callable
import pandas as pd
from markdown import Markdown
from IPython.core.display import Markdown as Markdown, Math as Math
from fractions import Fraction as NativeFraction

##### ./tmp/src/plot_adapter.py #####


class PlotAdapter:
    """
    TableAdapterクラス
    """

    @staticmethod
    def set_table_index(
        data_frame: pd.DataFrame, column_name: Union[str, int, float]
    ) -> None:
        ...

    @staticmethod
    def remove_display_limit(direction: Literal["row", "column"]) -> None:
        ...

    @staticmethod
    def add_column(
        data_frame: pd.DataFrame,
        column_name: Union[str, int, float],
        body: List[Union[str, int, float]],
    ) -> None:
        ...

    @staticmethod
    def display_table(data_frame: pd.DataFrame) -> type["PlotAdapter"]:
        ...


class plotRangeClass(TypedDict):
    min: Union[float, int]
    max: Union[float, int]


class AxBase:
    """
    FigureのAxを表す親クラス
    """

    def __init__(self, ax: Any) -> None:
        ...


class FigureBase:
    """
    Figureを表す親クラス
    """

    def __init__(
        self,
        row_column: Tuple[int, int],
        size: Tuple[Union[int, float], Union[int, float]] = (15, 7.5),
        title: str = "",
    ) -> None:
        ...

    def show(self) -> FigureBase:
        ...


##### ./tmp/src/_ad.py #####

hex_rgb = Tuple[int, int, int]
hsl = Tuple[Union[float, int], Union[float, int], Union[float, int]]
hsla_full = Tuple[
    Union[float, int], Union[float, int], Union[float, int], Union[float, int]
]
hsla = Union[hsla_full, hsl]
plot_color = Literal[
    "aliceblue",
    "antiquewhite",
    "aqua",
    "aquamarine",
    "azure",
    "beige",
    "bisque",
    "black",
    "blanchedalmond",
    "blue",
    "blueviolet",
    "brown",
    "burlywood",
    "cadetblue",
    "chartreuse",
    "chocolate",
    "coral",
    "cornflowerblue",
    "cornsilk",
    "crimson",
    "cyan",
    "darkblue",
    "darkcyan",
    "darkgoldenrod",
    "darkgray",
    "darkgreen",
    "darkgrey",
    "darkkhaki",
    "darkmagenta",
    "darkolivegreen",
    "darkorange",
    "darkorchid",
    "darkred",
    "darksalmon",
    "darkseagreen",
    "darkslateblue",
    "darkslategray",
    "darkslategrey",
    "darkturquoise",
    "darkviolet",
    "deeppink",
    "deepskyblue",
    "dimgray",
    "dimgrey",
    "dodgerblue",
    "firebrick",
    "floralwhite",
    "forestgreen",
    "fuchsia",
    "gainsboro",
    "ghostwhite",
    "gold",
    "goldenrod",
    "gray",
    "green",
    "greenyellow",
    "grey",
    "honeydew",
    "hotpink",
    "indianred",
    "indigo",
    "ivory",
    "khaki",
    "lavender",
    "lavenderblush",
    "lawngreen",
    "lemonchiffon",
    "lightblue",
    "lightcoral",
    "lightcyan",
    "lightgoldenrodyellow",
    "lightgray",
    "lightgreen",
    "lightgrey",
    "lightpink",
    "lightsalmon",
    "lightseagreen",
    "lightskyblue",
    "lightslategray",
    "lightslategrey",
    "lightsteelblue",
    "lightyellow",
    "lime",
    "limegreen",
    "linen",
    "magenta",
    "maroon",
    "mediumaquamarine",
    "mediumblue",
    "mediumorchid",
    "mediumpurple",
    "mediumseagreen",
    "mediumslateblue",
    "mediumspringgreen",
    "mediumturquoise",
    "mediumvioletred",
    "midnightblue",
    "mintcream",
    "mistyrose",
    "moccasin",
    "navajowhite",
    "navy",
    "oldlace",
    "olive",
    "olivedrab",
    "orange",
    "orangered",
    "orchid",
    "palegoldenrod",
    "palegreen",
    "paleturquoise",
    "palevioletred",
    "papayawhip",
    "peachpuff",
    "peru",
    "pink",
    "plum",
    "powderblue",
    "purple",
    "rebeccapurple",
    "red",
    "rosybrown",
    "royalblue",
    "saddlebrown",
    "salmon",
    "sandybrown",
    "seagreen",
    "seashell",
    "sienna",
    "silver",
    "skyblue",
    "slateblue",
    "slategray",
    "slategrey",
    "snow",
    "springgreen",
    "steelblue",
    "tan",
    "teal",
    "thistle",
    "tomato",
    "turquoise",
    "violet",
    "wheat",
    "white",
    "whitesmoke",
    "yellow",
    "yellowgreen",
]
plotRange = Tuple[Union[int, float], Union[int, float]]
plotRanges = Dict[str, plotRange]
plotRange_2d = Tuple[plotRange, plotRange]
range_v1 = Tuple[Union[int, float], Union[int, float]]
range_v2 = Tuple[
    Tuple[Union[int, float], Union[int, float]],
    Tuple[Union[int, float], Union[int, float]],
]
variable_symbol = Any
formula_symbol = Any
variables = Dict[str, variable_symbol]


class equation(TypedDict):
    formula_left: str
    formula_right: str


operator_symbol = Literal[
    "+",
    "*",
    "**",
    "%",
    "log",
    "/",
    "sin",
    "cos",
    "tan",
    "&",
    "~",
    "|",
    "setInterval",
    "setIntervalUnion",
    "UniversalSet",
    "finite_set",
    "||",
    "floor",
    "sols",
]
#  'sin', 'cos', 'tan', '&', '~', '|', 'setInterval', 'setIntervalUnion', 'finite_set', '||', 'floor','sols']
number_symbol = Literal["oo", "-oo"]
equationSymbol = Literal["="]
conditionSymbol = Literal["True", "False"]
inequationSymbol = Literal["<", "<=", ">", ">="]
unequationSymbol = Literal["!="]
symbolRelationType = Literal[
    operator_symbol,
    number_symbol,
    conditionSymbol,
    equationSymbol,
    inequationSymbol,
    unequationSymbol,
]
symbolType = Literal[symbolRelationType, "symbol", conditionSymbol]


class vennData(TypedDict):
    label: str
    set: Union[set[int], set[str]]


class plotRange_eachVariable(TypedDict):
    min: Union[int, float]
    max: Union[int, float]
    symbol: str


sympyClass = Literal[
    "<class 'sympy.core.add.Add'>",
    "<class 'sympy.core.mul.Mul'>",
    "<class 'sympy.core.numbers.Half'>",
    "<class 'sympy.core.numbers.Infinity'>",
    "<class 'sympy.core.numbers.NegativeInfinity'>",
    "<class 'sympy.core.numbers.Rational'>",
    "<class 'sympy.core.power.Pow'>",
    "<class 'sympy.core.relational.Equality'>",
    "<class 'sympy.core.relational.GreaterThan'>",
    "<class 'sympy.core.relational.LessThan'>",
    "<class 'sympy.core.relational.StrictGreaterThan'>",
    "<class 'sympy.core.relational.StrictLessThan'>",
    "<class 'sympy.core.relational.Unequality'>",
    "<class 'sympy.sets.sets.EmptySet'>",
    "<class 'sympy.sets.sets.FiniteSet'>",
    "<class 'sympy.sets.sets.Interval'>",
    "<class 'sympy.sets.sets.Union'>",
    "<class 'sympy.sets.sets.UniversalSet'>",
    "<class 'sympy.logic.boolalg.BooleanFalse'>",
    "<class 'sympy.logic.boolalg.BooleanTrue'>",
    # "<class 'sympy.polys.rootoftools.ComplexRootOf'>",
    "Abs",
    "And",
    "cos",
    "floor",
    "log",
    "Mod",
    "Not",
    "Or",
    "sin",
    "tan",
]
sympyFunction2Operator: Dict[sympyClass, symbolRelationType]


class astElement(TypedDict):
    type: Literal["function", "symbol", "condition"]
    name: symbolType
    text: str
    argumentsLength: int
    arguments: List[astElement]


class variableType(TypedDict):
    real: bool
    integer: bool
    rational: bool
    positive: bool


class variableType_optional(TypedDict, total=False):
    real: Literal[True]
    integer: Literal[True]
    rational: Literal[True]
    positive: Literal[True]


##### ./tmp/src/ast.py #####


class Ast:
    """
    数式の抽象構文木を表現するクラス。

    数式の解析に使う。
    """

    @staticmethod
    def get_plotable_condition_list(
        ast: astElement,
        all_variables: variables,
        conditions: List[astElement] = [],
    ) -> List[astElement]:
        """
        抽象構文木からプロット可能な条件を抽出する。

        Parameters:
            ast: 解析する抽象構文木

            all_variables: すべての変数を含むDict。

            conditions: 既存の条件のリスト。


        Returns:
            プロット可能な条件のリスト。
        """
        ...

    def __init__(
        self,
        proof: Proof,
        express: str,
        assertee_operator: List[symbol_type] = [],
        variable_types: Union[variable_type_optional, variable_types_optional] = {},
    ) -> None:
        """
        数式の抽象構文木を表現するクラス。
        数式の解析に使う。

        Args:
            proof (Proof): 証明に関する情報。

            express (str): 解析する数式の文字列。

            assertee_operator (List[symbol_type], optional): 断定する関数のリスト。デフォルトは空のリスト。

            variable_types (Union[variable_type_optional, variable_types_optional], optional): 変数の型情報。デフォルトは空の辞書。
        """
        ...

    @property
    def ast_prettified_inequation_for_factorize(self) -> astElement:
        """
        数式を因数分解のための形式に変換した抽象構文木。

        Returns:
            astElement: 因数分解のために整形された抽象構文木。
        """
        ...

    @property
    def element(self) -> astElement:
        ...

    @property
    def element_not_evaluated(self) -> astElement:
        """
        このインスタンスの数式の抽象構文木を返します。

        Returns:
            astElement: 抽象構文木。
        """
        ...

    @property
    def evaluated(self) -> astElement:
        """
        数式の抽象構文木を評価した結果を返します。

        Returns:
            astElement: 評価された抽象構文木。
        """
        ...

    @property
    def factors(self) -> List[str]:
        """
        因数s。

        Returns:
            List[str]: 因数のリスト。
        """
        ...

    @property
    def text(self) -> str:
        """
        抽象構文木をテキスト形式で取得します。

        Returns:
            str: 抽象構文木のテキスト形式。
        """
        ...

    @property
    def variables(self) -> set[str]:
        """
        式中の変数を取得します。

        Returns:
            set[str]: 式中の変数の集合。
        """
        ...

    def assert_operator(
        self,
        assertee_operator: List[symbol_type],
        should_regressive_search: bool = False,
    ) -> Ast:
        """
        数式に対して機能を適用します。

        Args:
            assertee_operator (List[DefineType.symbol_type]): 断定する関数のリスト。

            should_regressive_search (bool, optional): 逆順で検索するかどうか。デフォルトは False。


        Returns:
            Ast: 自分自身を返す。
        """
        ...

    def get_end_leafs(
        self,
        ast: Union[astElement, None] = None,
        leaf_type: List[symbol_relation_type] = [],
        leafs: List[astElement] = [],
    ) -> List[astElement]:
        """
        抽象構文木の末端のノードを取得する。

        Parameters:
            ast (astElement, 任意): 解析する抽象構文木。Noneの場合は、ast_prettified_inequation_for_factorizeを使用します。

            leaf_type (List[symbol_relation_type], 任意): 取得する末端ノードのタイプのリスト。最初は空のリスト。

            leafs (List[astElement], 任意): 既存の末端ノードのリスト。最初は空のリスト。


        Returns:
            List[astElement]: 末端のノードのリスト。
        """
        ...

    def get_power_term(self, ast: Union[astElement, None] = None) -> List[str]:
        """
        指定された抽象構文木からべき乗の項を抽出します。

        Parameters:
            ast (astElement, 任意): 解析する抽象構文木。Noneの場合は、elementプロパティを使用します。

        Returns:
            List[str]: べき乗の項のリスト。
        """
        ...


##### ./tmp/src/ax.py #####


class Ax(AxBase):
    """
    2Dグラフ描画用のクラス
    """

    def __init__(self, figure: Figure, ax: Any) -> None:
        ...

    def add_grid(self) -> Ax:
        ...

    def plot_condition(
        self,
        condition: SymbolCondition,
        axises: Union[List[str], None] = None,
        color: Union[hsla, None] = None,
    ) -> Ax:
        ...

    def plot_line_formula(
        self,
        formula: Union[Formula, str, float, int, NativeFraction],
        variable: str,
        color: hsla = (220, 100, 50),
        label: str = "",
    ) -> Ax:
        ...

    def plot_scatter_formula(
        self,
        data: Union[List[Position_x], Positions_list_x],
        formula: Union[Formula, str, float, int, NativeFraction],
        variable: str,
        color: Union[plot_color, hex_rgb] = "black",
        label: str = "",
    ) -> Ax:
        ...

    def plot_scatter_points(
        self,
        data: Union[List[Position], Positions_list],
        color: Union[plot_color, hex_rgb],
    ) -> Ax:
        ...

    def reset_label(self, labels: Tuple[str, str]) -> Ax:
        ...

    def reset_plot_property(
        self,
        property: Literal["dot_radius", "line_width", "z_oder"],
        value: Union[float, int],
    ) -> Ax:
        ...

    def reset_range(self, _range: plotRange_2d) -> Ax:
        """
        グラフ範囲の設定

        注意:
            再設定は、エリアの追加前にする必要がある。
        """
        ...

    def reset_title(self, title: str) -> Ax:
        """
        グラフ範囲の設定

        注意:
            再設定は、エリアの追加前にする必要がある。
        """
        ...

    def set_legend(self) -> Ax:
        ...


##### ./tmp/src/complex_condition.py #####


class ComplexCondition:
    """
    等式、不等式、非等号の論理結合
    """

    def __init__(self, proof: Proof, express: str) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def logical_tree(self) -> MarkdownContents:
        ...

    def can_cast(self, type: type_from_term_inequation) -> SymbolicBool:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    def display(self) -> ComplexCondition:
        ...

    def display_logical_tree(self) -> ComplexCondition:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> ComplexCondition:
        ...

    def __and__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        """
        論理和の中置演算子

        Args:
            other : 演算対象
        """
        ...

    def __eq__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __ge__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __gt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __invert__(self) -> symbol_condition:
        ...

    def __le__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lshift__(self, other: SymbolCondition) -> MathConditional:
        ...

    def __lt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ne__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __or__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...


class ComplexCondition_v1(ComplexCondition):
    """
    １変数のみの等式、不等式、非等号の論理結合
    """

    def __init__(self, proof: Proof, express: str) -> None:
        ...

    @property
    def range(self) -> markdown_str:
        ...

    def can_get_set_integer(
        self, set_limit: int = 1000, should_raise_error: bool = False
    ) -> bool:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    def display_range(self) -> ComplexCondition_v1:
        ...

    def get_set_integer(self, set_limit: int = 1000) -> set[int]:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def __sub__(
        self, formula: ComplexCondition_v1
    ) -> Union[ComplexCondition_v1, Equation]:
        ...


class ComplexCondition_v2(ComplexCondition):
    """
    ２変数のみの等式、不等式、非等号の論理結合
    """

    def __init__(self, proof: Proof, express: str) -> None:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...


##### ./tmp/src/conditional.py #####


class Conditional(metaclass=ABCMeta):
    """
    命題を取り扱う親クラス
    """

    def __init__(
        self,
        sufficient_condition: str,
        necessary_condition: str,
        sufficient_condition_bool: bool = True,
        necessary_condition_bool: bool = True,
    ) -> None:
        ...

    @property
    @abstractmethod
    def text(self) -> str:
        ...

    @property
    @abstractmethod
    def text_necessary_condition(self) -> str:
        ...

    @property
    @abstractmethod
    def text_sufficient_condition(self) -> str:
        ...

    @property
    def text_converse(self) -> str:
        ...

    @property
    def text_inverse(self) -> str:
        ...

    @property
    def text_contrapositive(self) -> str:
        ...

    @property
    def text_opposition(self) -> str:
        ...

    @property
    @abstractmethod
    def converse(self) -> Conditional:
        ...

    @property
    @abstractmethod
    def inverse(self) -> Conditional:
        ...

    @property
    @abstractmethod
    def contrapositive(self) -> Conditional:
        ...

    @property
    @abstractmethod
    def opposition(self) -> Conditional:
        ...

    def analyze_strategy(self) -> Conditional:
        ...

    def add_suffix(self, segment_index: Literal[0, 1], opinion: bool) -> str:
        ...


##### ./tmp/src/designed_float.py #####


class Float:
    """
    designed mathモジュールの浮動小数を表すクラス
    """

    def __init__(self, proof: Proof, express: float) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def degree(self) -> int:
        """
        式の最大の次数

        注意:
            整数多項式以外は、正しい結果を返さない。
            例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def ast(self) -> Ast.Ast:
        ...

    @property
    def is_integer(self) -> Union[bool, None]:
        ...

    @property
    def number(self) -> float:
        ...

    def can_cast(self, type: Union[type[Integer], type[Fraction]]) -> bool:
        ...

    def get_coefficients(
        self, focus_variable: str, should_limit_integer: bool = False
    ) -> List[Float]:
        ...

    def __eq__(self, other: term_) -> Union[SymbolicBool, Equation]:
        ...

    def __ne__(self, other: term_) -> Union[SymbolicBool, Unequation]:
        ...

    def __lt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __le__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __gt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __ge__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def display(self) -> Float:
        ...

    @overload
    def __add__(
        self,
        formula: Union[float, int, Float, Integer, Fraction],
    ) -> Float:
        ...

    @overload
    def __add__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __sub__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Float:
        ...

    @overload
    def __sub__(self, formula: Formula) -> Formula:
        ...

    def __neg__(self) -> Float:
        ...

    @overload
    def __mul__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Float:
        ...

    @overload
    def __mul__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __truediv__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Float:
        ...

    @overload
    def __truediv__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __mod__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Float:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, formula: Formula) -> Formula:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Integer:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(self, formula: Formula) -> Formula:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __pow__(
        self,
        formula: Union[
            Formula,
            float,
            int,
            Fraction,
            Integer,
            Float,
        ],
    ) -> Formula:
        """
        [**] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __radd__(self, formula: Union[float, int]) -> Float:
        """
        [+] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rsub__(self, formula: Union[float, int]) -> Float:
        """
        [-] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rmul__(self, formula: Union[float, int]) -> Float:
        """
        [*] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rtruediv__(self, formula: Union[float, int]) -> Float:
        """
        [/] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rpow__(self, formula: Union[float, int]) -> Formula:
        """
        [**] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rmod__(self, formula: Union[float, int]) -> Float:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rfloordiv__(self, formula: Union[float, int]) -> Integer:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rshift__(self, type: type[Integer]) -> Integer:
        ...

    @overload
    def __rshift__(self, type: type[Formula]) -> Formula:
        ...

    @overload
    def __rshift__(self, type: type[Fraction]) -> Fraction:
        ...


##### ./tmp/src/designed_range.py #####


class Range:
    """
    等式、不等式、非等号の論理結合による実数の範囲を表すクラス
    """

    def __init__(self, proof: Proof, express: str) -> None:
        ...

    @property
    def ast(self) -> Ast:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    def as_set(self, variable: str) -> Set:
        ...

    def can_get_set_integer(
        self,
        ast: Union[astElement, None] = None,
        set_limit: int = 1000,
        should_raise_error: bool = False,
    ) -> bool:
        ...

    def display(self) -> Range:
        ...

    def get_set_integer(
        self, ast: Union[astElement, None] = None, set_limit: int = 1000
    ) -> set[int]:
        ...

    def __or__(self, formula: Range) -> Union[Set, Range]:
        ...

    def __and__(self, formula: Range) -> Union[Set, Range]:
        ...

    def __sub__(self, formula: Range) -> Union[Set, Range]:
        ...

    def __eq__(self, formula: Range) -> bool:
        ...

    def __ne__(self, formula: Range) -> bool:
        ...

    def __lt__(self, formula: Range) -> bool:
        ...

    def __le__(self, formula: Range) -> bool:
        ...

    def __gt__(self, formula: Range) -> bool:
        ...

    def __ge__(self, formula: Range) -> bool:
        ...

    def __format__(self, __format_spec: str) -> markdown_str:
        ...


##### ./tmp/src/designed_set.py #####


class Set:
    """
    designed mathモジュールにおける集合を表すクラス。
    要素は基本的に、整数。
    """

    def __init__(
        self,
        proof: Proof,
        express: Union[
            express_str, express_str_set, express_int_set, express_float_set
        ] = set(),
    ) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def native_set(self) -> set[int]:
        ...

    def display(self) -> Set:
        ...


express_str = str
express_str_set = set[str]
express_int_set = set[int]
express_float_set = set[float]

##### ./tmp/src/diophantine_equation_utils.py #####


class DiophantineEquationUtils:
    """
    不定方程式を解くためのユーティリティクラス
    次数(dimensionのd), 変数(variableのv)でそれぞれ使い分ける。
    """

    @staticmethod
    def solve_diophantine_equation_d1_v2(
        equation: Equation,
        proof: Proof,
        parameter_symbol: str = "k_",
        search_range: Tuple[int, int] = (-5, 5),
        section_title: str = "１次２変数の不定方程式の解",
        section_id: str = "solve_diophantine_equation_d1_v2",
    ) -> VectorEquation:
        ...

    @staticmethod
    def solve_diophantine_equation_d1_v2_disassembly_type(
        equation: Equation,
        proof: Proof,
        section_title: str = "１次２変数の不定方程式(分解型)の解",
        section_id: str = "solve_diophantine_equation_d1_v2_disassembly_type",
    ) -> VectorSolutions:
        ...

    @staticmethod
    def solve_diophantine_equation_d2_v2_disassembly_type(
        equation: Equation,
        proof: Proof,
        is_natural_number: bool = False,
        section_title: str = "２次２変数の不定方程式(分解型)の解",
        section_id: str = "solve_diophantine_equation_d2_v2_disassembly_type",
    ) -> VectorSolutions:
        ...

    @staticmethod
    def solve_diophantine_equation_Add_and_subtract_products(
        proof: Proof,
        equation: add_and_subtract_products_equation,
        is_natural_number: bool = False,
        section_title: str = "２乗差の不定方程式の解",
        section_id: str = "solve_diophantine_equation_Add_and_subtract_products",
    ) -> VectorSolutions:
        ...

    @staticmethod
    def solve_diophantine_equation_symmetric(
        equation: Equation,
        proof: Proof,
        variable_size_order: List[str] = [],
        is_order_strict: bool = False,
        section_title: str = "対称式の不定方程式の解",
        section_id: str = "solve_diophantine_equation_symmetric",
    ) -> Union[VectorSolutions, None]:
        """
        対称不定方程式を解く

        注意
        ----------
        変数の大小関係の引数に柔軟に対応する拡張が必要かも。現実装は、対応範囲が狭い。
        解が自然数に限る

        Parameters
        ----------
        proof
        equation
            解くべき自然数不定方程式。右辺が整数である必要がある。
        variable_size_order:
            変数の大小関係
        is_order_strict
            大小関係が厳密か、等号を含むか

        Returns
        -------
        solutions:
            不定方程式の解のセット
        """
        ...

    @staticmethod
    def solve_equation_of_rapidly_increase_each_sides_difference(
        equation: Equation,
        proof: Proof,
        scan_range: Tuple[int, int] = (0, 10),
        section_title: str = "急速に差が開く等式の解法",
        section_id: str = "solve_equation_of_rapidly_increase_each_sides_difference",
    ) -> Solutions:
        ...

    @staticmethod
    def get_solution_range_of_diophantine_equation(
        equation: Equation,
        proof: Proof,
        variable_size_order: List[str],
        is_order_strict: bool = False,
        section_title: str = "不定方程式の解の範囲",
        section_id: str = "get_solution_range_of_diophantine_equation",
    ) -> List[Inequation]:
        ...


##### ./tmp/src/equation.py #####


class Equation:
    """
    一般的な方程式クラス
    """

    def __init__(self, proof: Proof, equation: Union[str, term_pair]) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    def __invert__(self) -> symbol_condition:
        """
        sum

        Args:
            x (int): 1st argument
            y (int): 2nd argument

        Returns:
            int: sum result

        Examples:
            >>> print(testfunc(2,5))
            7
        """
        ...

    def __and__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        """
        論理和の中置演算子

        Args:
            other : 演算対象
        """
        ...

    def __or__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        ...

    def __eq__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ne__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __le__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __gt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ge__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lshift__(self, other: SymbolCondition) -> MathConditional:
        ...

    def can_cast(self, type: type_from_term_inequation) -> SymbolicBool:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> SymbolCondition:
        ...

    @property
    def formulas(self) -> Tuple[Formula, Formula]:
        ...

    @property
    def text_forDisplay(self) -> str:
        ...

    @property
    def text_for_input(self) -> str:
        ...

    @property
    def degree(self) -> int:
        """
        式の最大の次数

        注意:
            整数多項式以外は、正しい結果を返さない。
            例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @property
    def variables(self) -> set[str]:
        """
        式の変数
        """
        ...

    @property
    def evaluated(self) -> Union[Equation, SymbolicBool]:
        ...

    def solve_diophantine_equation_d1_v2(
        self,
        parameter_symbol: str = "k_",
        search_range: Tuple[int, int] = (-5, 5),
        section_title: str = "１次２変数の不定方程式の解",
        section_id: str = "solve_diophantine_equation_d1_v2",
    ) -> VectorEquation:
        ...

    def solve_diophantine_equation_d1_v2_disassembly_type(
        self,
        section_title: str = "１次２変数の不定方程式(分解型)の解",
        section_id: str = "solve_diophantine_equation_d1_v2_disassembly_type",
    ) -> VectorSolutions:
        ...

    def solve_diophantine_equation_d2_v2_disassembly_type(
        self,
        is_natural_number: bool = False,
        section_title: str = "２次２変数の不定方程式(分解型)の解",
        section_id: str = "solve_diophantine_equation_d2_v2_disassembly_type",
    ) -> VectorSolutions:
        ...

    def solve_diophantine_equation_Add_and_subtract_products(
        self,
        equation: add_and_subtract_products_equation,
        is_natural_number: bool = False,
        section_title: str = "２乗差の不定方程式の解",
        section_id: str = "solve_diophantine_equation_Add_and_subtract_products",
    ) -> VectorSolutions:
        ...

    def solve_diophantine_equation_symmetric(
        self,
        variable_size_order: List[str] = [],
        is_order_strict: bool = False,
        section_title: str = "対称式の不定方程式の解",
        section_id: str = "solve_diophantine_equation_symmetric",
    ) -> Union[VectorSolutions, None]:
        """
        対称不定方程式を解く

        注意
        ----------
        変数の大小関係の引数に柔軟に対応する拡張が必要かも。現実装は、対応範囲が狭い。
        解が自然数に限る

        Parameters
        ----------
        proof
        equation
            解くべき自然数不定方程式。右辺が整数である必要がある。
        variable_size_order:
            変数の大小関係
        is_order_strict
            大小関係が厳密か、等号を含むか

        Returns
        -------
        solutions:
            不定方程式の解のセット
        """
        ...

    def solve_equation_of_rapidly_increase_each_sides_difference(
        self,
        scan_range: Tuple[int, int] = (0, 10),
        section_title: str = "急速に差が開く等式の解法",
        section_id: str = "solve_equation_of_rapidly_increase_each_sides_difference",
    ) -> Solutions:
        ...

    def substitute(
        self,
        conditions: Union[dict_float, dict_int, dict_term, Equation, Equations],
        side: Union[literal_direction, None] = None,
    ) -> Equation:
        ...

    def get_solution_range_of_diophantine_equation(
        self,
        variable_size_order: List[str],
        is_order_strict: bool = False,
        section_title: str = "不定方程式の解の範囲",
        section_id: str = "get_solution_range_of_diophantine_equation",
    ) -> List[Inequation]:
        ...

    def is_definition(self) -> bool:
        ...

    def display(self, is_raw: bool = True) -> Equation:
        ...

    def solve(self, focus_variable: Union[str, Formula]) -> FormulaVector:
        ...

    def is_identity(self) -> bool:
        ...

    def factorize(self) -> Equation:
        ...

    def get_particular_solution_d1_v2(
        self, search_range: Tuple[int, int]
    ) -> Union[dict_int, None]:
        ...

    def __add__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [+] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __sub__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [-] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __neg__(self) -> Fraction:
        ...

    def __mul__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [*] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __truediv__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [/] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __pow__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [**] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __radd__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [+] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rsub__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [-] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rmul__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [*] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rtruediv__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [/] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rpow__(
        self,
        equation_or_term: Union[
            Equation,
            Term,
            int,
            float,
            NativeFraction,
        ],
    ) -> Equation:
        """
        [**] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[DefineEquation]) -> DefineEquation:
        ...

    @overload
    def __rshift__(self, type: type[ExplainEquation]) -> ExplainEquation:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...


class Equation_2d(Equation):
    """
    2次(dimensionのd)の方程式クラス。
    """

    def __init__(
        self,
        proof: Proof,
        equation: Union[str, term_pair],
        main_variable: str = "",
    ) -> None:
        ...

    @property
    def vietas_formulas_product(self) -> Formula:
        ...

    @property
    def vietas_formulas_addition(self) -> Formula:
        ...

    @property
    def discriminant(self) -> Formula:
        ...

    @property
    def a(self) -> Formula:
        ...

    @property
    def b(self) -> Formula:
        ...

    @property
    def c(self) -> Formula:
        ...


class ExplainEquation(Equation):
    """
    左辺が単一の変数である、説明式クラス。
    """

    def __init__(self, proof: Proof, equation: Union[str, formula_term_pair]) -> None:
        ...


class DefineEquation(ExplainEquation):
    """
    定義式クラス。
    """

    def __init__(self, proof: Proof, equation: Union[str, formula_term_pair]) -> None:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...


term_pair = Tuple[term, term]
formula_term_pair = Tuple[Formula, term]
dict_float = Dict[str, float]
dict_int = Dict[str, int]
dict_term = Dict[str, Term]
literal_direction = Literal["left", "right"]

##### ./tmp/src/equation_utils.py #####

default_condition: condition


class EquationUtils:
    """
    方程式のユーティリティクラス
    """

    @staticmethod
    def adjust_function(
        proof: Proof,
        equation: Equation,
        adjust_function_symbol: Literal["+", "-", "*", "/", "**"],
        equation_or_term: Union[
            Equation,
            Term,
            float,
            int,
            NativeFraction,
        ],
        is_operate_from_right: bool = True,
    ) -> Equation:
        ...


##### ./tmp/src/equations.py #####


class Equations:
    """
    連立方程式クラス
    """

    def __init__(
        self, proof: Proof, equations: Union[express_list, express_tuple]
    ) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def equations(self) -> List[Equation]:
        ...

    def add_equation(self, equations: List[Equation]) -> Equations:
        ...

    def append(self, equation: Equation) -> Equations:
        ...

    def solve(self, focus_terms: set[str] = set()) -> Union[VectorEquation, None]:
        ...

    def display(self) -> Equations:
        ...

    def reduce_variable(
        self,
        target_variable: str = "",
        define_equation: Union[Equation, None] = None,
    ) -> Equations:
        ...

    def __getitem__(self, index: int) -> Equation:
        ...

    def __iter__(self) -> Generator[Equation, None, None]:
        ...

    def __len__(self) -> int:
        ...


class Solutions(Equations):
    """
    それぞれの変数について説かれた形の連立方程式クラス
    """

    def __init__(
        self,
        proof: Proof,
        equations: Union[List[Equation], Tuple[Vector, Vector]],
    ) -> None:
        ...

    def sort(self, should_reverse: bool = False) -> Solutions:
        ...

    def display(self) -> Solutions:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __add__(self, other: Solutions) -> Solutions:
        """
        [+] の中置演算子

        引数:
            other: Vector
        結果:
            Vector
        """
        ...


class VectorEquation(Equations):
    """
    ベクトル方程式クラス
    """

    def __init__(
        self,
        proof: Proof,
        equations: Union[List[Equation], Tuple[Vector, Vector]],
    ) -> None:
        ...

    @property
    def left_side_vector(self) -> Vector:
        ...

    @property
    def right_side_vector(self) -> Vector:
        ...

    def add_equation(self, equations: List[Equation]) -> VectorEquation:
        ...

    def append(self, equation: Equation) -> VectorEquation:
        ...

    def sort(self, should_reverse: bool = False) -> VectorEquation:
        ...

    def display(self) -> VectorEquation:
        ...

    def __eq__(self, other: VectorEquation) -> bool:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...


express_list = List[Equation]
express_tuple = Tuple[Vector, Vector]

##### ./tmp/src/figure.py #####


class Figure(FigureBase):
    """
    グラフの描画クラス。
    """

    def __init__(
        self,
        proof: Proof,
        row_column: Tuple[int, int],
        unit_size: Tuple[Union[int, float], Union[int, float]] = (5, 5),
        title: str = "",
    ) -> None:
        ...

    @property
    def proof(self) -> Proof:
        ...

    @property
    def axes(self) -> List[List[Ax]]:
        ...

    def add_subplot(self, row_column: Tuple[int, int]) -> Figure:
        ...

    def display(self) -> Figure:
        ...


##### ./tmp/src/figure_reservation.py #####


class FigureReservation:
    """
    図形登録クラス。
    図形クラスはインスタンスが定義された断面でレンダリングされ、出力の並びが狂うため、表示を先送りするためのクラス。
    """

    def __init__(
        self,
        express: Union[SymbolCondition, Formula],
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> None:
        ...

    def display(self) -> FigureReservation:
        ...


##### ./tmp/src/formula.py #####


class Formula:
    """
    数字、定数、変数、演算子で構成された数式を表すクラス。
    """

    def __init__(
        self,
        proof: Proof,
        text: Union[str, float, int],
        variable_types: Union[variable_type_optional, variable_types_optional] = {},
    ) -> None:
        ...

    @property
    def ast(self) -> Ast.Ast:
        ...

    @property
    def completing_square(self) -> squared_result:
        ...

    @property
    def degree(self) -> int:
        ...

    @property
    def factorized_elements(self) -> List[Formula]:
        """
        因数分解の因数(次数なし)
        """
        ...

    @property
    def is_integer(self) -> Union[bool, None]:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def text_factorized(self) -> str:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    def can_cast(
        self,
        type: Union[
            type[Integer],
            type[Float],
            type[Fraction],
        ],
    ) -> bool:
        ...

    def check_fo_symmetry(self) -> SymbolicBool:
        ...

    def display(self) -> Formula:
        ...

    def differentiate(
        self, focus_variable: Union[str, Formula, None] = None
    ) -> Formula:
        ...

    def expand(self) -> Formula:
        ...

    def factorize(self) -> Formula:
        """
        caution!: 数字のみの項のある因数分解は失敗するlx:(4+4*x)。sympifyで変換する際に、4*(1+x)が展開されてしまう。代わりに、factorized_elementsを使用する
        """
        ...

    def fragile_substitute(self, subsitutee: Tuple[str, Formula]) -> Formula:
        ...

    def get_coefficients(
        self, focus_variable: str, should_limit_integer: bool = False
    ) -> List[Formula]:
        ...

    def get_factors(self) -> List[Formula]:
        ...

    def identify_from_condition(
        self,
        divisor_quantity: int,
        range: Tuple[int, int],
        section_title: str = "同定する_条件から",
        section_id: str = "identify_from_condition",
    ) -> Vector:
        ...

    def integrate(self, focus_variable: Union[str, Formula, None] = None) -> Formula:
        ...

    def is_integer_rough_check(
        self, rough_search: bool = False, only_positive: bool = True
    ) -> Union[bool, None]:
        ...

    def is_specific_times(
        self,
        times: int,
        expected_mod: List[int],
        condition: condition = {"times": 0, "mod": [0]},
        section_title: str = "proof_specific_times",
    ) -> bool:
        ...

    def is_relatively_prime(
        self,
        other: Union[Integer, int, Formula],
        relational_prime_pairs: List[
            Tuple[
                Union[int, Integer, Formula],
                Union[int, Integer, Formula],
            ]
        ] = [],
    ) -> Union[bool, None]:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ] = None,
        title: str = "",
    ) -> Figure:
        ...

    def make_uni_variantization(self, target_variable: str) -> Formula:
        ...

    def rough_check_monotonically_increase(
        self, points: Optional[List[int]] = None, is_in_Natural: bool = True
    ) -> Union[bool, None]:
        ...

    def solve(self, focus_variable: Union[str, Formula, None] = None) -> FormulaVector:
        ...

    def substitute(
        self,
        conditions: Union[
            conditions_float,
            conditions_int,
            conditions_str,
            conditions_term,
            Equation,
            Equations,
        ],
    ) -> Formula:
        ...

    def proof_powers_modularity(
        self,
        mod: int,
        section_title: str = "乗数の剰余",
        section_id: str = "proof_powers_modularity",
    ) -> Formula:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ] = None,
        title: str = "",
        color: hsla = (220, 100, 50),
        label: str = "",
    ) -> Formula:
        ...

    def __lt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __le__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __gt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __ge__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __add__(
        self,
        other: Union[
            float,
            int,
            Integer,
            Float,
            Fraction,
            Formula,
        ],
    ) -> Formula:
        """
        [+] の中置演算子

        引数:
            other: 演算子の左側の式
        結果:
            Formula
        """
        ...

    def __sub__(
        self,
        other: Union[
            Formula,
            float,
            int,
            Fraction,
            Integer,
            Float,
        ],
    ) -> Formula:
        """
        [-] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __neg__(self) -> Formula:
        ...

    def __mul__(
        self,
        other: Union[
            Formula,
            float,
            int,
            Fraction,
            Integer,
            Float,
        ],
    ) -> Formula:
        """
        [*] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __truediv__(
        self,
        other: Union[
            Formula,
            float,
            int,
            Fraction,
            Integer,
            Float,
        ],
    ) -> Formula:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __pow__(
        self,
        other: Union[
            Formula,
            float,
            int,
            Fraction,
            Integer,
            Float,
        ],
    ) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __mod__(self, other: Union[Formula, float, int, Integer, Float]) -> Formula:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __floordiv__(
        self, other: Union[Formula, float, int, Integer, Float]
    ) -> Formula:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __radd__(self, other: Union[float, int]) -> Formula:
        """
        [+] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rsub__(self, other: Union[float, int]) -> Formula:
        """
        [-] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rmul__(self, other: Union[float, int]) -> Formula:
        """
        [*] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rtruediv__(self, other: Union[float, int]) -> Formula:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rpow__(self, other: Union[float, int]) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rmod__(self, other: Union[float, int]) -> Formula:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rfloordiv__(self, other: Union[float, int]) -> Formula:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __eq__(self, other: str) -> str:
        ...

    @overload
    def __eq__(self, other: term_) -> Union[SymbolicBool, Equation]:
        ...

    @overload
    def __ne__(self, other: str) -> str:
        ...

    @overload
    def __ne__(self, other: term_) -> Union[SymbolicBool, Unequation]:
        ...

    def check_operator(self, check_operator: List[symbol_type]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Float]) -> Float:
        ...

    @overload
    def __rshift__(self, type: type[Fraction]) -> Fraction:
        ...

    @overload
    def __rshift__(self, type: type[Integer]) -> Integer:
        ...


##### ./tmp/src/formula_utils.py #####


class FormulaUtils:
    """
    式のutilクラス
    """

    @staticmethod
    def identify_from_condition(
        proof: Proof,
        formula: Formula,
        divisor_quantity: int,
        range: Tuple[int, int],
        section_title: str = "同定する_条件から",
        section_id: str = "identify_from_condition",
    ) -> Vector:
        ...

    @staticmethod
    def is_specific_times(
        proof: Proof,
        formula: Formula,
        times: int,
        expected_mod: List[int],
        condition: condition = {"times": 0, "mod": [0]},
        section_title: str = "proof_specific_times",
    ) -> bool:
        ...

    @staticmethod
    def substitute(
        proof: Proof,
        formula: Formula,
        conditions: Union[
            conditions_float,
            conditions_int,
            conditions_str,
            conditions_term,
            Equation,
            Equations,
        ],
    ) -> Formula:
        ...

    @staticmethod
    def adjust_function_right(
        proof: Proof,
        formula: Formula,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Union[
            Integer,
            int,
            Float,
            float,
            Fraction,
            Formula,
        ],
    ) -> Formula:
        ...

    @staticmethod
    def adjust_function_left(
        proof: Proof,
        formula: Formula,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Union[
            Integer,
            int,
            Float,
            float,
            Fraction,
            Formula,
        ],
    ) -> Formula:
        ...

    @staticmethod
    def proof_powers_modularity(
        proof: Proof,
        formula: Formula,
        mod: int,
        section_title: str = "乗数の剰余",
        section_id: str = "proof_powers_modularity",
    ) -> type["FormulaUtils"]:
        ...

    @staticmethod
    def subtract_prime(proof: Proof, term: astElement) -> subtract_prime_result:
        ...

    @staticmethod
    def subtract_term(
        proof: Proof,
        formula: Formula,
        other: Formula,
    ) -> Tuple[subtract_prime_result, subtract_prime_result]:
        ...


##### ./tmp/src/fraction.py #####


class Fraction:
    """
    designed mathモジュールにおける分数クラス。
    """

    def __init__(self, proof: Proof, express: Union[str, express_fraction]) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def degree(self) -> int:
        """
        式の最大の次数

        注意:
            整数多項式以外は、正しい結果を返さない。
            例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def ast(self) -> Ast.Ast:
        ...

    @property
    def is_integer(self) -> Union[bool, None]:
        ...

    @property
    def numerator(self) -> int:
        ...

    @property
    def denominator(self) -> int:
        ...

    @property
    def number(self) -> Union[int, NativeFraction]:
        ...

    def can_cast(self, type: Union[type[Float], type[Integer]]) -> bool:
        ...

    def get_coefficients(
        self, focus_variable: str, should_limit_integer: bool = False
    ) -> List[Fraction]:
        ...

    def __eq__(self, other: term_) -> Union[SymbolicBool, Equation]:
        ...

    def __ne__(self, other: term_) -> Union[SymbolicBool, Unequation]:
        ...

    def __lt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __le__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __gt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __ge__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def display(self) -> Fraction:
        ...

    @overload
    def __rshift__(self, type: type[Float]) -> Float:
        ...

    @overload
    def __rshift__(self, type: type[Formula]) -> Formula:
        ...

    @overload
    def __rshift__(self, type: type[Integer]) -> Integer:
        ...

    @overload
    def __add__(
        self, formula: Union[Integer, int, Fraction]
    ) -> Union[Fraction, Integer]:
        ...

    @overload
    def __add__(self, formula: Union[Float, float]) -> Float:
        ...

    @overload
    def __add__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __sub__(
        self, formula: Union[Integer, int, Fraction]
    ) -> Union[Fraction, Integer]:
        ...

    @overload
    def __sub__(self, formula: Union[Float, float]) -> Float:
        ...

    @overload
    def __sub__(self, formula: Formula) -> Formula:
        ...

    def __neg__(self) -> Fraction:
        ...

    @overload
    def __mul__(
        self, formula: Union[Integer, int, Fraction]
    ) -> Union[Fraction, Integer]:
        ...

    @overload
    def __mul__(self, formula: Union[Float, float]) -> Float:
        ...

    @overload
    def __mul__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __truediv__(
        self, formula: Union[Integer, int, Fraction]
    ) -> Union[Fraction, Integer]:
        ...

    @overload
    def __truediv__(self, formula: Union[Float, float]) -> Float:
        ...

    @overload
    def __truediv__(self, formula: Formula) -> Formula:
        ...

    @overload
    def __mod__(
        self, formula: Union[Integer, int, Fraction]
    ) -> Union[Integer, Fraction]:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, formula: Union[float, Float]) -> Float:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, formula: Formula) -> Formula:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(
        self,
        formula: Union[Integer, int, Float, float, Fraction],
    ) -> Integer:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(self, formula: Formula) -> Formula:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __pow__(
        self,
        formula: Union[
            Integer,
            int,
            Float,
            float,
            Fraction,
            Formula,
        ],
    ) -> Formula:
        ...

    @overload
    def __radd__(self, formula: Union[int, Integer]) -> Union[Fraction, Integer]:
        ...

    @overload
    def __radd__(self, formula: float) -> Float:
        ...

    @overload
    def __rsub__(self, formula: Union[int, Integer]) -> Union[Fraction, Integer]:
        ...

    @overload
    def __rsub__(self, formula: float) -> Float:
        ...

    @overload
    def __rmul__(self, formula: Union[int, Integer]) -> Union[Fraction, Integer]:
        ...

    @overload
    def __rmul__(self, formula: float) -> Float:
        ...

    @overload
    def __rtruediv__(self, formula: Union[int, Integer]) -> Union[Fraction, Integer]:
        ...

    @overload
    def __rtruediv__(self, formula: float) -> Float:
        ...

    @overload
    def __rmod__(self, formula: Union[int, Integer]) -> Union[Integer, Fraction]:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rmod__(self, formula: float) -> Float:
        """
        [%] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    def __rfloordiv__(self, formula: Union[float, int]) -> Integer:
        """
        [//] の中置演算子

        引数:
            formula: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rpow__(self, formula: Union[int, Integer]) -> Union[Fraction, Integer]:
        ...

    @overload
    def __rpow__(self, formula: float) -> Formula:
        ...


express_fraction = Tuple[
    Union[int, float, NativeFraction],
    Union[int, float, NativeFraction],
]

##### ./tmp/src/inequation.py #####


class Inequation:
    """
    不等式を表すクラス
    """

    def __init__(
        self,
        proof: Proof,
        express: Union[str, express_inequation],
        is_strict_mode: bool = False,
    ) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    def __invert__(self) -> symbol_condition:
        ...

    def __and__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        """
        論理和の中置演算子

        Args:
            other : 演算対象
        """
        ...

    def __or__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        ...

    def __eq__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ne__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __le__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __gt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ge__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lshift__(self, other: SymbolCondition) -> MathConditional:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> SymbolCondition:
        ...

    @property
    def formulas(self) -> Tuple[Formula, Formula]:
        ...

    @property
    def text_factorized(self) -> str:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def degree(self) -> int:
        """
        式の最大の次数

        注意:
            整数多項式以外は、正しい結果を返さない。
            例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @property
    def solved(
        self,
    ) -> Union[Inequation, SymbolicBool, ComplexCondition]:
        ...

    @property
    def evaluated(self) -> Union[Inequation, SymbolicBool]:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    def can_cast(self, type: type_from_term_inequation) -> SymbolicBool:
        ...

    def factorize(self) -> Inequation:
        ...

    def display(
        self,
        state: Literal[
            "row", "factorized", "factorized_and_split"
        ] = "factorized_and_split",
    ) -> Inequation:
        ...


class Inequation_v1(Inequation):
    """
    1変数のみの不等式を表すクラス。
    """

    def __init__(
        self,
        proof: Proof,
        express: Union[str, express_inequation],
        is_strict_mode: bool = False,
    ) -> None:
        ...

    @property
    def range(self) -> markdown_str:
        ...

    def can_get_set_integer(
        self, set_limit: int = 1000, should_raise_error: bool = False
    ) -> bool:
        ...

    def __sub__(
        self, formula: Inequation_v1
    ) -> Union[ComplexCondition_v2, ComplexCondition_v1, Equation,]:
        ...

    def __eq__(self, formula: Inequation_v1) -> bool:
        ...

    def __ne__(self, formula: Inequation_v1) -> bool:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    def get_set_integer(self, set_limit: int = 1000) -> set[int]:
        ...


class Inequation_v2(Inequation):
    """
    2変数のみの不等式を表すクラス。
    """

    def __init__(
        self,
        proof: Proof,
        express: Union[str, express_inequation],
        is_strict_mode: bool = False,
    ) -> None:
        ...

    def __sub__(self, formula: Inequation_v1) -> Union[ComplexCondition_v2, Equation]:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...


express_inequation = Tuple[term, term]
literal_eq = Literal["="]

##### ./tmp/src/integer.py #####


class Integer:
    """
    整数を扱うクラスです。
    """

    def __init__(self, proof: Proof, express: int) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        """
        変数のセットを返します。
        """
        ...

    @property
    def degree(self) -> int:
        """
        式の最大の次数を返します。

        注意:

        整数多項式以外は、正しい結果を返さない。

        例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @property
    def text(self) -> str:
        """
        テキスト表現を返します。
        """
        ...

    @property
    def ast(self) -> Ast.Ast:
        """
        AST表現を返します。
        """
        ...

    @property
    def is_integer(self) -> Union[bool, None]:
        """
        整数であるかどうかを返します。
        """
        ...

    @property
    def number(self) -> int:
        """
        数値表現を返します。
        """
        ...

    @property
    def is_prime(self) -> bool:
        """
        素数であるかどうかを返します。
        """
        ...

    @property
    def divisor_quantity(self) -> Integer:
        """
        約数の個数を返します。
        """
        ...

    @property
    def divisor_summary(self) -> Integer:
        """
        約数の和を返します。
        """
        ...

    @property
    def divisors(self) -> List[int]:
        """
        約数のリストを返します。
        """
        ...

    @staticmethod
    def proof_having_rational_root_2_be_integer(
        proof: Proof,
        root: str = "m",
        numerator: str = "q",
        denominator: str = "l",
        section_title: str = "無理数の証明",
    ) -> bool:
        """
        「有理平方根を持つならば整数」ことを証明します。
        """
        ...

    @staticmethod
    def proof_prime_exist_indefinitely(
        proof: Proof,
        section_title: str = "証明する_素数が無限に存在すること",
        section_id: str = "proof_prime_exist_indefinitely",
    ) -> Integer:
        """
        素数が無限に存在することを証明します。
        """
        ...

    def prime_factorize(self) -> Dict[int, int]:
        """
        素因数分解を行い、結果を返します。
        """
        ...

    def get_primes_up_to_self(self) -> List[int]:
        """
        自身までの素数のリストを返します。
        """
        ...

    def can_cast(self, type: Union[type[Float], type[Fraction]]) -> bool:
        """
        キャストが可能かどうかを返します。
        """
        ...

    def get_coefficients(
        self, focus_variable: str, should_limit_integer: bool = False
    ) -> List[Integer]:
        """
        係数を返します。
        """
        ...

    @overload
    def is_relatively_prime(
        self,
        other: Union[Integer, int],
        relational_prime_pairs: List[
            Tuple[
                Union[int, Integer, Formula],
                Union[int, Integer, Formula],
            ]
        ] = [],
    ) -> bool:
        """
        互いに素であるかどうかを返します。
        """
        ...

    @overload
    def is_relatively_prime(
        self,
        other: Formula,
        relational_prime_pairs: List[
            Tuple[
                Union[int, Integer, Formula],
                Union[int, Integer, Formula],
            ]
        ] = [],
    ) -> Union[bool, None]:
        """
        互いに素であるかどうかを返します。
        """
        ...

    def get_split_pair_in_to_product(
        self,
        uniqueness: Literal["combination", "order"] = "order",
        is_include_minus: bool = False,
    ) -> set[Tuple[int, int]]:
        """
        積に分解したペアを返します。
        """
        ...

    def __ne__(self, other: term_) -> Union[SymbolicBool, Unequation]:
        """
        不等式関係を評価します。
        """
        ...

    def __lt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        """
        より小さい関係を評価します。
        """
        ...

    def __le__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        """
        以下の関係を評価します。
        """
        ...

    def __gt__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        """
        より大きい関係を評価します。
        """
        ...

    def __ge__(self, other: term_) -> Union[SymbolicBool, Inequation]:
        """
        以上の関係を評価します。
        """
        ...

    def __format__(self, __format_spec: str) -> str:
        """
        フォーマットされたテキストを返します。
        """
        ...

    def display(self) -> Integer:
        """
        表示します。
        """
        ...

    @overload
    def __rshift__(self, type: type[Float]) -> Float:
        ...

    @overload
    def __rshift__(self, type: type[Formula]) -> Formula:
        ...

    @overload
    def __rshift__(self, type: type[Fraction]) -> Fraction:
        ...

    @overload
    def __rshift__(self, type: type[Integer]) -> Integer:
        ...

    @overload
    def __add__(self, other: Union[Integer, int]) -> Integer:
        ...

    @overload
    def __add__(self, other: Fraction) -> Fraction:
        ...

    @overload
    def __add__(self, other: Union[Float, float]) -> Float:
        ...

    @overload
    def __add__(self, other: Formula) -> Formula:
        ...

    @overload
    def __sub__(self, other: Union[Integer, int]) -> Integer:
        ...

    @overload
    def __sub__(self, other: Fraction) -> Fraction:
        ...

    @overload
    def __sub__(self, other: Union[Float, float]) -> Float:
        ...

    @overload
    def __sub__(self, other: Formula) -> Formula:
        ...

    def __neg__(self) -> Integer:
        ...

    @overload
    def __mul__(self, other: Union[Integer, int]) -> Integer:
        ...

    @overload
    def __mul__(self, other: Fraction) -> Fraction:
        ...

    @overload
    def __mul__(self, other: Union[Float, float]) -> Float:
        ...

    @overload
    def __mul__(self, other: Formula) -> Formula:
        ...

    @overload
    def __truediv__(
        self, other: Union[Integer, int, Fraction]
    ) -> Union[Fraction, Integer]:
        ...

    @overload
    def __truediv__(self, other: Union[Float, float]) -> Float:
        ...

    @overload
    def __truediv__(self, other: Formula) -> Formula:
        ...

    @overload
    def __mod__(self, other: Union[Integer, int]) -> Integer:
        """
        [%] の中置演算子

        引数:
            other: Union[Integer, int]
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, other: Fraction) -> Union[Integer, Fraction]:
        """
        [%] の中置演算子

        引数:
            other: Fraction
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, other: Union[float, Float]) -> Float:
        """
        [%] の中置演算子

        引数:
            other: Float
        結果:
            Formula
        """
        ...

    @overload
    def __mod__(self, other: Formula) -> Formula:
        """
        [%] の中置演算子

        引数:
            other: Formula
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(
        self, other: Union[Integer, int, Float, float, Fraction]
    ) -> Integer:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __floordiv__(self, other: Formula) -> Formula:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __pow__(self, other: Union[Integer, int]) -> Integer:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __pow__(
        self,
        other: Union[Formula, float, Float, Fraction],
    ) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __radd__(self, other: Union[int, Integer]) -> Integer:
        """
        [+] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __radd__(self, other: float) -> Float:
        """
        [+] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rsub__(self, other: Union[int, Integer]) -> Integer:
        """
        [-] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rsub__(self, other: float) -> Float:
        """
        [-] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rmul__(self, other: Union[int, Integer]) -> Integer:
        """
        [*] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rmul__(self, other: float) -> Float:
        """
        [*] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rtruediv__(self, other: Union[int, Integer]) -> Union[Integer, Fraction]:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rtruediv__(self, other: float) -> Float:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rpow__(self, other: Union[int, Integer]) -> Integer:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rpow__(self, other: float) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rmod__(self, other: Union[int, Integer]) -> Integer:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @overload
    def __rmod__(self, other: float) -> Float:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __rfloordiv__(self, other: Union[float, int]) -> Integer:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    def __eq__(self, term: term_) -> Union[SymbolicBool, Equation]:
        ...

    def get_powered_residual(
        self,
        power: int,
        mod: int,
        _range: Tuple[int, int] = (1, 5),
        section_title: str = "乗数の剰余",
        section_id: str = "get_powered_residual",
    ) -> Formula:
        ...


##### ./tmp/src/integer_utils.py #####


class IntegerUtils:
    """
    整数のutilクラス
    """

    @staticmethod
    def proof_having_rational_root_2_be_integer(
        proof: Proof,
        root: str = "m",
        numerator: str = "q",
        denominator: str = "l",
        section_title: str = "proof_having_rational_root_2_be_integer",
    ) -> bool:
        ...

    @staticmethod
    def proof_prime_exist_indefinitely(
        proof: Proof,
        section_title: str = "素数が無限にある証明",
        section_id: str = "proof_prime_exist_indefinitely",
    ) -> type["IntegerUtils"]:
        ...

    @staticmethod
    @overload
    def is_relatively_prime(
        proof: Proof,
        integer: Integer,
        other: Formula,
        relational_prime_pairs: List[
            Tuple[
                Union[int, Integer, Formula],
                Union[int, Integer, Formula],
            ]
        ] = [],
    ) -> Union[bool, None]:
        ...

    @staticmethod
    @overload
    def is_relatively_prime(
        proof: Proof,
        integer: Integer,
        other: Union[Integer, int],
        relational_prime_pairs: List[
            Tuple[
                Union[int, Integer, Formula],
                Union[int, Integer, Formula],
            ]
        ] = [],
    ) -> bool:
        ...

    @staticmethod
    def get_split_pair_in_to_product(
        proof: Proof,
        integer: Integer,
        uniqueness: Literal["combination", "order"] = "order",
        is_include_minus: bool = False,
    ) -> set[Tuple[int, int]]:
        ...

    @staticmethod
    @overload
    def truediv__(
        proof: Proof,
        integer: Integer,
        other: Union[Integer, int, Fraction],
    ) -> Union[Fraction, Integer]:
        ...

    @staticmethod
    @overload
    def truediv__(
        proof: Proof,
        integer: Integer,
        other: Formula,
    ) -> Formula:
        ...

    @staticmethod
    @overload
    def truediv__(
        proof: Proof,
        integer: Integer,
        other: Union[Float, float],
    ) -> Float:
        ...

    @staticmethod
    @overload
    def mod__(
        proof: Proof,
        integer: Integer,
        other: Union[Integer, int],
    ) -> Integer:
        ...

    @staticmethod
    @overload
    def mod__(
        proof: Proof,
        integer: Integer,
        other: Fraction,
    ) -> Union[Integer, Fraction]:
        ...

    @staticmethod
    @overload
    def mod__(
        proof: Proof,
        integer: Integer,
        other: Union[float, Float],
    ) -> Float:
        ...

    @staticmethod
    @overload
    def mod__(
        proof: Proof,
        integer: Integer,
        other: Formula,
    ) -> Formula:
        ...

    @staticmethod
    @overload
    def floordiv__(
        proof: Proof,
        integer: Integer,
        other: Union[Integer, int, Float, float, Fraction],
    ) -> Integer:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def floordiv__(
        proof: Proof,
        integer: Integer,
        other: Formula,
    ) -> Formula:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def pow__(
        proof: Proof,
        integer: Integer,
        other: Union[Integer, int],
    ) -> Integer:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def pow__(
        proof: Proof,
        integer: Integer,
        other: Union[Formula, float, Float, Fraction],
    ) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rtruediv__(
        proof: Proof,
        integer: Integer,
        other: Union[int, Integer],
    ) -> Union[Integer, Fraction]:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rtruediv__(proof: Proof, integer: Integer, other: float) -> Float:
        """
        [/] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rpow__(
        proof: Proof,
        integer: Integer,
        other: Union[int, Integer],
    ) -> Integer:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rpow__(proof: Proof, integer: Integer, other: float) -> Formula:
        """
        [**] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rmod__(
        proof: Proof,
        integer: Integer,
        other: Union[int, Integer],
    ) -> Integer:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    @overload
    def rmod__(proof: Proof, integer: Integer, other: float) -> Float:
        """
        [%] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    def rfloordiv__(
        proof: Proof, integer: Integer, other: Union[float, int]
    ) -> Integer:
        """
        [//] の中置演算子

        引数:
            other: 式
        結果:
            Formula
        """
        ...

    @staticmethod
    def get_powered_residual(
        proof: Proof,
        integer: Integer,
        power: int,
        mod: int,
        _range: Tuple[int, int] = (1, 5),
        section_title: str = "乗数の剰余",
        section_id: str = "get_powered_residual",
    ) -> Formula:
        ...

    @staticmethod
    @overload
    def adjust_function_right(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Union[Integer, int],
    ) -> Integer:
        ...

    @staticmethod
    @overload
    def adjust_function_right(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Fraction,
    ) -> Fraction:
        ...

    @staticmethod
    @overload
    def adjust_function_right(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Union[Float, float],
    ) -> Float:
        ...

    @staticmethod
    @overload
    def adjust_function_right(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Formula,
    ) -> Formula:
        ...

    @staticmethod
    @overload
    def adjust_function_left(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: Union[int, Integer],
    ) -> Integer:
        ...

    @staticmethod
    @overload
    def adjust_function_left(
        proof: Proof,
        integer: Integer,
        adjust_function: Callable[[variables, str, Union[str, int, float]], str],
        other: float,
    ) -> Float:
        ...


##### ./tmp/src/intersect.py #####


class Intersect:
    """
    交差を表すクラス
    """

    def __init__(self, proof: Proof, element: set[str]) -> None:
        ...

    def display(self) -> Intersect:
        ...


##### ./tmp/src/markdown_contents.py #####


class MarkdownContents:
    """
    Markdownのコンテンツを表すクラス
    """

    def __init__(self, contents: List[str]) -> None:
        ...

    def display(self, indent_depth: int = 0) -> MarkdownContents:
        ...


##### ./tmp/src/math_conditional.py #####


class MathConditional(Conditional):
    """
    数式で記述された命題を表すクラス
    """

    def __init__(
        self,
        sufficient_condition: SymbolCondition,
        necessary_condition: SymbolCondition,
        sufficient_condition_bool: bool = True,
        necessary_condition_bool: bool = True,
    ) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def text_necessary_condition(self) -> str:
        ...

    @property
    def text_sufficient_condition(self) -> str:
        ...

    @property
    def converse(self) -> MathConditional:
        ...

    @property
    def inverse(self) -> MathConditional:
        ...

    @property
    def contrapositive(self) -> MathConditional:
        ...

    @property
    def opposition(self) -> MathConditional:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...


##### ./tmp/src/math_markdown_sign.py #####


class MathMarkdownSign:
    """
    Markdownで使用する数学記号のクラス
    """

    @staticmethod
    def annotation() -> str:
        ...

    @staticmethod
    def because() -> str:
        ...

    @staticmethod
    def ellipsis() -> str:
        ...

    @staticmethod
    def full_space() -> str:
        ...

    @staticmethod
    def half_plus_space() -> str:
        ...

    @staticmethod
    def half_space() -> str:
        ...

    @staticmethod
    def therefore() -> str:
        ...


##### ./tmp/src/proof.py #####


class Proof:
    """
    証明における説明、変数を管理するクラス
    """

    def __init__(self) -> None:
        """
        コンストラクタ
        """
        ...

    @property
    def variables(self) -> variables:
        ...

    @property
    def section_titles(self) -> List[str]:
        """
        _summary_

        Returns:
            List[str]: _description_
        """
        ...

    def get_section(self, title: str) -> Section:
        """
        関数の説明タイトル

        関数についての説明文

        Args:
            引数の名前 (引数の型): 引数の説明
            引数の名前 (:obj:`引数の型`, optional): 引数の説明.

        Returns:
            戻り値の型: 戻り値の説明 (例 : True なら成功, False なら失敗.)

        Raises:
            例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )

        Yields:
            戻り値の型: 戻り値についての説明

        Examples:

            関数の使い方について記載

            >>> print_test ("test", "message")
                test message

        Note:
            注意事項などを記載
        """
        ...

    def make_temporary_variable(self) -> Formula:
        ...

    def make_temporary_section_id(self, base_id: str) -> str:
        ...

    @overload
    def get_variable(self, variable: Union[List[str], set[str]]) -> List[Formula]:
        ...

    @overload
    def get_variable(self, variable: str) -> Formula:
        ...

    def update_variables(self, variables: variables) -> Proof:
        ...

    @overload
    def make_variable(
        self,
        variables: str,
        variable_types: Union[variable_type_optional, variable_types_optional] = {},
    ) -> Formula:
        ...

    @overload
    def make_variable(
        self,
        variables: variables_list,
        variable_types: Union[variable_type_optional, variable_types_optional] = {},
    ) -> formulas:
        ...

    def make_variables(
        self,
        variables: str,
        variable_types: Union[variable_type_optional, variable_types_optional] = {},
    ) -> formulas:
        ...

    def register_variables(
        self,
        variables: List[str],
        variable_types: variable_types_optional = {},
    ) -> Proof:
        ...

    def make_section(self, title: str, id: str) -> Section:
        ...

    @overload
    def append_explain(self, content: explain, section: str = "") -> Proof:
        ...

    @overload
    def append_explain(
        self,
        content: relation_content,
        section: str = "",
        is_therefore_sign: bool = False,
        appendix: str = "",
        appendix_type: Literal["because", "annotate", "plain"] = "because",
    ) -> Proof:
        ...

    def insert_section(
        self,
        section: Union[Section, str],
        parent_section: Union[str, Section, None] = None,
    ) -> Proof:
        ...

    def display_explain(self, section: str = "") -> Proof:
        ...

    def is_variable(self, express: Union[Formula, str]) -> bool:
        ...


variables_list = List[str]
variables_set = set[str]
formulas = List[Formula]

##### ./tmp/src/py_utils.py #####

#


#

# default_range:


class PyUtils:
    @staticmethod
    def is_num(string: str) -> bool:
        ...

    @staticmethod
    def is_float(string: str) -> bool:
        ...

    @staticmethod
    def is_integer(string: str) -> bool:
        ...

    @staticmethod
    def is_fraction(string: str) -> bool:
        ...

    @staticmethod
    def get_random_name(n: int, lower_case: bool) -> str:
        ...

    @overload
    @staticmethod
    def get_all_combination(choices: List[List[int]]) -> List[List[int]]:
        ...

    @overload
    @staticmethod
    def get_all_combination(choices: List[List[float]]) -> List[List[float]]:
        ...

    @overload
    @staticmethod
    def get_all_combination(choices: List[List[str]]) -> List[List[str]]:
        ...

    @staticmethod
    def translate_range_from_dict_to_tuple(
        plot_ranges: plotRanges,
        alphabetic_axis_order: bool = True,
        variables: set[str] = set(),
    ) -> plotRange_2d:
        ...

    @staticmethod
    def translate_range_from_single_to_twin(
        plot_range: plotRange,
    ) -> plotRange_2d:
        ...

    @staticmethod
    def translate_range_to_plotRange_2d(
        plot_ranges: Union[
            None,
            plotRanges,
            plotRange,
            plotRange_2d,
        ],
        alphabetic_axis_order: bool = True,
        variables: set[str] = set(),
    ) -> plotRange_2d:
        ...

    @staticmethod
    def display_safety(contents: Union[str, Markdown, Math]) -> None:
        ...


##### ./tmp/src/relation_content.py #####


class RelationContent:
    """
    前後と関係のあるMarkdown contentクラス
    """

    def __init__(
        self,
        content: relation_content,
        is_therefore_sign: bool = False,
        appendix: str = "",
        appendix_type: Literal["because", "annotate", "plain"] = "because",
    ) -> None:
        ...

    @property
    def content(self) -> relation_content:
        ...

    @property
    def ascended_therefore_sign(self) -> bool:
        ...

    def display(
        self,
        indent_depth: int = 0,
        previous_content: Union[RelationContent, None] = None,
        omit_mode: Literal["off", "on", "auto"] = "auto",
    ) -> RelationContent:
        ...


##### ./tmp/src/section.py #####


class Section:
    """
    証明文の章にあたるクラス。

    引数:
        id(str): id
    """

    def __init__(self, proof: Proof, title: str, id: str) -> None:
        ...

    def make_sub_section(
        self, title: str, id: str, index: Union[int, None] = None
    ) -> Section:
        ...

    def __getitem__(self, index: int) -> explain:
        ...

    @overload
    def __setitem__(self, index: int, value: Section) -> Section:
        ...

    @overload
    def __setitem__(self, index: int, value: RelationContent) -> RelationContent:
        ...

    def __iter__(self) -> Generator[explain, None, None]:
        ...

    @overload
    def append(self, content: explain, is_therefore_sign: bool = False) -> Section:
        ...

    @overload
    def append(
        self,
        content: relation_content,
        is_therefore_sign: bool = False,
        appendix: str = "",
        appendix_type: Literal["because", "annotate", "plain"] = "because",
    ) -> Section:
        ...

    def insert_section(self, section: Union[Section, str]) -> Section:
        ...

    def display(self, indent_depth: int = 0) -> Section:
        ...


##### ./tmp/src/symbol_condition_utils.py #####


class SymbolConditionUtils:
    """
    数式の論理結合演算子操作をまとめたクラス

    Attributes:
        variables (set[str]): 条件中で用いられる変数
        text (str): 条件中で用いられる変数
    """

    @staticmethod
    def invert__(proof: Proof, condition_left: SymbolCondition) -> symbol_condition:
        ...

    @staticmethod
    def and__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> symbol_condition:
        """
        論理和の中置演算子

        Args:
            other : 演算対象
        """
        ...

    @staticmethod
    def or__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> symbol_condition:
        ...

    @staticmethod
    def eq__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def ne__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def lt__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def le__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def gt__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def ge__(
        proof: Proof,
        condition_left: SymbolCondition,
        condition_right: Union[bool, symbol_condition],
    ) -> SymbolicBool:
        ...

    @staticmethod
    def format__(condition: SymbolCondition) -> str:
        ...

    @staticmethod
    def lshift__(
        condition_left: SymbolCondition,
        condition_right: SymbolCondition,
    ) -> MathConditional:
        ...

    @staticmethod
    def display(
        proof: Proof, condition: SymbolCondition
    ) -> type["SymbolConditionUtils"]:
        ...

    @staticmethod
    def make_figure(
        proof: Proof,
        condition: SymbolCondition,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    @staticmethod
    def plot(
        proof: Proof,
        condition: SymbolCondition,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> type["SymbolConditionUtils"]:
        ...


##### ./tmp/src/symbolic_bool.py #####


class SymbolicBool:
    """
    python nativeのboolではなく、designed math module(数式処理モジュール)で用いるbool
    """

    def __init__(self, proof: Proof, bool: bool) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    def display(self) -> SymbolicBool:
        ...

    @property
    def text(self) -> str:
        ...

    def __lt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __le__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __gt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ge__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __lshift__(self, other: SymbolCondition) -> MathConditional:
        ...

    def can_cast(self, type: type_from_term_inequation) -> SymbolicBool:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> SymbolCondition:
        ...

    @property
    def native_bool(self) -> bool:
        ...

    def __bool__(self) -> bool:
        ...

    def __invert__(self) -> SymbolicBool:
        ...

    def __eq__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ne__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    @overload
    def __and__(self, other: Union[bool, SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __and__(self, other: symbol_range) -> symbol_condition:
        ...

    @overload
    def __or__(self, other: Union[bool, SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __or__(self, other: symbol_range) -> symbol_condition:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[DefineEquation]) -> DefineEquation:
        ...

    @overload
    def __rshift__(self, type: type[ExplainEquation]) -> ExplainEquation:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...


##### ./tmp/src/table.py #####


class Table:
    """
    markdown表示可能な表クラス
    """

    def __init__(self, data: table_data) -> None:
        ...

    @property
    def data(self) -> table_data:
        ...

    def set_index(self, columnName: str) -> Table:
        ...

    def remove_display_limit(self, direction: Literal["row", "column"]) -> Table:
        ...

    def add_row(self) -> Table:
        ...

    def add_column(
        self, columnName: Union[str, int, float], body: List[Union[str, int, float]]
    ) -> Table:
        ...

    def display(self) -> Table:
        ...


##### ./tmp/src/term_utils.py #####


class TermUtils:
    """
    designed math(数式処理)モジュールでの項に関するユーティリティクラス
    """

    @staticmethod
    def get_degree(proof: Proof, term: Term) -> int:
        """
        式の最大の次数

        注意:
            整数多項式以外は、正しい結果を返さない。
            例）(x**2 + (1/x)**5) -> 5
        """
        ...

    @staticmethod
    def check_be_integer(proof: Proof, term: Term) -> Union[bool, None]:
        ...

    @staticmethod
    def evaluate_equality(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Equation]:
        ...

    @staticmethod
    def evaluate_not_equality(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Unequation]:
        ...

    @staticmethod
    def evaluate_less_than_relation(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Inequation]:
        ...

    @staticmethod
    def evaluate_less_or_equality(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Inequation]:
        ...

    @staticmethod
    def evaluate_greater_than_relation(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Inequation]:
        ...

    @staticmethod
    def evaluate_greater_or_equality(
        proof: Proof,
        term_left: Term,
        term_right: term_,
    ) -> Union[SymbolicBool, Inequation]:
        ...

    @staticmethod
    def get_stringify_text(term: Term) -> str:
        ...

    @staticmethod
    def get_formatted_text(term: Term) -> str:
        ...

    @staticmethod
    def display(proof: Proof, term: Term) -> type["TermUtils"]:
        ...


##### ./tmp/src/text_conditional.py #####


class TextConditional(Conditional):
    """
    一般言語による命題クラス
    """

    def __init__(
        self,
        sufficient_condition: str,
        necessary_condition: str,
        sufficient_condition_bool: bool = True,
        necessary_condition_bool: bool = True,
    ) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    @property
    def text_necessary_condition(self) -> str:
        ...

    @property
    def text_sufficient_condition(self) -> str:
        ...

    @property
    def text_converse(self) -> str:
        ...

    @property
    def text_inverse(self) -> str:
        ...

    @property
    def text_contrapositive(self) -> str:
        ...

    @property
    def text_opposition(self) -> str:
        ...

    @property
    def converse(self) -> TextConditional:
        ...

    @property
    def inverse(self) -> TextConditional:
        ...

    @property
    def contrapositive(self) -> TextConditional:
        ...

    @property
    def opposition(self) -> TextConditional:
        ...


##### ./tmp/src/unequation.py #####


class Unequation:
    """
    非等号クラス（右辺、左辺が等しくないことを表現するクラス)。
    方程式、不等式からのアナロジーで非等式と言いたいが、そんな日本語はないらしい。
    """

    def __init__(self, proof: Proof, equation: Union[str, express_term]) -> None:
        ...

    @property
    def text(self) -> str:
        ...

    def __invert__(self) -> symbol_condition:
        ...

    def __and__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        """
        論理和の中置演算子

        Args:
            other : 演算対象
        """
        ...

    def __or__(self, other: Union[bool, symbol_condition]) -> symbol_condition:
        ...

    def __eq__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ne__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __lt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __le__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __gt__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __ge__(self, other: Union[bool, symbol_condition]) -> SymbolicBool:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __lshift__(self, other: SymbolCondition) -> MathConditional:
        ...

    def can_cast(self, type: type_from_term_inequation) -> SymbolicBool:
        ...

    def make_figure(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> Figure:
        ...

    def plot(
        self,
        plot_ranges: Union[
            plotRange,
            plotRanges,
            plotRange_2d,
            None,
        ],
        alphabetic_axis_order: bool = True,
        title: str = "",
    ) -> SymbolCondition:
        ...

    @property
    def formulas(self) -> Tuple[Formula, Formula]:
        ...

    @property
    def text_forDisplay(self) -> str:
        ...

    @property
    def text_for_input(self) -> str:
        ...

    @property
    def variables(self) -> set[str]:
        """
        式の変数
        """
        ...

    @property
    def evaluated(self) -> Union[Unequation, SymbolicBool]:
        ...

    @overload
    def __rshift__(self, type: type[SymbolicBool]) -> SymbolicBool:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v1]) -> Inequation_v1:
        ...

    @overload
    def __rshift__(self, type: type[Inequation_v2]) -> Inequation_v2:
        ...

    @overload
    def __rshift__(self, type: type[Inequation]) -> Inequation:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v1]) -> ComplexCondition_v1:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition_v2]) -> ComplexCondition_v2:
        ...

    @overload
    def __rshift__(self, type: type[ComplexCondition]) -> ComplexCondition:
        ...

    @overload
    def __rshift__(self, type: type[Equation]) -> Equation:
        ...

    @overload
    def __rshift__(self, type: type[Unequation]) -> Unequation:
        ...

    def castable_type(self) -> List[type_from_term_inequation]:
        ...

    def substitute(
        self,
        conditions: Union[
            Dict[str, float],
            Dict[str, int],
            Dict[str, Term],
            Equation,
            Equations,
        ],
        side: Union[Literal["left", "right"], None] = None,
    ) -> Unequation:
        ...

    def display(self, is_raw: bool = True) -> Unequation:
        ...

    def is_identity(self) -> bool:
        ...

    def factorize(self) -> Unequation:
        ...


##### ./tmp/src/utils.py #####


class Utils:
    """
    designed math モジュールでのutilityクラス
    """

    @staticmethod
    def display(contents: Union[str, Markdown]) -> None:
        ...

    @staticmethod
    def getPrimes(range: Tuple[int, int]) -> List[int]:
        ...

    @staticmethod
    @overload
    def euclideanAlgorithm(
        proof: Proof, terms: Tuple[int, int], section_title: str
    ) -> Tuple[int, int]:
        ...

    @staticmethod
    @overload
    def euclideanAlgorithm(
        proof: Proof, terms: Tuple[str, str], section_title: str
    ) -> Tuple[str, str]:
        ...

    @staticmethod
    def cast(
        proof: Proof, type: term_type, text: str
    ) -> Union[Integer, Float, Fraction, Formula,]:
        ...

    @staticmethod
    def can_cast(type: term_type, text: str) -> bool:
        ...

    @staticmethod
    def get_called_location() -> int:
        """
        関数の呼び出し元の行番号を取得
        注意:
            !呼び出し元の上位行がすべて空の場合、常に1を返してしまうbugありTODO:修正!

        結果:
            呼び出し元の行
        """
        ...

    @staticmethod
    def display_row_express(proof: Proof, express: str) -> None:
        """
        式を評価せずに表示する
        要改修:
            ()が評価されて消えてしまう。
            x/xは評価されて1になってしまう。（変数宣言する必要あり）
        """
        ...

    @staticmethod
    def condition_logical_or(
        proof: Proof,
        conditions: Tuple[symbol_condition, symbol_condition],
    ) -> symbol_condition:
        ...

    @staticmethod
    def condition_logical_and(
        proof: Proof,
        conditions: Tuple[symbol_condition, symbol_condition],
    ) -> symbol_condition:
        ...


##### ./tmp/src/variable_handling.py #####


class VariableHandling:
    """
    designed math（数式処理）モジュールの変数をハンドリングするクラス
    """

    @staticmethod
    def create_variables_symbol(
        existed_variables: Dict[str, variable_symbol],
        variables: List[str],
        variable_types: variable_types_optional = {},
    ) -> Dict[str, variable_symbol]:
        ...


##### ./tmp/src/vector.py #####


class Vector:
    """
    designed math(数式処理モジュール)のベクトルクラス
    """

    def __init__(self, proof: Proof, elements: List[term_instance]) -> None:
        ...

    @property
    def variables(self) -> set[str]:
        ...

    @property
    def latex(self) -> str:
        ...

    def display(self) -> None:
        ...

    def append(self, element: term_instance) -> Vector:
        ...

    def __add__(self, other: Vector) -> Vector:
        """
        [+] の中置演算子

        引数:
            other: Vector
        結果:
            Vector
        """
        ...

    def __sub__(self, other: Vector) -> Vector:
        """
        [-] の中置演算子

        引数:
            other: Vector
        結果:
            Vector
        """
        ...

    def __neg__(self) -> Vector:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...

    def __getitem__(self, index: int) -> term_instance:
        ...

    def __iter__(self) -> Generator[term_instance, None, None]:
        ...

    def __len__(self) -> int:
        ...

    def __eq__(self, other: Vector) -> bool:
        ...


class FormulaVector(Vector):
    def __init__(self, proof: Proof, elements: List[Formula]) -> None:
        ...

    def append(self, element: Formula) -> FormulaVector:
        ...

    def __getitem__(self, index: int) -> Formula:
        ...

    def __iter__(self) -> Generator[term_instance, None, None]:
        ...


class IntegerPair(Vector):
    def __init__(
        self,
        proof: Proof,
        pair: integer_pair_input,
        sum: Union[integer_candidate_input, None] = None,
        product: Union[integer_candidate_input, None] = None,
    ) -> None:
        ...

    @property
    def elements(self) -> integer_pair:
        ...

    @property
    def sum(self) -> integer_candidate:
        ...

    @property
    def product(self) -> integer_candidate:
        ...

    def __getitem__(self, index: int) -> Union[Formula, Integer]:
        ...


class NaturalPair(IntegerPair):
    def __init__(
        self,
        proof: Proof,
        pair: integer_pair_input,
        sum: Union[integer_candidate_input, None] = None,
        product: Union[integer_candidate_input, None] = None,
        gcd: Union[integer_candidate_input, None] = None,
        lcm: Union[integer_candidate_input, None] = None,
        relational_prime_pairs: List[
            Tuple[integer_candidate_input, integer_candidate_input]
        ] = [],
    ) -> None:
        ...

    @property
    def gcd(self) -> Union[NaturalPair, integer_candidate]:
        ...

    @property
    def gcd_history(self) -> Section:
        ...

    @property
    def lcm(self) -> Union[integer_candidate, None]:
        ...

    @property
    def product_relation_equation(self) -> Equation:
        ...

    @property
    def summation_relation_equation(self) -> Union[Equation, None]:
        ...

    def display_gcd_history(self) -> NaturalPair:
        ...

    @overload
    def identify_from_condition(
        self,
        sum: int,
        lcm: None,
        gcd: int,
        section_title: str = "同定する_条件から",
        section_id: str = "identify_from_condition",
    ) -> VectorSolutions:
        ...

    @overload
    def identify_from_condition(
        self,
        sum: int,
        lcm: int,
        gcd: None = None,
        section_title: str = "同定する_条件から",
        section_id: str = "identify_from_condition",
    ) -> VectorSolutions:
        ...


##### ./tmp/src/vector_solutions.py #####


class VectorSolutions:
    """
    ベクトル方程式のうち、各変数について説かれた形式のクラス
    """

    def __init__(
        self,
        proof: Proof,
        equations: Union[List[VectorEquation], List[Solutions]],
    ) -> None:
        ...

    @property
    def equations(self) -> List[VectorEquation]:
        ...

    def add(
        self, vector_equations: Union[List[VectorEquation], VectorSolutions]
    ) -> VectorSolutions:
        ...

    def append(self, vector_equation: VectorEquation) -> VectorSolutions:
        ...

    def __getitem__(self, index: int) -> VectorEquation:
        ...

    def __iter__(self) -> Generator[VectorEquation, None, None]:
        ...

    def __format__(self, __format_spec: str) -> str:
        ...


##### ./tmp/src/ven_diagram.py #####


class VenDiagram:
    """
    ベン図クラス。。
    """

    def __init__(self, data: List[vennData]) -> None:
        ...

    def display(self) -> VenDiagram:
        ...


##### ./tmp/src/ven_diagram_reservation.py #####


class VenDiagramReservation:
    """
    ベン図登録クラス。
    図形クラスはインスタンスが定義された断面でレンダリングされ、出力の並びが狂うため、表示を先送りするためのクラス。
    """

    def __init__(self, data: List[vennData]) -> None:
        ...

    def display(self) -> VenDiagramReservation:
        ...


##### ./tmp/src/define_type.py #####

SymbolCondition = Union[
    Equation, Inequation, Unequation, ComplexCondition, SymbolicBool
]
Term = Union[Formula, Float, Integer, Fraction]


class subtract_prime_result(TypedDict):
    term: Formula
    signInteger: Literal[1, -1]


class Modee(TypedDict):
    residual: int
    power: int


markdown_str = str
integer_candidate = Union[Integer, Formula]
integer_candidate_input = Union[int, integer_candidate]
integer_pair_input = Tuple[integer_candidate_input, integer_candidate_input]
integer_pair = Tuple[integer_candidate, integer_candidate]
condition_symbol = Literal["True", "False"]
#

equation_symbol_ = Literal["="]

inequality_relation = Literal["<", "<=", ">", ">="]
inequation_symbol = Literal["<", "<=", ">", ">="]
term_type = Union[type[Integer], type[Float], type[Fraction], type[Formula]]
table_data = Dict[str, List[Union[str, int, float]]]
unequation_symbol = Literal["!="]

plotRange_ = Tuple[
    Tuple[Union[int, float], Union[int, float]],
    Tuple[Union[int, float], Union[int, float]],
]
symbol_relation_type = Literal[
    operator_symbol,
    number_symbol,
    condition_symbol,
    equation_symbol_,
    inequation_symbol,
    unequation_symbol,
]
symbol_type = Literal[symbol_relation_type, "symbol", condition_symbol]
type_from_term_inequation = Union[
    type[SymbolicBool],
    type[Inequation],
    type[Inequation_v1],
    type[Inequation_v2],
    type[Equation],
    type[Unequation],
    type[ComplexCondition],
    type[ComplexCondition_v1],
    type[ComplexCondition_v2],
]

single_condition = Union[
    Equation, Unequation, Inequation, Inequation_v1, Inequation_v2, SymbolicBool
]
symbol_range = Union[
    Equation,
    Unequation,
    Inequation,
    Inequation_v1,
    Inequation_v2,
    ComplexCondition,
    ComplexCondition_v1,
    ComplexCondition_v2,
]
symbol_condition = Union[symbol_range, SymbolicBool]


class squared_result(TypedDict):
    square: Formula
    correction_term: Formula


class add_and_subtract_products_equation(TypedDict):
    left_plus_term: Formula
    left_minus_term: Formula
    right_constant_term: Union[Integer, Fraction]


class euclidean_output_each_process(TypedDict):
    result: NaturalPair
    explain: Section


class euclidean_output(TypedDict):
    result: Union[NaturalPair, integer_candidate]
    explain: Section


class variable_type_optional(TypedDict, total=False):
    commutative: Literal[True]
    complex: Literal[True]
    composite: Literal[True]
    even: Literal[True]
    extended_negative: Literal[True]
    extended_nonnegative: Literal[True]
    extended_nonpositive: Literal[True]
    extended_nonzero: Literal[True]
    extended_positive: Literal[True]
    extended_real: Literal[True]
    finite: Literal[True]
    imaginary: Literal[True]
    infinite: Literal[True]
    integer: Literal[True]
    irrational: Literal[True]
    negative: Literal[True]
    noninteger: Literal[True]
    nonnegative: Literal[True]
    nonpositive: Literal[True]
    nonzero: Literal[True]
    odd: Literal[True]
    positive: Literal[True]
    prime: Literal[True]
    rational: Literal[True]
    real: Literal[True]
    zero: Literal[True]


# Dependent type
variable_types_optional = Dict[str, variable_type_optional]
explain = Union[
    Section,
    RelationContent,
    str,
    MarkdownContents,
    Table,
    FigureReservation,
    VenDiagramReservation,
]


class common_initialize_result(TypedDict):
    proof: Proof
    ast: astElement
    variables: set[str]


class equation_symbol(TypedDict):
    formula_left: variable_symbol
    formula_right: variable_symbol


class checked_variable(TypedDict):
    existed_variables: variables
    added_variables: set[str]


class condition(TypedDict):
    times: int
    mod: List[int]


term_instance = Union[float, int, Integer, Float, Fraction, Formula]
conditions_float = Dict[str, float]
conditions_int = Dict[str, int]
conditions_str = Dict[str, str]
conditions_term = Dict[str, Term]
conditions_fraction = Dict[str, NativeFraction]
conditions_native = Union[conditions_float, conditions_int, conditions_str]
term_ = Union[Term, float, int, NativeFraction]
term = Union[Term, str, float, int, NativeFraction]


class Position_only_x(TypedDict, total=True):
    x: Union[int, float, str]


class Position_only_y(TypedDict, total=True):
    y: Union[int, float, str]


class Position_only(Position_only_x, Position_only_y):
    ...


class Annotation(TypedDict, total=False):
    annotation: str


class Position(Position_only, Annotation):
    ...


class Position_x(Position_only_x, Annotation):
    ...


class Positions_only_x(TypedDict, total=True):
    x: Union[List[int], List[float], List[str]]


class Positions_only_y(TypedDict, total=True):
    y: List[Union[int, float, str]]


class Positions_only(Positions_only_x, Positions_only_y):
    ...


class Annotations(TypedDict, total=False):
    annotation: List[str]


class Positions_list(Positions_only, Annotations):
    ...


class Positions_list_x(Positions_only_x, Annotations):
    ...


class result_of_factorized_and_split(TypedDict):
    inequations: Union[
        Tuple[Tuple[Inequation, Inequation], Tuple[Inequation, Inequation]], None
    ]
    relation_index: Literal[0, 1, 2, 3]


#


#

relation_content = Union[
    symbol_condition,
    Term,
    MathConditional,
    Solutions,
    VectorEquation,
    VectorSolutions,
    Vector,
]

express_term = Tuple[term, term]
