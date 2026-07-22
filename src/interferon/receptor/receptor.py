"""Async SDK receptor scaffold."""

from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from interferon.receptor.state_cache import StateCache
from interferon.signals.schema import Signal

SignalHandler = Callable[[Signal], Awaitable[None]]


@dataclass(frozen=True, slots=True)
class HandlerRegistration:
    pattern: str
    handler: SignalHandler
    reason: str | None = None
    priority: str | None = None


class Receptor:
    def __init__(
        self,
        *,
        host: str = "interferon",
        port: int = 8765,
        transport: str = "sse",
        project_id: str | None = None,
        auth_token: str | None = None,
        failure_mode: str = "freeze",
        prime_on_connect: bool = True,
        discard_expired: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.transport = transport
        self.project_id = project_id
        self.auth_token = auth_token
        self.failure_mode = failure_mode
        self.prime_on_connect = prime_on_connect
        self.discard_expired = discard_expired
        self.cache = StateCache()
        self.handlers: list[HandlerRegistration] = []

    def on(
        self,
        pattern: str = "*",
        *,
        reason: str | None = None,
        priority: str | None = None,
    ) -> Callable[[SignalHandler], SignalHandler]:
        def decorator(handler: SignalHandler) -> SignalHandler:
            self.handlers.append(HandlerRegistration(pattern, handler, reason, priority))
            return handler

        return decorator

    async def start(self) -> None:
        raise NotImplementedError("Async receptor transport loop is not implemented yet")

    async def fetch_state(self) -> dict:
        raise NotImplementedError("State priming is not implemented yet")

    def state(self, container: str) -> dict | None:
        return self.cache.get(container)

    def all_states(self) -> dict:
        return self.cache.all()
