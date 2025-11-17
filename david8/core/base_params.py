import dataclasses
from typing import Any

from ..protocols.dialect import ParamStyleProtocol


@dataclasses.dataclass(slots=True)
class BaseParams(ParamStyleProtocol):
    _params_bag: dict[str, Any] = dataclasses.field(default_factory=dict)

    def add_param(self, value: Any) -> tuple[str, str]:
        key = str(len(self._params_bag) + 1)
        self._params_bag[key] = value
        return key, self._render_param(key)

    def reset_parameters(self):
        self._params_bag.clear()

    def get_parameters(self):
        return self._params_bag

    def _render_param(self, key: str) -> str:
        raise NotImplementedError

    def was_param_added(self, key: str) -> bool:
        return key in self._params_bag

    def get_param_by_key(self, key: str) -> int | str | float | None:
        return self._params_bag[key]
