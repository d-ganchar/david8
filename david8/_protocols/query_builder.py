from dataclasses import dataclass
from typing import Protocol

from .._protocols.dml import SelectProtocol


@dataclass(slots=True)
class QueryBuilderProtocol(Protocol):
    def select(self, *args) -> SelectProtocol:
        pass
