import dataclasses

from david8.core.arg_convertors import to_col_or_expr
from david8.core.base_aliased import BaseAliased
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import ExprProtocol, FunctionProtocol


@dataclasses.dataclass(slots=True)
class Function(BaseAliased, FunctionProtocol):
    name: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f"{self.name}()"


@dataclasses.dataclass(slots=True, kw_only=True)
class ZeroArgsCallableFactory:
    name: str = ''

    def __call__(self) -> FunctionProtocol:
        return Function(self.name)


@dataclasses.dataclass(slots=True, kw_only=True)
class FnCallableFactory:
    name: str = ''


@dataclasses.dataclass(slots=True)
class _SeparatedStrArgsFn(Function):
    """
    str works as column name. concat('col_name', 2, 0.5, val('test')) -> concat(col_name, '2', '0.5', 'test')
    """
    args: tuple
    separator: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        items = ()
        for item in self.args:
            if isinstance(item, str):
                items += (dialect.quote_ident(item),)
                continue
            if isinstance(item, float | int):
                items += (f"'{item}'",)
                continue

            items += (item.get_sql(dialect),)

        return f"{self.name}({self.separator.join(items)})"


@dataclasses.dataclass(slots=True)
class SeparatedStrArgsCallableFactory(FnCallableFactory):
    separator: str

    def __call__(self, *args: int | float | str | ExprProtocol) -> FunctionProtocol:
        return _SeparatedStrArgsFn(self.name, args, self.separator)


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


@dataclasses.dataclass(slots=True)
class OneArgDistinctCallableFactory(FnCallableFactory):
    def __call__(self, column: str, distinct: bool = False) -> FunctionProtocol:
        return _OneArgDistinctFn(self.name, column, distinct)


@dataclasses.dataclass(slots=True)
class _StrArgFn(Function):
    """
    upper(col_name)
    lower(col_name)
    etc
    """
    value: str | ExprProtocol = ''

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self.value, str):
            value = dialect.quote_ident(self.value)
        else:
            value = self.value.get_sql(dialect)
        return f"{self.name}({value})"


@dataclasses.dataclass(slots=True)
class StrArgCallableFactory(FnCallableFactory):
    value: str = ''

    def __call__(self, value: str | ExprProtocol) -> FunctionProtocol:
        return _StrArgFn(self.name, value)


@dataclasses.dataclass(slots=True)
class _CastFn(Function):
    value: str | ExprProtocol
    cast_type: str

    def _get_sql(self, dialect: DialectProtocol) -> str:
        value = to_col_or_expr(self.value, dialect)
        return f"{self.name}({value} AS {self.cast_type})"


@dataclasses.dataclass(slots=True)
class CastCallableFactory(FnCallableFactory):
    name = 'CAST'
    def __call__(self, value: str | ExprProtocol, cast_type: str) -> FunctionProtocol:
        return _CastFn('CAST', value, cast_type)
