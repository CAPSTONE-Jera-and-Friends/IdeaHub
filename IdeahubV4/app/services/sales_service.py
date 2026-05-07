from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

from app.core.interfaces import Clock
from app.repositories.sales_repository import SalesRepository


@dataclass(frozen=True)
class SalesService:
    repo: SalesRepository
    clock: Clock

    @staticmethod
    def _shape(summary_row: Any) -> dict[str, Any]:
        return {
            "transactions": int(summary_row.transactions or 0),
            "total_revenue": float(summary_row.total_revenue or 0),
            "space_revenue": float(summary_row.space_revenue or 0),
            "food_revenue": float(summary_row.food_revenue or 0),
        }

    def daily_sales(self) -> dict[str, Any]:
        today = self.clock.now().date()
        return {"date": str(today), **self._shape(self.repo.summary_for_day(today))}

    def sales_summary(self, period: str) -> dict[str, Any]:
        today = self.clock.now().date()
        if period == "yesterday":
            start_date = today - timedelta(days=1)
            end_date = start_date
        elif period == "7days":
            start_date = today - timedelta(days=6)
            end_date = today
        elif period == "1month":
            start_date = today - timedelta(days=29)
            end_date = today
        else:
            period = "today"
            start_date = today
            end_date = today
        return {
            "period": period,
            "start_date": str(start_date),
            "end_date": str(end_date),
            **self._shape(self.repo.summary_for_range(start_date, end_date)),
        }

    def sales_compare(self) -> dict[str, Any]:
        today = self.clock.now().date()
        yesterday = today - timedelta(days=1)
        return {
            "today": self._shape(self.repo.summary_for_day(today)),
            "yesterday": self._shape(self.repo.summary_for_day(yesterday)),
            "last_7_days": self._shape(self.repo.summary_for_range(today - timedelta(days=6), today)),
            "last_30_days": self._shape(self.repo.summary_for_range(today - timedelta(days=29), today)),
        }
