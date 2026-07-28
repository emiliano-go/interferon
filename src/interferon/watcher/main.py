"""Watcher entrypoint"""

import asyncio
import signal


from interferon.log import get_logger, setup_logging
from interferon.watcher.listener import DockerListener

setup_logging()
logger = get_logger(__name__)


async def handle_event(event : dict) -> None:
    action = event.get("Action") or event.get("status", "?")
    container_id = event.get("ID", "?")
    actor = event.get("Actor", {})
    attrs = actor.get("Attributes", "?")
    image = attrs.get("image", "?")
    exit_code = attrs.get("exitCode")
    name = attrs.get("name", container_id[:12])

    parts = [f"action={action}", f"container={name}", f"image={image}"]

    if exit_code is not None:
        parts.append(f"exit_code={exit_code}")

    logger.info("Event: %s", " ".join(parts))

async def main() -> None:

    listener = DockerListener(handle_event)
    listener_task = asyncio.create_task(listener.start())

    loop = asyncio.get_running_loop()
    stop = asyncio.Event()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop.set)

    logger.info("Watcher started, waiting for Docker events...")
    await stop.wait()

    logger.info("Shutting down...")
    await listener.stop()
    listener_task.cancel()

    try:
        await listener_task

    except asyncio.CancelledError:
        pass

if __name__ == "__main__":
    asyncio.run(main())