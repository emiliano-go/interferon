"""State store backend scaffold."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class StateRow:
    container_id: str
    container_name: str
    project_signature: str
    state: str
    origin: str
    service: str | None = None
    reason: str | None = None
    last_signal: str | None = None
    since: float = 0.0
    updated_at: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class MemoryStateStore:
    def __init__(self) -> None:
        self._rows: dict[str, StateRow] = {}

    def load_all(self) -> list[StateRow]:
        return list(self._rows.values())

    def upsert(self, row: StateRow) -> None:
        self._rows[row.container_id] = row

    def delete(self, container_id: str) -> None:
        self._rows.pop(container_id, None)
