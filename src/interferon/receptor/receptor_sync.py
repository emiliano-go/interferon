"""Sync SDK receptor scaffold."""

from collections.abc import Callable
from dataclasses import dataclass

from interferon.receptor.state_cache import StateCache
from interferon.signals.schema import Signal

SignalHandler = Callable[[Signal], None]


@dataclass(frozen=True, slots=True)
class SyncHandlerRegistration:
    pattern: str
    handler: SignalHandler
    reason: str | None = None
    priority: str | None = None


class SyncReceptor:
    def __init__(self, *, host: str = "interferon", port: int = 8765, transport: str = "sse", failure_mode: str = "freeze") -> None:
        self.host = host
        self.port = port
        self.transport = transport
        self.failure_mode = failure_mode
        self.cache = StateCache()
        self.handlers: list[SyncHandlerRegistration] = []

    def on(
        self,
        pattern: str = "*",
        *,
        reason: str | None = None,
        priority: str | None = None,
    ) -> Callable[[SignalHandler], SignalHandler]:
        def decorator(handler: SignalHandler) -> SignalHandler:
            self.handlers.append(SyncHandlerRegistration(pattern, handler, reason, priority))
            return handler

        return decorator

    def start(self) -> None:
        raise NotImplementedError("Sync receptor transport loop is not implemented yet")

    def state(self, container: str) -> dict | None:
        return self.cache.get(container)

    def all_states(self) -> dict:
        return self.cache.all()
