import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import FrameBoundProtocol, FrameModeProtocol


@dataclasses.dataclass(slots=True)
class UnboundedPrecedingBound(FrameBoundProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'UNBOUNDED PRECEDING'


@dataclasses.dataclass(slots=True)
class PrecedingBound(FrameBoundProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'PRECEDING'


@dataclasses.dataclass(slots=True)
class FollowingBound(FrameBoundProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'FOLLOWING'


@dataclasses.dataclass(slots=True)
class UnboundedFollowingBound(FrameBoundProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'UNBOUNDED FOLLOWING'


@dataclasses.dataclass(slots=True)
class CurrentRowBound(FrameBoundProtocol):
    def get_sql(self, dialect: DialectProtocol) -> str:
        return 'CURRENT ROW'


@dataclasses.dataclass(slots=True)
class BaseMode(FrameModeProtocol):
    _name: str
    _start: FrameBoundProtocol
    _end: FrameBoundProtocol = None

    def get_sql(self, dialect: DialectProtocol) -> str:
        if self._end:
            return f'{self._name} BETWEEN {self._start.get_sql(dialect)} AND {self._end.get_sql(dialect)}'
        return f'{self._name} {self._start.get_sql(dialect)}'


class RowsMode(BaseMode):
    pass

class RangeMode(BaseMode):
    pass
