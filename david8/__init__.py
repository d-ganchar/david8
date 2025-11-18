from .core.base_dialect import BaseDialect as _BaseDialect
from .core.base_query_builder import BaseQueryBuilder as _BaseQueryBuilder
from .param_styles import PyFormatParamStyle
from .protocols.dialect import ParamStyleProtocol
from .protocols.query_builder import QueryBuilderProtocol


def get_default_qb(param_style: ParamStyleProtocol = None, is_quote_mode: bool = False) -> QueryBuilderProtocol:
    dialect = _BaseDialect(param_style or PyFormatParamStyle(), is_quote_mode)
    return _BaseQueryBuilder(dialect)
