"""Role-aware signal mapping."""

ROLE_SIGNALS: dict[str, dict[str, str]] = {
    "database": {"die": "db_down", "oom": "db_oom", "start": "db_recovering"},
    "api": {"die": "api_down", "oom": "api_oom", "start": "api_recovering"},
    "worker": {"die": "worker_down"},
    "cache": {"die": "cache_down"},
    "frontend": {"die": "frontend_down"},
}
