import dataclasses

from ..core.base_aliased import Column
from ..protocols.dialect import DialectProtocol
from ..protocols.sql import (
    DeleteProtocol,
    ExprProtocol,
    InsertProtocol,
    LogicalOperatorProtocol,
    PredicateProtocol,
    SelectProtocol,
    UpdateProtocol,
)
from .base_dql import BaseWhereConstruction
from .base_expressions import FullTableName
from .base_query import BaseQuery


@dataclasses.dataclass(slots=True)
class BaseUpdate(BaseQuery, UpdateProtocol):
    dialect: DialectProtocol = None
    alias: str = ''
    target_table: FullTableName = dataclasses.field(default_factory=FullTableName)
    where_construction: BaseWhereConstruction = dataclasses.field(default_factory=BaseWhereConstruction)
    set_construction: tuple[
        str,
        [str | int | float | ExprProtocol | SelectProtocol],
        ...
    ] = dataclasses.field(default_factory=tuple)

    def table(self, table_name: str, alias: str = '', db_name: str = '') -> 'UpdateProtocol':
        self.target_table.set_names(table_name, db_name)
        self.alias = alias
        return self

    def set_(self, column: str, value: str | int | float | ExprProtocol | SelectProtocol) -> 'UpdateProtocol':
        self.set_construction += ((column, value, ), )
        return self

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'UpdateProtocol':
        self.where_construction.add_conditions(*args)
        return self

    def _table_to_sql(self, dialect: DialectProtocol) -> str:
        table = self.target_table.get_sql(dialect)
        if self.alias:
            table = f'{table} AS {dialect.quote_ident(self.alias)}'

        return table

    def _set_construction_to_sql(self, dialect: DialectProtocol) -> str:
        set_columns = ()

        for col, value in self.set_construction:
            if isinstance(value, Column):
                sql_val = value.get_sql(dialect)
            elif isinstance(value, (ExprProtocol, SelectProtocol)):
                sql_val = f'({value.get_sql(dialect)})'
            else:
                _, sql_val = dialect.get_paramstyle().add_param(value)

            set_columns += (f'{dialect.quote_ident(col)} = {sql_val}',)

        return f' SET {", ".join(set_columns)}'

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return 'UPDATE '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        set_columns = self._set_construction_to_sql(dialect)
        table = self._table_to_sql(dialect)
        where = self.where_construction.get_sql(dialect)
        return f'{table}{set_columns}{where}'


@dataclasses.dataclass(slots=True)
class BaseInsert(BaseQuery, InsertProtocol):
    from_query_expr: SelectProtocol | None = None
    dialect: DialectProtocol = None
    alias: str = ''
    target_table: FullTableName = dataclasses.field(default_factory=FullTableName)
    values: tuple[str | float | int] = dataclasses.field(default_factory=tuple)
    column_set: tuple[str, ...] = dataclasses.field(default_factory=tuple)

    def _get_sql(self, dialect: DialectProtocol) -> str:
        columns = f' ({", ".join(dialect.quote_ident(c) for c in self.column_set)})' if self.column_set else ' '
        sql = f'INSERT INTO {self.target_table.get_sql(dialect)}{columns}'

        if self.from_query_expr:
            sql = f'{sql} {self.from_query_expr.get_sql(dialect)}'
        else:
            placeholders = ()
            for value in self.values:
                _, placeholder = dialect.get_paramstyle().add_param(value)
                placeholders += (placeholder,)

            sql = f'{sql} VALUES ({", ".join(placeholders)})'

        return sql

    def into(self, table_name: str, db_name: str = '') -> 'InsertProtocol':
        self.target_table.set_names(table_name, db_name)
        return self

    def value(self, col_name: str, value: str | float | int) -> 'InsertProtocol':
        self.values += (value, )
        self.column_set += (col_name, )
        self.from_query_expr = None
        return self

    def columns(self, *args: str) -> 'InsertProtocol':
        self.column_set = args
        return self

    def from_select(self, query: SelectProtocol) -> 'InsertProtocol':
        self.from_query_expr = query
        self.values = tuple()
        return self


@dataclasses.dataclass(slots=True)
class BaseDelete(BaseQuery, DeleteProtocol):
    target_table: FullTableName = dataclasses.field(default_factory=FullTableName)
    where_construction: BaseWhereConstruction = dataclasses.field(default_factory=BaseWhereConstruction)

    def where(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> DeleteProtocol:
        self.where_construction.add_conditions(*args)
        return self

    def from_table(self, table_name: str, db_name: str = '') -> 'DeleteProtocol':
        self.target_table.set_names(table_name, db_name)
        return self

    def _render_sql_prefix(self, dialect: DialectProtocol) -> str:
        return 'DELETE FROM '

    def _render_sql(self, dialect: DialectProtocol) -> str:
        where = self.where_construction.get_sql(dialect)
        return f'{self.target_table.get_sql(dialect)}{where}'
