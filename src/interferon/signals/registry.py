"""Signal Registry"""

from typing import Any

from interferon.signals.schema import Signal, SignalPriority


class SignalRegistry:
    """Pluggable signal clasification and creation. 
    Subclass to extend or override mappins or swap signal_cls
    """

    signal_cls : type[Signal] = Signal

    # Docker events -> signal name
    event_map : dict[str, str] = {
        "oom" : "oom_killed",
        "stop" : "container_stopped",
        "restart" : "container_restarted",
        "kill" : "container_killed"
    }

    # Exit code -> signal name (only for die action)
    exit_code_signals : dict[int, str] = {
        0 : "container_stopped",
        1 : "container_error",
        78 : "config_bad",
        137 : "container_killed"
    }

    # Signal name -> default priority
    default_priorities : dict[str, SignalPriority] = {
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

    # Role name -> {action, signal_name}
    role_signals = dict[str, dict[str, str]] = {
        "database": {"die": "db_down", "oom": "db_oom", "start": "db_recovering"},
        "api": {"die": "api_down", "oom": "api_oom", "start": "api_recovering"},
        "worker": {"die": "worker_down"},
        "cache": {"die": "cache_down"},
        "frontend": {"die": "frontend_down"},
    }

    def classify(
            self, 
            action : str, 
            exit_code : int | None, 
            labels : dict[str, str]
            ) -> tuple[str | None, str | None]:

        """Returns (signal_name, reason). Both None = drop
        1. Label override: interferon.signals.<action>
        2. Role signal: interferon.role` + role_signals
        3. Built-in: exit code → event_map → drop
        """

        signal_name = labels.get(f"interferon.signals.{action}")
        reason = labels.get(f"interferon.signals.{action}.reason")

        if signal_name:
            return signal_name, reason

        role = labels.get("interferon.role")

        if role and role in self.role_signals:
            role_entry = self.role_signals[role]

            if action in role_entry:
                return role_entry[action], None

        if action == "die" and exit_code is not None:
            name = self.exit_code_signals.get(exit_code)

            if name:
                return name, None

        name = self.event_map.get(action)

        if name:
            return name, None

        return None, None

    def default_priority(self, signal_name : str) -> SignalPriority:
        return self.default_priorities.get(signal_name, SignalPriority.WARNING)

    # Registration Helpers

    def register_role(self, name :  str, **action_map : str) -> None:
        self.role_signals[name] = action_map

    def register_priority(self, signal_name : str, priority : SignalPriority) -> None:
        self.default_priorities[signal_name] = priority

    def register_event_map(self, action : str, signal_name : str):
        self.event_map[action] = signal_name

    def register_exit_code(self, code : int, signal_name :  str) -> None:
        self.exit_code_signals[code] = signal_name

    # Signal creation

    def create_signal(
            self,
            *,
            signal_type : str,
            container : str,
            action : str = "",
            exit_code : int | None = None,
            image : str | None = None,
            labels : dict[str, str] | None = None,
            project_signature :  str | None = None,
            docker_event_id : str | None = None,
            reason : str | None = None,
            kwargs**      
    ) -> Signal:

        priority = kwargs.pop("priority", None) or self.default_priority(signal_type)

        return self.signal_cls.create(
            type=self.signal_type,
            container=container,
            priority=priority,
            exit_code=exit_code,
            image=image,
            container_labels=labels or {},
            project_signature=project_signature,
            docker_event_id=docker_event_id,
            reason=reason,
            **kwargs
            )
