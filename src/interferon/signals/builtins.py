"""Built-in Docker event to Interferon signal mappings."""

from interferon.signals.schema import SignalPriority


DOCKER_EVENT_MAP: dict[str, str] = {
    "oom": "oom_killed",
    "stop": "container_stopped",
    "restart": "container_restarted",
    "kill": "container_killed",
}

EXIT_CODE_SIGNALS: dict[int, str] = {
    0: "container_stopped",
    1: "container_error",
    78: "config_bad",
    137: "container_killed",
}

DEFAULT_PRIORITIES: dict[str, SignalPriority] = {
    "container_killed": SignalPriority.CRITICAL,
    "oom_killed": SignalPriority.CRITICAL,
    "db_down": SignalPriority.CRITICAL,
    "db_oom": SignalPriority.CRITICAL,
    "api_down": SignalPriority.CRITICAL,
    "config_bad": SignalPriority.CRITICAL,
    "db_degraded": SignalPriority.WARNING,
    "worker_down": SignalPriority.WARNING,
    "cache_down": SignalPriority.WARNING,
    "container_error": SignalPriority.WARNING,
    "db_recovering": SignalPriority.INFO,
    "db_healthy": SignalPriority.INFO,
    "container_stopped": SignalPriority.INFO,
    "container_restarted": SignalPriority.INFO,
    "heartbeat": SignalPriority.INFO,
}
