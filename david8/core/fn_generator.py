import dataclasses

from ..expressions import val
from ..protocols.dialect import DialectProtocol
from ..protocols.sql import ExprProtocol, FrameModeProtocol, FunctionProtocol, WindowSpecProtocol
from .arg_convertors import to_col_or_expr
from .base_aliased import BaseAliased


@dataclasses.dataclass(slots=True)
class Function(BaseAliased, FunctionProtocol):
    name: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f"{self.name}()"


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
class _OneArgDistinctFn(Function):
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
class _WindowSpecFunction(_OneArgDistinctFn, WindowSpecProtocol):
    _window: str = ''
    _partition_by: list[str | FunctionProtocol] = dataclasses.field(default_factory=list)
    _order_by: list[str | list[str]] = dataclasses.field(default_factory=list)
    _frame_mode: FrameModeProtocol = None

    def over(
        self,
        partition_by: list[str | FunctionProtocol] = None,
        order_by: list[str | tuple[str, int]] = None,
        window: str = '',
        frame_mode: FrameModeProtocol = None,
    ) -> 'WindowSpecProtocol':
        self._window = window
        self._frame_mode = frame_mode
        self._partition_by = partition_by or []
        self._order_by = order_by or []

        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        sql = super()._get_sql(dialect)
        if not any([self._window, self._partition_by, self._order_by]):
            return sql

        parts = ()
        if self._partition_by:
            parts += ('PARTITION BY',)
            for part in self._partition_by:
                if isinstance(part, str):
                    parts += (dialect.quote_ident(part),)
                elif isinstance(part, FunctionProtocol):
                    parts += (part.get_sql(dialect),)

        if self._order_by:
            order_by_items = ()
            for part in self._order_by:
                if isinstance(part, str):
                    order_by_items += (dialect.quote_ident(part), )
                if isinstance(part, list) and len(part) == 1:
                    if isinstance(part[0], str):
                        order_by_items += (f'{dialect.quote_ident(part[0])} DESC', )

            parts += ('ORDER BY', ', '.join(order_by_items))

        if self._frame_mode:
            parts += (self._frame_mode.get_sql(dialect),)

        window_name = f'{self._window} ' if self._window else ''
        return f"{sql} OVER ({window_name}{' '.join(parts)})"


@dataclasses.dataclass(slots=True)
class OneArgDistinctFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return _OneArgDistinctFn(self.name, column, distinct)


@dataclasses.dataclass(slots=True)
class OneArgDistinctWindowFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> _WindowSpecFunction:
        return _WindowSpecFunction(self.name, column, distinct)


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
class _CastFn(Function):
    value: str | ExprProtocol
    cast_type: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        value = to_col_or_expr(self.value, dialect)
        return f"{self.name}({value} AS {self.cast_type})"


@dataclasses.dataclass(slots=True)
class CastFactory(FnCallableFactory):
    name = 'CAST'
    def __call__(self, value: str | ExprProtocol, cast_type: str) -> FunctionProtocol:
        return _CastFn('CAST', value, cast_type)


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
