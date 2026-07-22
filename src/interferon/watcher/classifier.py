"""Docker event to Signal classification scaffold."""

from typing import Any

from interferon.signals.builtins import DOCKER_EVENT_MAP, EXIT_CODE_SIGNALS


def classify_event(event: dict[str, Any]) -> str | None:
    action = event.get("Action") or event.get("status")
    if action == "die":
        attributes = event.get("Actor", {}).get("Attributes", {})
        exit_code = attributes.get("exitCode")
        return EXIT_CODE_SIGNALS.get(int(exit_code)) if exit_code is not None else None
    return DOCKER_EVENT_MAP.get(action)
