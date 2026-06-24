from .core.sql_92_join import Sql92Join as _Sql92Join
from .core.sql_1999_join import LiteralJoin as _LiteralJoin
from .protocols.sql import LiteralJoinProtocol as _LiteralJoinProtocol
from .protocols.sql import Sql92JoinProtocol as _Sql92JoinProtocol


def left() -> _Sql92JoinProtocol:
    return _Sql92Join(join_type='LEFT JOIN')

def right() -> _Sql92JoinProtocol:
    return _Sql92Join(join_type='RIGHT JOIN')

def inner() -> _Sql92JoinProtocol:
    return _Sql92Join(join_type='INNER JOIN')

def lateral() -> _LiteralJoinProtocol:
    return _LiteralJoin()
