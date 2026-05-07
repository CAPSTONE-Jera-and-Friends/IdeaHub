from __future__ import annotations

import os

from app import socketio
from app.core.notifiers import NoopNotifier, SocketIONotifier


def get_notifier():
    """Return serverless-safe notifier on Vercel, socket notifier otherwise."""
    if os.environ.get("VERCEL"):
        return NoopNotifier()
    return SocketIONotifier(socketio=socketio)
