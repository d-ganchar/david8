from ..protocols.dialect import DialectProtocol
from ..protocols.sql import ExprProtocol


def to_col_or_expr(value: str | ExprProtocol, dialect: DialectProtocol) -> str:
    if isinstance(value, str):
        return dialect.quote_ident(value)
    return value.get_sql(dialect)
