from .core.sql_92_join import Sql92Join as _Sql92Join
from .protocols.sql import Sql92JoinProtocol


def left() -> Sql92JoinProtocol:
    return _Sql92Join(join_type='LEFT JOIN')

def right() -> Sql92JoinProtocol:
    return _Sql92Join(join_type='RIGHT JOIN')

def inner() -> Sql92JoinProtocol:
    return _Sql92Join(join_type='INNER JOIN')
