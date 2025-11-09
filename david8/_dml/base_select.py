import dataclasses
from dataclasses import dataclass

from .._protocols.dml import SelectProtocol


@dataclass(slots=True)
class BaseSelect(SelectProtocol):
    _select_fields: tuple = dataclasses.field(default_factory=tuple)
    _where_fields: tuple = dataclasses.field(default_factory=tuple)
    _group_by: tuple = dataclasses.field(default_factory=tuple)
    _from: str = ''

    def select(self, *args) -> 'SelectProtocol':
        self._select_fields = args
        return self

    def where(self, *args) -> 'SelectProtocol':
        self._where_fields = args
        return self

    def from_table(self, table_name: str) -> 'SelectProtocol':
        self._from = table_name
        return self

    def group_by(self, *args) -> 'SelectProtocol':
        self._group_by = args
        return self

    def to_sql(self) -> tuple[str, list]:
        fields = ', '.join([f'{f}' for f in self._select_fields])
        _from = f' FROM {self._from}' if self._from else ''
        _group_by = ', '.join([f'{f}' for f in self._group_by])
        _group_by = f' GROUP BY {_group_by}' if _group_by else ''

        return f'SELECT {fields}{_from}{_group_by}', []
