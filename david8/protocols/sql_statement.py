from typing import Protocol, Union

from david8.protocols.dialect import DialectProtocol


class SqlStatementProtocol(Protocol):
    def get_sql(self) -> str:
        pass

    def get_parameters(self) -> Union[list, dict]:
        pass


class PredicateProtocol(SqlStatementProtocol):
    def set_dialect(self, dialect: DialectProtocol):
        pass
