from ..protocols.dialect import DialectProtocol
from ..protocols.sql import ExprProtocol


def to_col_or_expr(value: str | int | ExprProtocol, dialect: DialectProtocol) -> str:
    if isinstance(value, str):
        return dialect.quote_ident(value)
    if isinstance(value, int):
        return f'{value}'
    return value.get_sql(dialect)
