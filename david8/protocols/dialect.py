from typing import Protocol


class ParamStyleProtocol(Protocol):
    def add_param(self, value: int | str | float | None) -> tuple[str, str]:
        pass

    def get_parameters(self) -> dict | list | tuple:
        pass

    def reset_parameters(self):
        pass

    def was_param_added(self, key: str) -> bool:
        pass

    def get_param_by_key(self, key: str) -> int | str | float | None:
        pass


class DialectProtocol(Protocol):
    def quote_ident(self, name: str) -> str:
        pass

    def get_paramstyle(self) -> ParamStyleProtocol:
        pass

    def is_quote_mode(self) -> bool:
        pass
