from david8.core.base_join import BaseJoin
from david8.protocols.dml import JoinProtocol


def left() -> JoinProtocol:
    return BaseJoin('LEFT')

def right() -> JoinProtocol:
    return BaseJoin('RIGHT')

def inner() -> JoinProtocol:
    return BaseJoin('INNER')
