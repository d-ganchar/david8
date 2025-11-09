from typing import Protocol, Union


class SqlStatementProtocol(Protocol):
    def to_sql(self) -> tuple[str, list]:
        """
        Returns SQL statement with list of positioned parameters
        """


class ColumnProtocol(SqlStatementProtocol):
    """
    Conditions calculated in memory: WHERE price + X > 100
    """

    @classmethod
    def eq(
        cls,
        left_expression: Union[str, 'SqlStatementProtocol'],
        right_expression: Union[int, float, str, 'SqlStatementProtocol'],
    )  -> SqlStatementProtocol:
        pass

    @classmethod
    def is_null(cls, expression: Union[str, 'SqlStatementProtocol'])  -> SqlStatementProtocol:
        pass

    @classmethod
    def is_not_null(cls, expression: Union[str, 'SqlStatementProtocol']) -> SqlStatementProtocol:
        pass

    @classmethod
    def gt(
        cls,
        left_expression: Union[str, 'SqlStatementProtocol'],
        right_expression: Union[int, float, str, 'SqlStatementProtocol'],
    ) -> SqlStatementProtocol:
        pass

    @classmethod
    def lt(
        cls,
        left_expression: Union[str, 'SqlStatementProtocol'],
        right_expression: Union[int, float, str, 'SqlStatementProtocol'],
    ) -> SqlStatementProtocol:
        pass


class SelectColumnProtocol(SqlStatementProtocol):
    """
    Columns calculated in memory: SELECT (price - X) AS new_price
    """

    def as_(self, alias: str):
        pass

    def eq(self, value: Union[int, float, str, 'SqlStatementProtocol']) -> 'SelectColumnProtocol':
        pass

    def is_null(self) -> 'SelectColumnProtocol':
        pass

    def is_not_null(self) -> 'SelectColumnProtocol':
        pass

    def gt(self, value: Union[int, float, 'SqlStatementProtocol']) -> 'SelectColumnProtocol':
        pass

    def lt(self, value: Union[int, float, 'SqlStatementProtocol']) -> 'SelectColumnProtocol':
        pass
