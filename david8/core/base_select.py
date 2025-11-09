import dataclasses
from dataclasses import dataclass

from ..core.columns import WhereCondition
from ..protocols.dml import SelectProtocol


@dataclass(slots=True)
class BaseSelect(SelectProtocol):
    _select: tuple = dataclasses.field(default_factory=tuple)
    _where: tuple[WhereCondition, ...] = dataclasses.field(default_factory=tuple)
    _group_by: tuple = dataclasses.field(default_factory=tuple)
    _from: str = ''
    _limit: int = None

    def select(self, *args) -> 'SelectProtocol':
        self._select = args
        return self

    def where(self, *args: WhereCondition) -> 'SelectProtocol':
        self._where = args
        return self

    def from_table(self, table_name: str) -> 'SelectProtocol':
        self._from = table_name
        return self

    def group_by(self, *args) -> 'SelectProtocol':
        self._group_by = args
        return self

    def limit(self, value: int) -> 'SelectProtocol':
        self._limit = value
        return self

    def to_sql(self) -> tuple[str, list]:
        parameters = []
        fields = ', '.join([f'{f}' for f in self._select])
        _from = f' FROM {self._from}' if self._from else ''
        group_by = ', '.join([f'{f}' for f in self._group_by])
        group_by = f' GROUP BY {group_by}' if group_by else ''
        limit = f' LIMIT {self._limit}' if self._limit else ''

        where = []
        for cond in self._where:
            cond_str, cond_params = cond.to_sql()
            parameters.extend(cond_params)
            where.append(cond_str)

        where = f" WHERE {' AND '.join(where)}" if where else ''

        return f'SELECT {fields}{_from}{where}{group_by}{limit}', parameters
