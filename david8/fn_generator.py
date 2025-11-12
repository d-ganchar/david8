import dataclasses
from copy import deepcopy

from david8.expressions import Column, Parameter
from david8.protocols.dialect import DialectProtocol
from david8.protocols.sql import SqlFunctionProtocol


@dataclasses.dataclass(slots=True)
class StrArgsFunction(SqlFunctionProtocol):
    _name: str
    _args: tuple = dataclasses.field(default_factory=tuple)

    def __call__(self, *args: SqlFunctionProtocol | int | float | str | Column | Parameter) -> SqlFunctionProtocol:
        self._args = args
        return deepcopy(self)

    def get_sql(self, dialect: DialectProtocol) -> str:
        items = []
        for item in self._args:
            if isinstance(item, (str, float, int)):
                items.append(f"'{item}'")
                continue

            items.append(item.get_sql(dialect))

        return f"{self._name}({', '.join(items)})"
