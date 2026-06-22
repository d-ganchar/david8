from typing import Any, Protocol, Union

from ..protocols.dialect import DialectProtocol


class QueryProtocol(Protocol):
    """
    Full SQL query
    """
    def get_sql(self, dialect: DialectProtocol = None) -> str:
        pass

    def get_parameters(self) -> dict:
        pass

    def get_list_parameters(self) -> list[Any]:
        pass

    def get_tuple_parameters(self) -> tuple[Any]:
        pass

    def get_dialect(self) -> DialectProtocol:
        pass


class ExprProtocol:
    """
    Common SQL expression
    """
    def get_sql(self, dialect: DialectProtocol) -> str:
        pass


class DescProtocol(ExprProtocol):
    pass


class WindowSpecProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class AliasedProtocol(ExprProtocol):
    def as_(self, alias: str) -> 'AliasedProtocol':
        pass


class ParameterProtocol(AliasedProtocol):
    pass


class ValueProtocol(AliasedProtocol):
    pass


class PredicateProtocol(AliasedProtocol):
    pass


class FunctionProtocol(AliasedProtocol):
    pass


class FrameModeProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class FrameBoundProtocol(ExprProtocol):
    """
    SQL:2003 (ISO/IEC 9075-2:2003)
    """


class LogicalOperatorProtocol(ExprProtocol):
    pass


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
    ) -> 'WindowSpecProtocol':
        pass


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
    ) -> 'WindowSpecProtocol':
        pass

    def filter(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'AggFunctionProtocol':
        pass


class JoinProtocol(AliasedProtocol):
    pass


class SelectProtocol(QueryProtocol):
    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> 'SelectProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'SelectProtocol':
        pass

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> 'SelectProtocol':
        pass

    def from_expr(self, expr: Union['SelectProtocol', FunctionProtocol], alias: str = '') -> 'SelectProtocol':
        pass

    def group_by(self, *args: str | int) -> 'SelectProtocol':
        pass

    def limit(self, value: int) -> 'SelectProtocol':
        pass

    def order_by(self, *args: str | int | DescProtocol) -> 'SelectProtocol':
        pass

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

    def union(self, *args: 'SelectProtocol', all_flag: bool = True) -> 'SelectProtocol':
        pass

    def having(self, *args: PredicateProtocol) -> 'SelectProtocol':
        pass

    def join(self, join: JoinProtocol) -> 'SelectProtocol':
        pass

    def window(self, name: str, spec: WindowSpecProtocol) -> 'SelectProtocol':
        pass


class Sql92JoinProtocol(JoinProtocol):
    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'Sql92JoinProtocol':
        pass

    def table(self, name: str, db: str = '') -> 'Sql92JoinProtocol':
        pass

    def query(self, query: SelectProtocol) -> 'Sql92JoinProtocol':
        pass

    def using(self, *args: str) -> 'Sql92JoinProtocol':
        pass


class UpdateProtocol(QueryProtocol):
    def table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        pass

    def set_record(self, record: dict) -> 'UpdateProtocol':
        pass

    def set_(self, column: str, value: str | int | float | ExprProtocol | SelectProtocol) -> 'UpdateProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'UpdateProtocol':
        pass


class InsertProtocol(QueryProtocol):
    def into(self, table_name: str, db_name: str = '') -> 'InsertProtocol':
        pass

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

    def values(self, columns: tuple[str] | list[str], data: tuple | list) -> 'InsertProtocol':
        pass

    def from_expr(
        self,
        columns: tuple[str] | list[str],
        expr: Union['SelectProtocol', ExprProtocol]
    ) -> 'InsertProtocol':
        pass

    def record(self, record: dict) -> 'InsertProtocol':
        pass


class DeleteProtocol(QueryProtocol):
    def from_table(self, table_name: str, db_name: str = '') -> 'DeleteProtocol':
        pass

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'DeleteProtocol':
        pass


class CreateTableProtocol(QueryProtocol):
    def as_(self, query: SelectProtocol, table: str, db: str = '') -> 'CreateTableProtocol':
        pass


class DropProtocol(QueryProtocol):
    def table(self, table_name: str, db_name: str = '') -> 'DropProtocol':
        pass


class IntervalProtocol(AliasedProtocol):
    def second(self, value: int) -> 'IntervalProtocol':
        pass

    def minute(self, value: int) -> 'IntervalProtocol':
        pass

    def hour(self, value: int) -> 'IntervalProtocol':
        pass

    def day(self, value: int) -> 'IntervalProtocol':
        pass

    def week(self, value: int) -> 'IntervalProtocol':
        pass

    def month(self, value: int) -> 'IntervalProtocol':
        pass

    def quarter(self, value: int) -> 'IntervalProtocol':
        pass

    def year(self, value: int) -> 'IntervalProtocol':
        pass
