from dataclasses import dataclass, field

from ..expressions import val
from ..protocols.dialect import DialectProtocol
from ..protocols.sql import (
    AggFunctionProtocol,
    DescProtocol,
    ExprProtocol,
    FrameModeProtocol,
    FunctionProtocol,
    LogicalOperatorProtocol,
    PredicateProtocol,
)
from .arg_convertors import to_col_or_expr
from .base_aliased import BaseAliased
from .base_frames import BaseOverClause


@dataclass(slots=True)
class Function(BaseAliased, FunctionProtocol):
    name: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f"{self.name}()"


@dataclass(slots=True)
class SeparatedArgsFn(Function):
    fn_items: tuple[str | int | float | ExprProtocol, ...]
    separator: str = ', '
    numbers_as_str: bool = True

    def _get_sql(self, dialect: DialectProtocol) -> str:
        items = ()
        for item in self.fn_items:
            if isinstance(item, str):
                items += (dialect.quote_ident(item),)
                continue
            elif isinstance(item, (int, float)):
                items += (f"'{item}'",) if self.numbers_as_str else (f'{item}',)
                continue

            items += (item.get_sql(dialect),)

        return f'{self.name}({self.separator.join(items)})'


@dataclass(slots=True, kw_only=True)
class FnCallableFactory:
    name: str = ''


@dataclass(slots=True)
class SeparatedArgsFnFactory(FnCallableFactory):
    separator: str = ', '

    def __call__(self, *args: int | float | str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=args, separator=self.separator)


@dataclass(slots=True)
class OneArgDistinctFn(Function):
    """
    SUM(DISTINCT price)
    AVG(DISTINCT quantity)
    STDDEV(DISTINCT score)
    """
    column: str = ''
    distinct: bool = False

    def _get_sql(self, dialect: DialectProtocol) -> str:
        name = f"{self.name}({'DISTINCT ' if self.distinct else ''}"
        return f"{name}{dialect.quote_ident(self.column)})"


@dataclass
class BaseOverClauseFunction(Function, AggFunctionProtocol):
    _window: str = ''
    _partition_by: list[str | FunctionProtocol] = field(default_factory=list)
    _order_by: list[str | list[str]] = field(default_factory=list)
    _frame_mode: FrameModeProtocol = None
    _filter: tuple[LogicalOperatorProtocol | PredicateProtocol, ...] = field(default_factory=tuple)

    def over(
        self,
        partition_by: list[str | FunctionProtocol] = None,
        order_by: list[str | DescProtocol] = None,
        window: str = '',
        frame_mode: FrameModeProtocol = None,
    ) -> 'AggFunctionProtocol':
        self._window = window
        self._frame_mode = frame_mode
        self._partition_by = partition_by or []
        self._order_by = order_by or []

        return self

    def filter(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'AggFunctionProtocol':
        self._filter = args
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        sql = super()._get_sql(dialect)
        spec_sql = BaseOverClause(
            _window=self._window,
            _partition_by=self._partition_by,
            _order_by=self._order_by,
            _frame_mode=self._frame_mode,
        ).get_sql(dialect)

        filter_sql = ''
        if self._filter:
            conditions = ', '.join(f.get_sql(dialect) for f in self._filter)
            filter_sql = f' FILTER ({conditions})'

        spec_sql = f'{filter_sql} OVER {spec_sql}' if spec_sql else ''
        return f"{sql}{spec_sql}"


@dataclass
class OverClauseFunction(BaseOverClauseFunction, OneArgDistinctFn):
    pass


@dataclass
class OverClause2ArgFunction(BaseOverClauseFunction, SeparatedArgsFn):
    pass


@dataclass(slots=True)
class ZeroArgAggFactory(FnCallableFactory):
    def __call__(self) -> AggFunctionProtocol:
        return OverClauseFunction(self.name, distinct=False)


@dataclass(slots=True)
class OneArgDistinctFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return OneArgDistinctFn(self.name, column, distinct)


@dataclass(slots=True)
class OneArgDistinctWindowFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> AggFunctionProtocol:
        return OverClauseFunction(self.name, column, distinct=distinct)


@dataclass(slots=True)
class OneArgWindowFactory(FnCallableFactory):
    def __call__(self, column: str) -> AggFunctionProtocol:
        return OverClauseFunction(self.name, column)


@dataclass(slots=True)
class TwoArgWindowFactory(FnCallableFactory):
    def __call__(self, arg1: str | ExprProtocol, arg2: str | ExprProtocol) -> AggFunctionProtocol:
        return OverClause2ArgFunction(name=self.name, fn_items=(arg1, arg2))


@dataclass(slots=True)
class TwoArgIntWindowFactory(FnCallableFactory):
    def __call__(self, arg1: str | ExprProtocol, arg2: int | ExprProtocol) -> AggFunctionProtocol:
        return OverClause2ArgFunction(name=self.name, fn_items=(arg1, arg2), numbers_as_str=False)


@dataclass(slots=True)
class StrArgFactory(FnCallableFactory):
    def __call__(self, value: str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=(value,))


@dataclass(slots=True)
class ColStrIntArgFactory(FnCallableFactory):
    def __call__(self, arg1: str | int | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                val(arg1) if isinstance(arg1, int) else arg1,
            ),
        )


@dataclass(slots=True)
class FirstCol1StrArgFactory(FnCallableFactory):
    separator: str = ', '
    def __call__(self, col_name: str | ExprProtocol, arg1: str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                col_name,
                arg1 if isinstance(arg1, ExprProtocol) else val(arg1),
            ),
            self.separator,
        )


@dataclass(slots=True)
class FirstCol1ValFactory(FnCallableFactory):
    separator: str = ', '
    def __call__(self, col_name: str | ExprProtocol, value: str | float | int | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                col_name,
                value if isinstance(value, ExprProtocol) else val(value),
            ),
            self.separator,
        )


@dataclass(slots=True)
class FirstCol2StrArgFactory(FnCallableFactory):
    def __call__(
        self,
        col_name: str | ExprProtocol,
        arg1: str | ExprProtocol,
        arg2: str | ExprProtocol,
    ) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=(
            col_name,
            arg1 if isinstance(arg1, ExprProtocol) else val(arg1),
            arg2 if isinstance(arg2, ExprProtocol) else val(arg2),
        ))


@dataclass(slots=True)
class FirstCol2IntArgFactory(FnCallableFactory):
    def __call__(
        self,
        col_name: str | ExprProtocol,
        arg1: int | ExprProtocol,
        arg2: int | ExprProtocol,
    ) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=(
            col_name,
            arg1 if isinstance(arg1, ExprProtocol) else val(arg1),
            arg2 if isinstance(arg2, ExprProtocol) else val(arg2),
        ))


@dataclass(slots=True)
class CastFn(Function):
    value: str | ExprProtocol
    cast_type: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        value = to_col_or_expr(self.value, dialect)
        return f"{self.name}({value} AS {self.cast_type})"


@dataclass(slots=True)
class CastFactory(FnCallableFactory):
    name = 'CAST'
    def __call__(self, value: str | ExprProtocol, cast_type: str) -> FunctionProtocol:
        return CastFn('CAST', value, cast_type)


@dataclass(slots=True)
class StrIntArgsFactory(FnCallableFactory):
    def __call__(self, *args: str | int | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=args, numbers_as_str=False)


@dataclass(slots=True)
class GenerateSeriesFactory(FnCallableFactory):
    def __call__(
        self,
        start: int | float,
        stop: int | float = None,
        step: int | float = None,
    ) -> FunctionProtocol:
        args = (val(i) for i in (start, stop, step, ) if i is not None)
        return SeparatedArgsFn(
            separator=', ',
            fn_items=tuple(args),
            name='generate_series',
            numbers_as_str=False,
        )
