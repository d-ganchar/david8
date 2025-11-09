from typing import Protocol


class SqlStatementProtocol(Protocol):
    def to_sql(self) -> tuple[str, list]:
        """
        Returns SQL statement with list of SQL parameters
        """
