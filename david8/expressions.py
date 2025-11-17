from .core.base_aliased import BaseAliased
from .protocols.dialect import DialectProtocol


class Column(BaseAliased):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{dialect.quote_ident(self._name)}'


class Parameter(BaseAliased):
    def __init__(self, value: str | int | float) -> None:
        super().__init__()
        self._value = value

    def _get_sql(self, dialect: DialectProtocol) -> str:
        value = dialect.get_paramstyle().add_param(self._value)
        return value


class Value(BaseAliased):
    def __init__(self, value: str | int | float) -> None:
        super().__init__()
        self._value = value

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self._value, str):
            return f"'{self._value}'"
        return f'{self._value}'
