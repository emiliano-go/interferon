"""In-memory last-known-state cache for receptors."""

from typing import Any


class StateCache:
    def __init__(self) -> None:
        self._states: dict[str, dict[str, Any]] = {}

    def update(self, container: str, state: dict[str, Any]) -> None:
        self._states[container] = state

    def get(self, container: str) -> dict[str, Any] | None:
        return self._states.get(container)

    def all(self) -> dict[str, dict[str, Any]]:
        return dict(self._states)
