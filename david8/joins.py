from david8.core.base_join import BaseJoin as _BaseJoin
from david8.protocols.dml import JoinProtocol


def left() -> JoinProtocol:
    return _BaseJoin('LEFT JOIN')

def right() -> JoinProtocol:
    return _BaseJoin('RIGHT JOIN')

def inner() -> JoinProtocol:
    return _BaseJoin('INNER JOIN')
