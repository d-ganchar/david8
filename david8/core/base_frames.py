import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import (
    DescProtocol,
    FrameBoundProtocol,
    FrameModeProtocol,
    FunctionProtocol,
    OverClauseProtocol,
    WindowSpecProtocol,
)


@dataclasses.dataclass(slots=True)
class BaseOverClause(OverClauseProtocol, WindowSpecProtocol):
    _window: str = ''
    _partition_by: list[str | FunctionProtocol] = dataclasses.field(default_factory=list)
    _order_by: list[str | list[str]] = dataclasses.field(default_factory=list)
    _frame_mode: FrameModeProtocol = None

    def over(
        self,
        partition_by: list[str | FunctionProtocol] = None,
        order_by: list[str | DescProtocol] = None,
        window: str = '',
        frame_mode: FrameModeProtocol = None,
    ) -> 'OverClauseProtocol':
        self._window = window
        self._frame_mode = frame_mode
        self._partition_by = partition_by or []
        self._order_by = order_by or []

        return self

    def get_sql(self, dialect: DialectProtocol) -> str:
        if not any([self._window, self._partition_by, self._order_by]):
            return ''

        parts = ()
        if self._partition_by:
            parts += ('PARTITION BY',)
            for part in self._partition_by:
                if isinstance(part, str):
                    parts += (dialect.quote_ident(part),)
                elif isinstance(part, FunctionProtocol):
                    parts += (part.get_sql(dialect),)

        if self._order_by:
            order_by_items = ()
            for part in self._order_by:
                if isinstance(part, str):
                    order_by_items += (dialect.quote_ident(part), )
                    continue

                if isinstance(part, DescProtocol):
                    order_by_items += (part.get_sql(dialect), )

            parts += ('ORDER BY', ', '.join(order_by_items))

        if self._frame_mode:
            parts += (self._frame_mode.get_sql(dialect),)

        window_name = f'{self._window} ' if self._window else ''
        return f"({window_name}{' '.join(parts)})"


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
