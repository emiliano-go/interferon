Interferon
==========

Container-native immune signaling for Docker stacks.

Interferon is a Docker sidecar watcher plus Python SDK. The watcher observes Docker container lifecycle events, converts them into typed signals, and exposes them to application containers over transports such as HTTP SSE.

Read the blog post [here](https://blog.emiliano-go.com/works/interferon_project/)!

This repository is scaffolded for two publish targets:

- `interferon-sdk`: Python package for receptors and shared signal/transport code.
- `interferon`: Docker image running the watcher.
- `interferon-watchdog`: optional minimal sidecar for restarting a hung watcher.

Development
-----------

```bash
uv sync
uv run pytest
```

## How to test it
### Install deps
uv sync --dev

### Terminal 1: run the watcher
uv run python -m interferon.watcher.main

### Terminal 2: exercise containers
docker run --rm alpine echo hello    # → die + stop + destroy
docker run -d --name test nginx      # → create + start
docker kill test                     # → kill (exit_code 137)
docker rm test                       # → destroy
docker run --rm alpine sh -c "exit 1"  # → die (exit_code 1)

### Ctrl+C in Terminal 1 to see graceful shutdown
Expected output:
14:30:01 INFO __main__:Watcher started, waiting for Docker events...
14:30:01 INFO listener:Connected to Docker daemon
14:30:05 INFO __main__:Event: action=create container=foo image=alpine
14:30:05 INFO __main__:Event: action=start container=foo image=alpine
14:30:05 INFO __main__:Event: action=die container=foo image=alpine exit_code=0
14:30:05 INFO __main__:Event: action=stop container=foo image=alpine
14:30:05 INFO __main__:Event: action=destroy container=foo image=alpine