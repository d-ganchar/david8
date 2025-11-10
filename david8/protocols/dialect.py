from typing import Protocol


class ParamStyleProtocol(Protocol):
    def add_param(self, value: int | str | float | None) -> str:
        pass

    def get_parameters(self) -> dict | list | tuple:
        pass

    def reset_parameters(self):
        pass


class DialectProtocol(Protocol):
    def quote_ident(self, name: str) -> str:
        pass

    def get_paramstyle(self) -> ParamStyleProtocol:
        pass
