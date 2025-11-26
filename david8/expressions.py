from david8.core.base_aliased import Column as _Column
from david8.core.base_aliased import Parameter as _Parameter
from david8.core.base_aliased import SqlType as _SqlType
from david8.core.base_aliased import Value as _Value
from david8.protocols.sql import AliasedProtocol, ValueProtocol


def val(value: str | int | float) -> ValueProtocol:
    return _Value(value)

def col(name: str) -> _Column:
    return _Column(name)

def param(value: str | int | float, fixed_name: bool = False) -> _Parameter:
    return _Parameter(value, fixed_name)

def true() -> AliasedProtocol:
    return _SqlType('TRUE')

def false() -> AliasedProtocol:
    return _SqlType('FALSE')

def null() -> AliasedProtocol:
    return _SqlType('NULL')
