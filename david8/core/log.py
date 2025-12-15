import functools
import logging
from collections.abc import Callable

from ..protocols.dialect import DialectProtocol
from ..protocols.sql import QueryProtocol

log = logging.getLogger('david8')

def log_and_reset(func: Callable) -> Callable:
    """
    Recalculate parameters when subqueries and log final sql query with parameters
    """
    @functools.wraps(func)
    def wrapper(self: QueryProtocol, dialect: DialectProtocol = None):
        if dialect is None:
            self.get_dialect().get_paramstyle().reset_parameters()
            log_query = True
        else:
            log_query = False

        sql = func(self, dialect)
        if log_query:
            log.info('%s\n%s', sql, self.get_parameters())

        return sql
    return wrapper
