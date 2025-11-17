import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.dml import JoinProtocol, SelectProtocol
from ..protocols.sql import LogicalOperatorProtocol, PredicateProtocol


@dataclasses.dataclass(slots=True)
class BaseJoin(JoinProtocol):
    _alias: str = ''

    def __init__(self, join_type: str):
        self._join_type = join_type
        self._on: tuple[LogicalOperatorProtocol | PredicateProtocol, ...] = ()
        self._using: tuple[str, ...] = ()
        self._from: tuple | [str, str] | SelectProtocol = ()  # ('table', 'db',) or Query
        self._alias = ''

    def get_sql(self, dialect: DialectProtocol) -> str:
        alias = f' AS {dialect.quote_ident(self._alias)}' if self._alias else ''
        if isinstance(self._from, SelectProtocol):
            source = self._from.get_sql(dialect)
        else:
            table, db = self._from
            source = dialect.quote_ident(table)
            if db:
                source = '.'.join([source, dialect.quote_ident(db)])

        if self._using:
            using = ', '.join([dialect.quote_ident(u) for u in self._using])
            return f'{self._join_type} {source}{alias} USING ({using})'

        on = f"{' AND '.join(on.get_sql(dialect) for on in self._on)}"
        return f'{self._join_type} {source}{alias} ON ({on})'

    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> 'JoinProtocol':
        self._on += args
        self._using = ()
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

    def using(self, *args: str) -> 'JoinProtocol':
        self._using = args
        self._on = ()
        return self
