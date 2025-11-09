from ._base_query_builder import BaseQueryBuilder
from ._protocols.query_builder import QueryBuilderProtocol


def get_qb() -> QueryBuilderProtocol:
    return BaseQueryBuilder()
