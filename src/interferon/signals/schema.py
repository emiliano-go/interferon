"""Signal schema and JSON validation helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
import time
from typing import Any


class SignalPriority(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass(slots=True)
class Signal:
    type: str
    container: str
    timestamp: float
    priority: SignalPriority = SignalPriority.WARNING
    reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    ttl: float | None = None
    expires_at: float | None = None
    exit_code: int | None = None
    image: str | None = None
    docker_event_id: str | None = None
    project_signature: str | None = None
    container_labels: dict[str, str] = field(default_factory=dict)

    @classmethod
    def create(cls, **kwargs: Any) -> "Signal":
        kwargs.setdefault("timestamp", time.time())
        if isinstance(kwargs.get("priority"), str):
            kwargs["priority"] = SignalPriority(kwargs["priority"])
        ttl = kwargs.get("ttl")
        if ttl is not None and kwargs.get("expires_at") is None:
            kwargs["expires_at"] = kwargs["timestamp"] + float(ttl)
        signal = cls(**kwargs)
        signal.validate()
        return signal

    def validate(self) -> None:
        if not self.type:
            raise ValueError("signal type is required")
        if not self.container:
            raise ValueError("signal container is required")
        if self.ttl is not None and self.ttl <= 0:
            raise ValueError("signal ttl must be positive")

    def is_expired(self, now: float | None = None) -> bool:
        return self.expires_at is not None and self.expires_at < (now or time.time())

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["priority"] = self.priority.value
        return data
