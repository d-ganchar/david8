import dataclasses
from typing import Self

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import ExprProtocol, LiteralJoinProtocol, LogicalOperatorProtocol, PredicateProtocol


@dataclasses.dataclass(slots=True)
class LiteralJoin(LiteralJoinProtocol):
    _alias: str = ''
    _on_expr: tuple[LogicalOperatorProtocol | PredicateProtocol, ...] = dataclasses.field(default_factory=tuple)
    _expr: ExprProtocol | None = None

    def as_(self, alias: str) -> Self:
        self._alias = alias
        return self

    def get_sql(self, dialect: DialectProtocol) -> str:
        on = f"{' AND '.join(on.get_sql(dialect) for on in self._on_expr)}"
        expr = self._expr.get_sql(dialect) if self._expr else ''
        return f'INNER JOIN LATERAL ({expr}) AS {self._alias} ON ({on})'

    def on(self, *args: LogicalOperatorProtocol | PredicateProtocol) -> Self:
        self._on_expr += args
        return self

    def expression(self, expression: ExprProtocol) -> Self:
        self._expr = expression
        return self
