import dataclasses

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


@dataclasses.dataclass(slots=True)
class Function(BaseAliased, FunctionProtocol):
    name: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f"{self.name}()"


@dataclasses.dataclass(slots=True)
class Fn2Args(Function):
    arg1: str | ExprProtocol
    arg2: str | ExprProtocol

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f"{self.name}({to_col_or_expr(self.arg1, dialect)}, {to_col_or_expr(self.arg2, dialect)})"


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass(slots=True, kw_only=True)
class FnCallableFactory:
    name: str = ''


@dataclasses.dataclass(slots=True)
class SeparatedArgsFnFactory(FnCallableFactory):
    separator: str = ', '

    def __call__(self, *args: int | float | str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=args, separator=self.separator)


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass
class BaseOverClauseFunction(Function, AggFunctionProtocol):
    _window: str = ''
    _partition_by: list[str | FunctionProtocol] = dataclasses.field(default_factory=list)
    _order_by: list[str | list[str]] = dataclasses.field(default_factory=list)
    _frame_mode: FrameModeProtocol = None
    _filter: tuple[LogicalOperatorProtocol | PredicateProtocol, ...] = dataclasses.field(default_factory=tuple)

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


@dataclasses.dataclass
class OverClauseFunction(BaseOverClauseFunction, OneArgDistinctFn):
    pass


@dataclasses.dataclass
class OverClause2ArgFunction(BaseOverClauseFunction, Fn2Args):
    pass


@dataclasses.dataclass(slots=True)
class OneArgDistinctFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return OneArgDistinctFn(self.name, column, distinct)


@dataclasses.dataclass(slots=True)
class OneArgDistinctWindowFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> AggFunctionProtocol:
        return OverClauseFunction(self.name, column, distinct=distinct)


@dataclasses.dataclass(slots=True)
class OneArgWindowFactory(FnCallableFactory):
    def __call__(self, column: str) -> AggFunctionProtocol:
        return OverClauseFunction(self.name, column)


@dataclasses.dataclass(slots=True)
class TwoArgWindowFactory(FnCallableFactory):
    def __call__(self, arg1: str | ExprProtocol, arg2: str | ExprProtocol) -> AggFunctionProtocol:
        return OverClause2ArgFunction(self.name, arg1, arg2)


@dataclasses.dataclass(slots=True)
class StrArgFactory(FnCallableFactory):
    def __call__(self, value: str | ExprProtocol) -> FunctionProtocol:
        return SeparatedArgsFn(self.name, fn_items=(value,))


@dataclasses.dataclass(slots=True)
class ColStrIntArgFactory(FnCallableFactory):
    def __call__(
        self,
        arg1: str | int | ExprProtocol,
    ) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                val(arg1) if isinstance(arg1, int) else arg1,
            ),
        )


@dataclasses.dataclass(slots=True)
class FirstCol1StrArgFactory(FnCallableFactory):
    separator: str = ', '
    def __call__(
        self,
        col_name: str | ExprProtocol,
        arg1: str | ExprProtocol,
    ) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                col_name,
                arg1 if isinstance(arg1, ExprProtocol) else val(arg1),
            ),
            self.separator,
        )


@dataclasses.dataclass(slots=True)
class FirstCol1ValFactory(FnCallableFactory):
    separator: str = ', '
    def __call__(
        self,
        col_name: str | ExprProtocol,
        value: str | float | int | ExprProtocol,
    ) -> FunctionProtocol:
        return SeparatedArgsFn(
            self.name,
            (
                col_name,
                value if isinstance(value, ExprProtocol) else val(value),
            ),
            self.separator,
        )


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass(slots=True)
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


@dataclasses.dataclass(slots=True)
class CastFn(Function):
    value: str | ExprProtocol
    cast_type: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        value = to_col_or_expr(self.value, dialect)
        return f"{self.name}({value} AS {self.cast_type})"


@dataclasses.dataclass(slots=True)
class CastFactory(FnCallableFactory):
    name = 'CAST'
    def __call__(self, value: str | ExprProtocol, cast_type: str) -> FunctionProtocol:
        return CastFn('CAST', value, cast_type)


@dataclasses.dataclass(slots=True)
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
