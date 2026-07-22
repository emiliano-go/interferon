"""Per-container state machine scaffold."""

from enum import Enum


class ContainerState(str, Enum):
    UNKNOWN = "UNKNOWN"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    RECOVERING = "RECOVERING"
    STOPPED = "STOPPED"
