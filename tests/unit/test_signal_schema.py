from interferon.signals.schema import Signal, SignalPriority


def test_signal_create_sets_expiry_from_ttl() -> None:
    signal = Signal.create(type="db_degraded", container="db", timestamp=10.0, ttl=5.0)

    assert signal.priority == SignalPriority.WARNING
    assert signal.expires_at == 15.0


def test_signal_to_dict_serializes_priority_value() -> None:
    signal = Signal.create(type="heartbeat", container="__interferon__", priority="info")

    assert signal.to_dict()["priority"] == "info"
