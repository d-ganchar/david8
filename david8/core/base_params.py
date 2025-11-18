import dataclasses
from copy import deepcopy
from typing import Any

from ..protocols.dialect import ParamStyleProtocol


@dataclasses.dataclass(slots=True)
class BaseParams(ParamStyleProtocol):
    _params_bag: dict[str, Any] = dataclasses.field(default_factory=dict)

    def add_param(self, value: Any) -> tuple[str, str]:
        ix = str(len(self._params_bag) + 1)
        key = self._create_param_key(ix)
        self._params_bag[key] = value
        return key, self._render_param(ix)

    def reset_parameters(self):
        self._params_bag.clear()

    def get_parameters(self) -> dict[str, Any]:
        return deepcopy(self._params_bag)

    def get_list_parameters(self) -> list[Any]:
        return list(self._params_bag.values())

    def get_tuple_parameters(self) -> tuple:
        return tuple(self._params_bag.values())

    def _create_param_key(self, param_index: str) -> str:
        return param_index

    def _render_param(self, param_index: str) -> str:
        raise NotImplementedError

    def was_param_added(self, key: str) -> bool:
        return key in self._params_bag

    def get_param_by_key(self, key: str) -> int | str | float | None:
        return self._params_bag[key]
