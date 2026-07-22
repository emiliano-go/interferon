FROM python:3.13-slim

WORKDIR /app

COPY . .
ENV PYTHONPATH=/app/src

EXPOSE 8765
CMD ["python", "-m", "interferon.watcher.main"]
