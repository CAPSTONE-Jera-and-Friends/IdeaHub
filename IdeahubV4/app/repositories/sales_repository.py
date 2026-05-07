from __future__ import annotations

from datetime import date

from sqlalchemy import func

from app.models import Transaction


class SalesRepository:
    def summary_for_range(self, start_date: date, end_date: date):
        return (
            Transaction.query.with_entities(
                func.count(Transaction.id).label("transactions"),
                func.coalesce(func.sum(Transaction.total_bill), 0).label("total_revenue"),
                func.coalesce(func.sum(Transaction.time_bill), 0).label("space_revenue"),
                func.coalesce(func.sum(Transaction.food_bill), 0).label("food_revenue"),
            )
            .filter(func.date(Transaction.created_at) >= start_date)
            .filter(func.date(Transaction.created_at) <= end_date)
            .first()
        )

    def summary_for_day(self, target_date: date):
        return self.summary_for_range(target_date, target_date)
