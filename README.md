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
