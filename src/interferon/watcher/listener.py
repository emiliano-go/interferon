"""Docker socket event stream with async + exponential backoff."""

import asyncio
from collections.abc import Callable, Awaitable
from typing import Any
import aiodocker

from interferon.log import get_logger

logger = get_logger(__name__)

class DockerListener:
    """Streams container events from docker daemon.
    Calls callback(event_dict) for each event. Reconnects
    with exponential backoff on stream drops.
    """

    def __init__(
            self,
            callback : Callable[[dict[str, Any]], Awaitable[None]],
            *,
            backoff_base: float = 1.0,
            backfoff_max : float = 60.0,
    ) -> None:

        self.callback = callback
        self.backoff_base = backoff_base
        self.backoff_max = backfoff_max
        self._client : aiodocker.Docker | None = None
        self._stopped = False

    async def start(self) -> None:
        """Connect to Docker and stream events untill stopped"""

        self._stopped = False
        attempt = 0

        while not self._stopped:
            try:
                self._client = aiodocker.Docker()
                logger.info("Connected to Docker daemon")

                sub = self._client.events.subscribe(filters = {"type" : ["container"]})
                while True:
                    event = await sub.get()
                    if event is None:
                        break
                    if self._stopped:
                        break

                    try:
                        await self.callback(event)

                    except Exception:
                        logger.exception("Uncaught error in event callback")

                    attempt = 0

            except asyncio.CancelledError:
                logger.info("Listener cancelled")
                break

            except Exception:
                attempt += 1
                delay = min(self.backoff_base * 2 ** (attempt - 1), self.backoff_max)
                logger.warning(f"Docker connection lost, reconnecting in {delay}s, attempt {attempt}")
                await asyncio.sleep(delay)

            finally:
                if self._client:
                    await self._client.close()
                    self._client = None

    async def stop(self) -> None:
        """Signal the listener to disconnect on the next iteration"""
        self._stopped = True
        if self._client:
            await self._client.close()