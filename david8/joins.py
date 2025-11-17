from david8.core.base_join import BaseJoin
from david8.protocols.dml import JoinProtocol


def left() -> JoinProtocol:
    return BaseJoin('LEFT JOIN')

def right() -> JoinProtocol:
    return BaseJoin('RIGHT JOIN')

def inner() -> JoinProtocol:
    return BaseJoin('INNER JOIN')
