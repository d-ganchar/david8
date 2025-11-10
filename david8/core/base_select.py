import dataclasses
from dataclasses import dataclass

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import SelectProtocol
from ..protocols.sql import AsExpressionProtocol, LogicalOperatorProtocol, SqlExpressionProtocol


@dataclass(slots=True)
class BaseSelect(SelectProtocol):
    _dialect: DialectProtocol
    _select: tuple[str | AsExpressionProtocol, ...] = dataclasses.field(default_factory=tuple)
    _where: tuple[SqlExpressionProtocol, ...] = dataclasses.field(default_factory=tuple)
    _group_by: tuple = dataclasses.field(default_factory=tuple)
    _from_table: str = ''
    _from_db: str = ''
    _limit: int = None

    def select(self, *args: str | AsExpressionProtocol) -> 'SelectProtocol':
        self._select = args
        return self

    def where(self, *args: LogicalOperatorProtocol | SqlExpressionProtocol) -> 'SelectProtocol':
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

    def _convert_columns(self) -> str:
        columns = []

        for column in self._select:
            if isinstance(column, str):
                columns.append(self._dialect.quote_ident(column))
            else:
                columns.append(column.get_sql(self._dialect))

        return ', '.join(columns)

    def _convert_where(self) -> str:
        where = []
        for predicate in self._where:
            where.append(predicate.get_sql(self._dialect))

        return f" WHERE {' AND '.join(where)}" if where else ''

    def get_sql(self) -> str:
        self._dialect.get_paramstyle().reset_parameters()

        if self._from_table:
            _from = self._dialect.quote_ident(self._from_table)
            if self._from_db:
                from_db = self._dialect.quote_ident(self._from_db)
                _from = f'{from_db}.{_from}'

            _from = f' FROM {_from}'
        else:
            _from = ''

        group_by = ', '.join([f'{f}' for f in self._group_by])
        group_by = f' GROUP BY {group_by}' if group_by else ''
        limit = f' LIMIT {self._limit}' if self._limit else ''
        columns = self._convert_columns()
        where = self._convert_where()

        return f'SELECT {columns}{_from}{where}{group_by}{limit}'

    def get_parameters(self) -> list | dict:
        return self._dialect.get_paramstyle().get_parameters()
