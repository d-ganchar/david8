from typing import Any, Protocol, Union

from ..protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    def get_sql(self, dialect: DialectProtocol = None) -> str: ...

    def get_parameters(self) -> dict: ...

    def get_list_parameters(self) -> list[Any]: ...

    def get_tuple_parameters(self) -> tuple[Any]: ...

    def get_dialect(self) -> DialectProtocol: ...


class ExprProtocol:
    def get_sql(self, dialect: DialectProtocol) -> str: ...


class DescProtocol(ExprProtocol): ...


class WindowSpecProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class AliasedProtocol(ExprProtocol):
    def as_(self, alias: str) -> 'AliasedProtocol': ...


class ColumnProtocol(AliasedProtocol):
    def get_name(self) -> str: ...


class SourceProtocol(AliasedProtocol):
    @classmethod
    def get_source(cls) -> str: ...

    @classmethod
    def get_db(cls) -> str: ...


class ParameterProtocol(AliasedProtocol): ...


class ValueProtocol(AliasedProtocol): ...


class PredicateProtocol(AliasedProtocol): ...


class FunctionProtocol(AliasedProtocol): ...


class FrameModeProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class FrameBoundProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class LogicalOperatorProtocol(ExprProtocol): ...


class OverClauseProtocol(FunctionProtocol):
    """
    Deprecated since 1.6.0b1. Will be removed in 0.1.0
    Replaced with AggFunctionProtocol()
    """
    def over(
        self,
        partition_by: list[str | FunctionProtocol] = None,
        order_by: list[str | DescProtocol] = None,
        window: str = '',
        frame_mode: FrameModeProtocol = None,
    ) -> 'WindowSpecProtocol': ...


class AggFunctionProtocol(FunctionProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """
    def over(
        self,
        partition_by: list[str | FunctionProtocol] = None,
        order_by: list[str | DescProtocol] = None,
        window: str = '',
        frame_mode: FrameModeProtocol = None,
    ) -> 'WindowSpecProtocol': ...

    def filter(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'AggFunctionProtocol': ...


class JoinProtocol(AliasedProtocol): ...


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> 'SelectProtocol': ...

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'SelectProtocol': ...

    def from_source(self, source: SourceProtocol) -> 'SelectProtocol': ...

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'SelectProtocol': ...

    def from_expr(self, expr: Union['SelectProtocol', FunctionProtocol], alias: str = '') -> 'SelectProtocol': ...

    def group_by(self, *args: str | int) -> 'SelectProtocol': ...

    def limit(self, value: int) -> 'SelectProtocol': ...

    def offset(self, value: int) -> 'SelectProtocol': ...

    def order_by(self, *args: str | int | DescProtocol) -> 'SelectProtocol': ...

    def union(self, *args: 'SelectProtocol', all_flag: bool = True) -> 'SelectProtocol': ...

    def join(self, *join: JoinProtocol) -> 'SelectProtocol': ...

    def window(self, name: str, spec: WindowSpecProtocol) -> 'SelectProtocol': ...

    def having(self, *args: PredicateProtocol) -> 'SelectProtocol': ...

    def order_by_desc(self, *args: str | int) -> 'SelectProtocol':
        """
        Deprecated since 1.2.0b1. Will be removed in 0.1.0
        Use `order_by() + DescProtocol()` instead, example:

        from david8.expressions import desc

        qb.select('*').order_by(
            'style',
            desc('height', 'age'),
            'name',
            desc('color', 'weight')
        ).get_sql()

        # SELECT * FROM trees ORDER BY style, height DESC, age DESC, name, color DESC, weight DESC
        """


class Sql92JoinProtocol(JoinProtocol):
    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'Sql92JoinProtocol': ...

    def table(self, name: str, db: str = '') -> 'Sql92JoinProtocol': ...

    def query(self, query: SelectProtocol) -> 'Sql92JoinProtocol': ...

    def using(self, *args: str) -> 'Sql92JoinProtocol': ...

    def source(self, source: SourceProtocol) -> 'Sql92JoinProtocol': ...


class LiteralJoinProtocol(JoinProtocol):
    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'LiteralJoinProtocol': ...

    def expression(self, expression: ExprProtocol) -> 'LiteralJoinProtocol': ...


class UpdateProtocol(QueryProtocol):
    def table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol': ...

    def set_record(self, record: dict) -> 'UpdateProtocol': ...

    def set_(self, column: str, value: str | int | float | ExprProtocol | SelectProtocol) -> 'UpdateProtocol': ...

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'UpdateProtocol': ...


class InsertProtocol(QueryProtocol):
    def into(self, table_name: str, db_name: str = '') -> 'InsertProtocol': ...

    def into_source(self, source: SourceProtocol) -> 'InsertProtocol': ...

    def value(self, col_name: str, value: str | float | int) -> 'InsertProtocol':
        """
        Deprecated since 1.5.0b1. Will be removed in 0.1.0
        Use record():
            qb
            .insert()
            .into('movie')
            .record({'name': 'Aliens', 'year': 1986}),
        """

    def columns(self, *args: str) -> 'InsertProtocol':
        """
        Deprecated since 1.5.0b1. Will be removed in 0.1.0
        Use from_expr():
            qb
            .into('movie', 'art')
            .from_expr(
                ['name', 'year'],
                qb.select('col1', 'col2').from_table('old_movie')
            )
        """

    def from_select(self, query: SelectProtocol) -> 'InsertProtocol':
        """
        Deprecated since 1.5.0b1. Will be removed in 0.1.0
        Use from_expr():
            qb
            .into('movie', 'art')
            .from_expr(
                ['name', 'year'],
                qb.select('col1', 'col2').from_table('old_movie')
            )
        """

    def values(
        self,
        columns: tuple[str | ColumnProtocol, ...] | list[str | ColumnProtocol],
        data: tuple | list
    ) -> 'InsertProtocol': ...

    def from_expr(
        self,
        columns: tuple[str] | list[str],
        expr: Union['SelectProtocol', ExprProtocol]
    ) -> 'InsertProtocol': ...

    def record(self, record: dict) -> 'InsertProtocol': ...

    def records(self, records: list[dict[str, Any]]) -> 'InsertProtocol': ...


class DeleteProtocol(QueryProtocol):
    def from_table(self, table_name: str, db_name: str = '') -> 'DeleteProtocol': ...

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'DeleteProtocol': ...

    def from_source(self, source: SourceProtocol) -> 'DeleteProtocol': ...


class CreateTableProtocol(QueryProtocol):
    def as_(self, query: SelectProtocol, table: str, db: str = '') -> 'CreateTableProtocol': ...


class DropProtocol(QueryProtocol):
    def table(self, table_name: str, db_name: str = '', if_exists: bool = False) -> 'DropProtocol': ...

    def view(self, view_name: str, db_name: str = '', if_exists: bool = False) -> 'DropProtocol': ...


class IntervalProtocol(AliasedProtocol):
    def second(self, value: int) -> 'IntervalProtocol': ...

    def minute(self, value: int) -> 'IntervalProtocol': ...

    def hour(self, value: int) -> 'IntervalProtocol': ...

    def day(self, value: int) -> 'IntervalProtocol': ...

    def week(self, value: int) -> 'IntervalProtocol': ...

    def month(self, value: int) -> 'IntervalProtocol': ...

    def quarter(self, value: int) -> 'IntervalProtocol': ...

    def year(self, value: int) -> 'IntervalProtocol': ...
