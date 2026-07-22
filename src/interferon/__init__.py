"""Public SDK surface for Interferon receptors and signal emission."""

from interferon.receptor.receptor import Receptor
from interferon.receptor.receptor_sync import SyncReceptor
from interferon.signals.schema import Signal, SignalPriority


async def emit(
    signal_type: str,
    *,
    priority: SignalPriority | str = SignalPriority.WARNING,
    reason: str | None = None,
    metadata: dict | None = None,
    ttl: float | None = None,
) -> Signal:
    """Build and validate a programmatic signal.

    Transport delivery is intentionally left for the concrete transport clients.
    """
    return Signal.create(
        type=signal_type,
        container="__programmatic__",
        priority=priority,
        reason=reason,
        metadata=metadata or {},
        ttl=ttl,
    )


__all__ = ["Receptor", "Signal", "SignalPriority", "SyncReceptor", "emit"]
