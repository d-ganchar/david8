from .core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from .protocols.dialect import DialectProtocol
from .protocols.query_builder import QueryBuilderProtocol


def get_qb(dialect: DialectProtocol) -> QueryBuilderProtocol:
    return _BaseQueryBuilder(dialect)
