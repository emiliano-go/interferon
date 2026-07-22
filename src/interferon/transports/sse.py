"""SSE transport placeholders."""

from collections.abc import AsyncIterator

from interferon.signals.schema import Signal


async def connect_sse(*, host: str, port: int, path: str = "/signals") -> AsyncIterator[Signal]:
    """Connect to an SSE stream.

    The concrete HTTP implementation is intentionally deferred until the watcher
    server and zero-dependency client behavior are implemented together.
    """
    raise NotImplementedError("SSE client transport is not implemented yet")
    yield  # pragma: no cover
