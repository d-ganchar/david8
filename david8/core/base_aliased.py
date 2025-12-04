import dataclasses

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import AliasedProtocol, ParameterProtocol, ValueProtocol


@dataclasses.dataclass(slots=True, kw_only=True)
class BaseAliased(AliasedProtocol):
    alias: str = ''

    def as_(self, alias: str) -> AliasedProtocol:
        self.alias = alias
        return self

    def _get_sql(self, dialect: DialectProtocol) -> str:
        raise NotImplementedError()

    def get_sql(self, dialect: DialectProtocol) -> str:
        sql = self._get_sql(dialect)
        if self.alias:
            return f'{sql} AS {dialect.quote_ident(self.alias)}'

        return sql


class Value(BaseAliased, ValueProtocol):
    def __init__(self, value: str | int | float) -> None:
        super().__init__()
        self._value = value

    def _get_sql(self, dialect: DialectProtocol) -> str:
        if isinstance(self._value, str):
            return f"'{self._value}'"
        return f'{self._value}'


class SqlType(BaseAliased):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{self._name}'


class Parameter(BaseAliased, ParameterProtocol):
    def __init__(self, value: str | int | float, fixed_name: bool = False) -> None:
        super().__init__()
        self._value = value
        self._fixed_name = fixed_name
        self._key = ''
        self._placeholder = ''

    def _get_sql(self, dialect: DialectProtocol) -> str:
        params = dialect.get_paramstyle()
        if self._fixed_name:
            if not params.was_param_added(self._key):
                key, placeholder = params.add_param(self._value)
                self._key = key
                self._placeholder = placeholder

            return self._placeholder

        _, placeholder = params.add_param(self._value)
        return placeholder


class Column(BaseAliased):
    def __init__(self, name: str) -> None:
        super().__init__()
        self._name = name

    def _get_sql(self, dialect: DialectProtocol) -> str:
        return f'{dialect.quote_ident(self._name)}'
