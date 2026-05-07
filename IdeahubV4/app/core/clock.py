from __future__ import annotations

from datetime import datetime

from app.core.interfaces import Clock


class SystemClock(Clock):
    """Default clock implementation used across services."""

    def now(self) -> datetime:
        return datetime.utcnow()

    def utcnow(self) -> datetime:
        # Backward-compat helper for existing call sites.
        return self.now()

