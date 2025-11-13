import dataclasses
from copy import deepcopy

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import SelectProtocol
from ..protocols.sql import (
    AsExpressionProtocol,
    SqlExpressionProtocol,
    SqlLogicalOperatorProtocol,
    SqlPredicateProtocol,
)


@dataclasses.dataclass(slots=True)
class BaseSelect(SelectProtocol):
    def __init__(
        self,
        dialect: DialectProtocol,
        from_table: str = '',
        from_db: str = '',
        limit: int = None,
        where: tuple[SqlExpressionProtocol, ...] = None,
        select: tuple[str | AsExpressionProtocol, ...] = None,
        order_by: tuple[str | int, ...] = None,
        group_by: tuple = None,
        with_queries: tuple[tuple[str, 'SelectProtocol'], ...] = None,
    ):
        self._select = select or ()
        self._where = where or ()
        self._order_by = order_by or ()
        self._group_by = group_by or ()
        self._with_queries = with_queries or ()
        self._unions: tuple[tuple[str, SelectProtocol], ...] = ()  # ((True, query1), (False, query2))

        self._from_table = from_table
        self._from_db = from_db
        self._limit = limit
        self._dialect = dialect
        self._query_parameters = deepcopy(dialect.get_paramstyle().get_parameters())


    def select(self, *args: str | AsExpressionProtocol) -> 'SelectProtocol':
        self._select = args
        return self

    def where(self, *args: SqlLogicalOperatorProtocol | SqlPredicateProtocol) -> 'SelectProtocol':
        self._where = args
        return self

    def from_table(self, table_name: str, db_name: str = '') -> 'SelectProtocol':
        self._from_db = db_name
        self._from_table = table_name
        return self

    def group_by(self, *args) -> 'SelectProtocol':
        self._group_by = args
        return self

    def limit(self, value: int) -> 'SelectProtocol':
        self._limit = value
        return self

    def _columns_to_sql(self) -> str:
        columns = []

        for column in self._select:
            if isinstance(column, str):
                columns.append(self._dialect.quote_ident(column))
            else:
                columns.append(column.get_sql(self._dialect))

        return ', '.join(columns)

    def _where_to_sql(self) -> str:
        if not self._where:
            return ''

        where = []
        for predicate in self._where:
            where.append(predicate.get_sql(self._dialect))

        return f" WHERE {' AND '.join(where)}" if where else ''

    def _order_by_to_sql(self) -> str:
        order_items = []
        for item in self._order_by:
            if isinstance(item, int):
                order_items.append(str(item))
                continue

            clean_item = item.strip()
            lower_item = clean_item.lower()

            if lower_item.endswith(' desc'):
                column = clean_item[:-5]
                column = self._dialect.quote_ident(column)
                order_items.append(f'{column} DESC')
                continue
            elif lower_item.endswith(' asc'):
                column = clean_item[:-4]
                column = self._dialect.quote_ident(column)
                order_items.append(f'{column} ASC')
                continue

            order_items.append(self._dialect.quote_ident(clean_item))

        if order_items:
            return f' ORDER BY {", ".join(order_items)}'

        return ''

    def _with_queries_to_sql(self) -> str:
        if not self._with_queries:
            return ''

        with_items = ', '.join(
            f'{self._dialect.quote_ident(alias)} AS ({query.get_sql(self._dialect)})'
            for alias, query in self._with_queries
        )

        return f'WITH {with_items} '

    def _from_table_to_sql(self) -> str:
        if not self._from_table:
            return ''

        _from = self._dialect.quote_ident(self._from_table)
        if self._from_db:
            from_db = self._dialect.quote_ident(self._from_db)
            _from = f'{from_db}.{_from}'

        return f' FROM {_from}'

    def _union_to_sql(self) -> str:
        if not self._unions:
            return ''

        union_parts = []
        for union_type, query in self._unions:
            union_parts.append(f"UNION{' ALL' if union_type else ''} {query.get_sql(self._dialect)}")

        return f" {' '.join(union_parts)}"

    def get_sql(self, dialect: DialectProtocol = None) -> str:
        if dialect is None:
            self._dialect.get_paramstyle().reset_parameters()

        with_query = self._with_queries_to_sql()
        columns = self._columns_to_sql()
        where = self._where_to_sql()
        order_by = self._order_by_to_sql()
        table = self._from_table_to_sql()

        group_by = ', '.join([f'{f}' for f in self._group_by])
        group_by = f' GROUP BY {group_by}' if group_by else ''
        limit = f' LIMIT {self._limit}' if self._limit else ''
        union = self._union_to_sql()

        sql = f'{with_query}SELECT {columns}{table}{where}{group_by}{order_by}{limit}{union}'
        self._query_parameters = deepcopy(self._dialect.get_paramstyle().get_parameters())
        return sql

    def get_parameters(self) -> list | dict:
        return deepcopy(self._query_parameters)

    def order_by(self, *args: str | int) -> 'SelectProtocol':
        self._order_by = args
        return self

    def union(self, *args: SelectProtocol, all_flag: bool = True) -> 'SelectProtocol':
        for select in args:
            self._unions += (all_flag, select, ),

        return self
