from dataclasses import dataclass
from dataclasses import field as _field
from typing import ClassVar

from .core.base_aliased import BaseAliased as _BaseAliased
from .core.base_aliased import BaseCase as _BaseCase
from .core.base_aliased import BaseInterval as _BaseInterval
from .core.base_aliased import Column as _Column
from .core.base_aliased import create_parameter as _create_parameter
from .core.base_aliased import create_value
from .core.base_expressions import BaseDesc as _BaseDesc
from .core.base_expressions import BaseDistinct
from .core.base_expressions import FullTableName as _FullTableName
from .core.base_frames import BaseOverClause as _BaseOverClause
from .protocols.dialect import DialectProtocol
from .protocols.sql import (
    AliasedProtocol,
    ColumnProtocol,
    DescProtocol,
    ExprProtocol,
    FrameModeProtocol,
    FunctionProtocol,
    IntervalProtocol,
    LogicalOperatorProtocol,
    ParameterProtocol,
    PredicateProtocol,
    SourceProtocol,
    ValueProtocol,
    WindowSpecProtocol,
)


def val(value: str | int | float) -> ValueProtocol:
    return create_value(value)

def col(name: str) -> ColumnProtocol:
    return _Column(name)

def param(value: str | int | float, fixed_name: bool = False) -> ParameterProtocol:
    return _create_parameter(value, fixed_name)

def case(
    *conditions: tuple[str | PredicateProtocol | LogicalOperatorProtocol, str | int | float | PredicateProtocol],
    else_: str | int | float | ExprProtocol,
) -> AliasedProtocol:
    return _BaseCase(conditions=conditions, else_=else_)

def interval(as_int: bool = True) -> IntervalProtocol:
    return _BaseInterval(as_int=as_int)

def desc(*args: str | int) -> DescProtocol:
    return _BaseDesc(items=args)

def window_spec(
    partition_by: list[str | FunctionProtocol] = None,
    order_by: list[str | DescProtocol] = None,
    window: str = '',
    frame_mode: FrameModeProtocol = None,
) -> WindowSpecProtocol:
    return _BaseOverClause(
        _window=window,
        _partition_by=partition_by,
        _order_by=order_by,
        _frame_mode=frame_mode,
    )

def distinct(
    *args: str | ExprProtocol,
    on: tuple[str | ExprProtocol, ...] | list[str | ExprProtocol] | None = None,
) -> ExprProtocol:
    return BaseDistinct(_on_items=on or (), _items=args)


def field_(name: str) -> ColumnProtocol:
    return _field(default_factory=lambda: col(name))


@dataclass(slots=True)
class Source(SourceProtocol):
    _david8_source: ClassVar[str]
    _david8_db: ClassVar[str] = ''
    _david8_alias: str = ''

    @classmethod
    def get_source(cls) -> str:
        return cls._david8_source

    @classmethod
    def get_db(cls) -> str:
        return cls._david8_db

    def as_(self, alias: str) -> 'Source':
        self._david8_alias = alias
        return self

    def __getattribute__(self, name, /):
        value = object.__getattribute__(self, name)
        if isinstance(value, ColumnProtocol):
            return _FullTableName(value.get_name(), db=self._david8_alias)

        if isinstance(value, _BaseAliased):
            return _FullTableName(name, db=self._david8_alias)

        return value

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self._david8_db:
            name = f'{dialect.quote_ident(self._david8_db)}.{dialect.quote_ident(self._david8_source)}'
        else:
            name = f'{dialect.quote_ident(self._david8_source)}'

        if self._david8_alias:
            return f'{name} AS {dialect.quote_ident(self._david8_alias)}'
        return name
