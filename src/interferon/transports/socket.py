"""Optional Unix socket transport placeholder."""


class SocketTransport:
    def __init__(self, socket_path: str) -> None:
        self.socket_path = socket_path

    async def publish(self, payload: dict) -> None:
        raise NotImplementedError("Unix socket transport is not implemented yet")
