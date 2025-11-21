import dataclasses
from typing import Any

from ..core.base_aliased import AliasedProtocol
from ..protocols.dialect import DialectProtocol
from ..protocols.dml import JoinProtocol, SelectProtocol
from ..protocols.sql import (
    ExprProtocol,
    FunctionProtocol,
    LogicalOperatorProtocol,
    PredicateProtocol,
)
from .log import log


@dataclasses.dataclass(slots=True)
class BaseSelect(SelectProtocol):
    source_alias: str = ''
    dialect: DialectProtocol = None
    select_columns: tuple[
        str | AliasedProtocol | ExprProtocol | FunctionProtocol,
        ...
    ] = dataclasses.field(default_factory=tuple)

    where_conditions: tuple[ExprProtocol, ...] = dataclasses.field(default_factory=tuple)
    order_by_expressions: tuple[tuple[str | int, str], ...] = dataclasses.field(default_factory=tuple)
    group_by_expressions: tuple = dataclasses.field(default_factory=tuple)
    with_queries: tuple = dataclasses.field(default_factory=tuple)
    having_expressions: tuple[ExprProtocol, ...] = dataclasses.field(default_factory=tuple)

    # True = UNION ALL, False - regular union
    # ((True, query1), (False, query2))
    unions: tuple[tuple[str, SelectProtocol], ...] = dataclasses.field(default_factory=tuple)
    joins: tuple[JoinProtocol, ...] = dataclasses.field(default_factory=tuple)
    from_table_value: str = ''
    from_db_value: str = ''
    from_query_expr: SelectProtocol | None = None
    limit_value: int | None = None

    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        self.select_columns += args
        return self

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> SelectProtocol:
        self.where_conditions += args
        return self

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> SelectProtocol:
        self.from_db_value = db_name
        self.from_table_value = table_name
        self.source_alias = alias
        self.from_query_expr = None
        return self

    def from_query(self, query: 'SelectProtocol', alias: str = '') -> 'SelectProtocol':
        self.from_query_expr = query
        self.source_alias = alias
        self.from_db_value = ''
        self.from_table_value = ''
        return self

    def group_by(self, *args: str | int) -> SelectProtocol:
        self.group_by_expressions += args
        return self

    def limit(self, value: int) -> SelectProtocol:
        self.limit_value = value
        return self

    def _columns_to_sql(self, dialect: DialectProtocol) -> str:
        return ', '.join(
            dialect.quote_ident(column)
            if isinstance(column, str) else column.get_sql(dialect)
            for column in self.select_columns
        )

    def _where_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.where_conditions:
            return ''

        return f" WHERE {' AND '.join(predicate.get_sql(dialect) for predicate in self.where_conditions)}"

    def _order_by_to_sql(self) -> str:
        if not self.order_by_expressions:
            return ''

        order_items = tuple(
            f'{(value if isinstance(value, int) else self.dialect.quote_ident(value))}{ordr_type}'
            for value, ordr_type in self.order_by_expressions
        )

        return f" ORDER BY {', '.join(order_items)}"

    def _with_queries_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.with_queries:
            return ''

        with_items = ', '.join(
            f'{dialect.quote_ident(alias)} AS ({query.get_sql(dialect)})'
            for alias, query in self.with_queries
        )

        return f'WITH {with_items} '

    def _from_to_sql(self, dialect: DialectProtocol) -> str:
        if self.from_query_expr:
            source = f'({self.from_query_expr.get_sql(dialect)})'
        elif self.from_table_value:
            source = dialect.quote_ident(self.from_table_value)
            if self.from_db_value:
                source = f'{dialect.quote_ident(self.from_db_value)}.{source}'
        else:
            return ''

        source = f'{source} AS {dialect.quote_ident(self.source_alias)}' if self.source_alias else source
        return f' FROM {source}'

    def _union_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.unions:
            return ''

        return ' ' + ' '.join(
            f"UNION{' ALL' if union_type else ''} {query.get_sql(dialect)}"
            for union_type, query in self.unions
        )

    def _group_by_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.group_by_expressions:
            return ''

        return ' GROUP BY ' + ', '.join(
            f"{dialect.quote_ident(f) if isinstance(f, str) else str(f)}"
            for f in self.group_by_expressions
        )

    def _having_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.having_expressions:
            return ''

        return f" HAVING {' AND '.join(p.get_sql(dialect) for p in self.having_expressions)}"

    def _joins_to_sql(self, dialect: DialectProtocol) -> str:
        if not self.joins:
            return ''

        return ' ' + ' '.join(
            join.get_sql(dialect)
            for join in self.joins
        )

    def get_sql(self, dialect: DialectProtocol = None) -> str:
        """
        Don't forget about a query rendering sequence. You can break the sequence of query parameters, see:
        self._dialect.get_paramstyle().reset_parameters()

        [ WITH [ RECURSIVE ] <with_list> ]
        SELECT [ DISTINCT | ALL ]
               <select_list>
        FROM   <table_reference_list>
        [ JOIN <join_expression> ]
        [ WHERE <search_condition> ]
        [ JOIN <join_condition> ]
        [ GROUP BY <grouping_element_list> ]
        [ HAVING <search_condition> ]
        [ WINDOW <window_definition_list> ]
        [ { UNION | INTERSECT | EXCEPT } [ ALL | DISTINCT ] <query_expression> ]
        [ ORDER BY <sort_specification_list> ]
        [ LIMIT <limit_value> ]
        """
        if dialect is None:
            self.dialect.get_paramstyle().reset_parameters()
            dialect = self.dialect
            log_query = True
        else:
            log_query = False

        with_query = self._with_queries_to_sql(dialect)
        select = self._columns_to_sql(dialect)
        from_ref = self._from_to_sql(dialect)
        joins = self._joins_to_sql(dialect)
        where = self._where_to_sql(dialect)
        group_by = self._group_by_to_sql(dialect)
        having = self._having_to_sql(dialect)
        union = self._union_to_sql(dialect)
        order_by = self._order_by_to_sql()

        limit = f' LIMIT {self.limit_value}' if self.limit_value else ''
        sql = f'{with_query}SELECT {select}{from_ref}{joins}{where}{group_by}{order_by}{having}{limit}{union}'
        if log_query:
            log.info('%s\n%s', sql, self.get_parameters())

        return sql

    def get_parameters(self) -> dict:
        return self.dialect.get_paramstyle().get_parameters()

    def get_list_parameters(self) -> list[Any]:
        return self.dialect.get_paramstyle().get_list_parameters()

    def get_tuple_parameters(self) -> tuple[Any]:
        return self.dialect.get_paramstyle().get_tuple_parameters()

    def _add_to_order_by(self, *args: str | int, desc: bool = False):
        for arg in args:
            self.order_by_expressions += ((arg, ' DESC' if desc else ''), )

    def order_by(self, *args: str | int) -> SelectProtocol:
        self._add_to_order_by(*args)
        return self

    def order_by_desc(self, *args: str | int) -> 'SelectProtocol':
        self._add_to_order_by(*args, desc=True)
        return self

    def union(self, *args: SelectProtocol, all_flag: bool = True) -> SelectProtocol:
        for select in args:
            self.unions += (all_flag, select, ),

        return self

    def having(self, *args: PredicateProtocol | LogicalOperatorProtocol) -> SelectProtocol:
        self.having_expressions += args
        return self

    def join(self, join: JoinProtocol) -> SelectProtocol:
        self.joins += (join,)
        return self
