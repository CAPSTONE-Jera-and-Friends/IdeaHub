from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class Clock(ABC):
    @abstractmethod
    def now(self) -> datetime:
        raise NotImplementedError


class Notifier(ABC):
    @abstractmethod
    def session_checked_out(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def order_status_changed(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def booking_updated(self, payload: dict[str, Any]) -> None:
        raise NotImplementedError
