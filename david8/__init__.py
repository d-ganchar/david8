from ._base_query_builder import BaseQueryBuilder
from .protocols.dialect import DialectProtocol
from .protocols.query_builder import QueryBuilderProtocol


def get_qb(dialect: DialectProtocol) -> QueryBuilderProtocol:
    return BaseQueryBuilder(dialect)
