import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import JoinProtocol, SelectProtocol
from ..protocols.sql import LogicalOperatorProtocol, PredicateProtocol


@dataclasses.dataclass(slots=True)
class BaseJoin(JoinProtocol):
    _join_type: str
    _on: [LogicalOperatorProtocol | PredicateProtocol, ...] = dataclasses.field(default_factory=tuple)
    _alias: str = ''
    _from: tuple[str, str] | SelectProtocol = dataclasses.field(default_factory=tuple)  # ('table', 'db') | Query

    def get_sql(self, dialect: DialectProtocol) -> str:
        on = f"{' AND '.join(on.get_sql(dialect) for on in self._on)}"
        alias = f' AS {self._alias}' if self._alias else ''
        if isinstance(self._from, SelectProtocol):
            source = self._from.get_sql(dialect)
        else:
            table, db = self._from
            source = dialect.quote_ident(table)
            if db:
                source = '.'.join([source, dialect.quote_ident(db)])

        return f'{self._join_type} JOIN {source}{alias} ON ({on})'

    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'JoinProtocol':
        self._on += args
        return self

    def table(self, name: str, db: str = '') -> 'JoinProtocol':
        self._from = (name, db, )
        return self

    def query(self, query: SelectProtocol) -> 'JoinProtocol':
        self._from = query
        return self

    def as_(self, alias: str) -> JoinProtocol:
        self._alias = alias
        return self
