import dataclasses
from typing import Any

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import JoinProtocol, SelectProtocol
from ..protocols.sql import (
    AliasedProtocol,
    ExprProtocol,
    FunctionProtocol,
    LogicalOperatorProtocol,
    PredicateProtocol,
)


@dataclasses.dataclass(slots=True)
class BaseSelect(SelectProtocol):
    def __init__(
        self,
        dialect: DialectProtocol,
        select: tuple[str | AliasedProtocol | ExprProtocol | FunctionProtocol, ...] | None = None,
        with_queries: tuple[tuple[str, SelectProtocol], ...] = None,
    ):
        self._select = select or ()
        self._where: tuple[ExprProtocol, ...] = ()
        self._order_by: tuple[tuple[str | int, str], ...] = ()
        self._group_by: tuple = ()
        self._with_queries = with_queries or ()
        self._having: tuple[ExprProtocol, ...] = ()
        # True = UNION ALL
        self._unions: tuple[tuple[str, SelectProtocol], ...] = ()  # ((True, query1), (False, query2))
        self._joins: tuple[JoinProtocol, ...] = ()

        self._from_table = ''
        self._from_db = ''
        self._from_query: SelectProtocol | None = None
        self._alias = ''
        self._limit: int | None = None
        self._dialect = dialect


    def select(self, *args: str | AliasedProtocol | ExprProtocol | FunctionProtocol) -> SelectProtocol:
        self._select += args
        return self

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> SelectProtocol:
        self._where += args
        return self

    def from_table(self, table_name: str, alias: str = '', db_name: str = '') -> SelectProtocol:
        self._from_db = db_name
        self._from_table = table_name
        self._alias = alias
        self._from_query = None
        return self

    def from_query(self, query: 'SelectProtocol', alias: str = '') -> 'SelectProtocol':
        self._from_query = query
        self._alias = alias
        self._from_db = ''
        self._from_table = ''
        return self

    def group_by(self, *args: str | int) -> SelectProtocol:
        self._group_by += args
        return self

    def limit(self, value: int) -> SelectProtocol:
        self._limit = value
        return self

    def _columns_to_sql(self) -> str:
        return ', '.join(
            self._dialect.quote_ident(column)
            if isinstance(column, str) else column.get_sql(self._dialect)
            for column in self._select
        )

    def _where_to_sql(self) -> str:
        if not self._where:
            return ''

        return f" WHERE {' AND '.join(predicate.get_sql(self._dialect) for predicate in self._where)}"

    def _order_by_to_sql(self) -> str:
        if not self._order_by:
            return ''

        order_items = tuple(
            f'{(value if isinstance(value, int) else self._dialect.quote_ident(value))}{ordr_type}'
            for value, ordr_type in self._order_by
        )

        return f" ORDER BY {', '.join(order_items)}"

    def _with_queries_to_sql(self) -> str:
        if not self._with_queries:
            return ''

        with_items = ', '.join(
            f'{self._dialect.quote_ident(alias)} AS ({query.get_sql(self._dialect)})'
            for alias, query in self._with_queries
        )

        return f'WITH {with_items} '

    def _from_to_sql(self, dialect: DialectProtocol = None) -> str:
        source = ''
        if self._from_query:
            source = f'({self._from_query.get_sql(self._dialect)})'
        elif self._from_table:
            source = self._dialect.quote_ident(self._from_table)
            if self._from_db:
                from_db = self._dialect.quote_ident(self._from_db)
                source = f'{from_db}.{source}'
        else:
            return source

        alias = f' AS {self._dialect.quote_ident(self._alias)}' if self._alias else ''
        return f' FROM {source}{alias}'

    def _union_to_sql(self) -> str:
        if not self._unions:
            return ''

        return ' ' + ' '.join(
            f"UNION{' ALL' if union_type else ''} {query.get_sql(self._dialect)}"
            for union_type, query in self._unions
        )

    def _group_by_to_sql(self) -> str:
        if not self._group_by:
            return ''

        return ' GROUP BY ' + ', '.join(
            f"{self._dialect.quote_ident(f) if isinstance(f, str) else str(f)}"
            for f in self._group_by
        )

    def _having_to_sql(self) -> str:
        if not self._having:
            return ''

        return f" HAVING {' AND '.join(p.get_sql(self._dialect) for p in self._having)}"

    def _joins_to_sql(self) -> str:
        if not self._joins:
            return ''

        return ' ' + ' '.join(
            join.get_sql(self._dialect)
            for join in self._joins
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
        [ OFFSET <offset> ]
        [ FETCH { FIRST | NEXT } <n> { ROW | ROWS } ONLY ]
        """
        if dialect is None:
            self._dialect.get_paramstyle().reset_parameters()

        with_query = self._with_queries_to_sql()
        select = self._columns_to_sql()
        from_ref = self._from_to_sql(dialect)
        joins = self._joins_to_sql()
        where = self._where_to_sql()
        group_by = self._group_by_to_sql()
        having = self._having_to_sql()
        union = self._union_to_sql()
        order_by = self._order_by_to_sql()

        limit = f' LIMIT {self._limit}' if self._limit else ''
        sql = f'{with_query}SELECT {select}{from_ref}{joins}{where}{group_by}{order_by}{having}{limit}{union}'

        return sql

    def get_parameters(self) -> dict:
        return self._dialect.get_paramstyle().get_parameters()

    def get_list_parameters(self) -> list[Any]:
        return self._dialect.get_paramstyle().get_list_parameters()

    def get_tuple_parameters(self) -> tuple[Any]:
        return self._dialect.get_paramstyle().get_tuple_parameters()

    def _add_to_order_by(self, *args: str | int, desc: bool = False):
        for arg in args:
            self._order_by += ((arg, ' DESC' if desc else ''), )

    def order_by(self, *args: str | int) -> SelectProtocol:
        self._add_to_order_by(*args)
        return self

    def order_by_desc(self, *args: str | int) -> 'SelectProtocol':
        self._add_to_order_by(*args, desc=True)
        return self

    def union(self, *args: SelectProtocol, all_flag: bool = True) -> SelectProtocol:
        for select in args:
            self._unions += (all_flag, select, ),

        return self

    def having(self, *args: PredicateProtocol | LogicalOperatorProtocol) -> SelectProtocol:
        self._having += args
        return self

    def join(self, join: JoinProtocol) -> SelectProtocol:
        self._joins += (join,)
        return self
