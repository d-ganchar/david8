import dataclasses
from typing import Union

from ..protocols.sql_statement import ColumnProtocol, SqlStatementProtocol


class _IsNullExpression(SqlStatementProtocol):
    def to_sql(self) -> tuple[str, list]:
        return 'IS NULL', []


class _IsNotNullExpression(SqlStatementProtocol):
    def to_sql(self) -> tuple[str, list]:
        return 'IS NOT NULL', []


@dataclasses.dataclass(slots=True)
class WhereCondition(ColumnProtocol):
    _left_expression: str | SqlStatementProtocol
    _right_expression: int | float | str | SqlStatementProtocol
    _parameters: list
    _operator: str

    def __init__(
        self,
        left_expression: str | SqlStatementProtocol,
        right_expression: int | float | str | SqlStatementProtocol,
        operator: str = '',
    ):
        self._left_expression = left_expression
        self._right_expression = right_expression
        self._operator = operator


    @classmethod
    def eq(cls, left_expression: str | SqlStatementProtocol,
           right_expression: int | float | str | SqlStatementProtocol):
        return WhereCondition(left_expression, right_expression, '=')

    @classmethod
    def is_null(cls, expression: Union[str, 'SqlStatementProtocol'])-> SqlStatementProtocol:
        return WhereCondition(expression, _IsNullExpression())

    @classmethod
    def is_not_null(cls, expression: Union[str, 'SqlStatementProtocol'])-> SqlStatementProtocol:
        return WhereCondition(expression, _IsNotNullExpression())

    @classmethod
    def gt(cls, left_expression: str | SqlStatementProtocol,
           right_expression: Union[int, float, str, 'SqlStatementProtocol'])-> SqlStatementProtocol:
        return WhereCondition(left_expression, right_expression, '>')

    @classmethod
    def lt(cls, left_expression: str | SqlStatementProtocol,
           right_expression: Union[int, float, str, 'SqlStatementProtocol'])-> SqlStatementProtocol:
        return WhereCondition(left_expression, right_expression, '<')

    @classmethod
    def position_param_char(cls) -> str:
        return '?'

    def to_sql(self) -> tuple[str, list]:
        parameters = []

        if isinstance(self._left_expression, str):
            left_expression = self._left_expression
        else:
            left_expression, left_params = self._left_expression.to_sql()
            parameters.extend(left_params)

        if isinstance(self._right_expression, (str, float, int)):
            right_expression = self.position_param_char()
            parameters.append(self._right_expression)
        else:
            right_expression, right_params = self._right_expression.to_sql()
            parameters.extend(right_params)

        operator = f' {self._operator} ' if self._operator else ' '
        sql = f'{left_expression}{operator}{right_expression}'

        return sql, parameters
