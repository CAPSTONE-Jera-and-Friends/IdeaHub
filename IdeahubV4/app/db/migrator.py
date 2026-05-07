from __future__ import annotations

from sqlalchemy import text


class SchemaMigrator:
    """Runs ALTER TABLE statements in an idempotent way."""

    def __init__(self, db, app) -> None:
        self._db = db
        self._app = app

    def run(self) -> None:
        db = self._db
        db.create_all()
        checks = [
            (
                "orders",
                "status",
                "ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'preparing'",
            ),
            (
                "order_items",
                "status",
                "ALTER TABLE order_items ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'preparing'",
            ),
            ("space_types", "capacity", "ALTER TABLE space_types ADD COLUMN capacity INT NULL"),
            (
                "users",
                "job_role",
                "ALTER TABLE users ADD COLUMN job_role VARCHAR(50) NOT NULL DEFAULT 'general'",
            ),
            ("orders", "handled_by", "ALTER TABLE orders ADD COLUMN handled_by INT NULL"),
            (
                "customer_sessions",
                "number_of_people",
                "ALTER TABLE customer_sessions ADD COLUMN number_of_people INT NOT NULL DEFAULT 1",
            ),
            ("boardroom_bookings", "session_id", "ALTER TABLE boardroom_bookings ADD COLUMN session_id INT NULL"),
            ("boardroom_bookings", "started_at", "ALTER TABLE boardroom_bookings ADD COLUMN started_at DATETIME NULL"),
            (
                "boardroom_bookings",
                "expected_end_at",
                "ALTER TABLE boardroom_bookings ADD COLUMN expected_end_at DATETIME NULL",
            ),
            ("boardroom_bookings", "ended_at", "ALTER TABLE boardroom_bookings ADD COLUMN ended_at DATETIME NULL"),
            (
                "boardroom_bookings",
                "extended_minutes",
                "ALTER TABLE boardroom_bookings ADD COLUMN extended_minutes INT NOT NULL DEFAULT 0",
            ),
            ("boardroom_bookings", "course", "ALTER TABLE boardroom_bookings ADD COLUMN course VARCHAR(100) NULL"),
        ]
        for table_name, column_name, ddl in checks:
            has_col = db.session.execute(
                text(
                    """
                SELECT COLUMN_NAME
                FROM information_schema.COLUMNS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = :table_name
                AND COLUMN_NAME = :column_name
            """
                ),
                {"table_name": table_name, "column_name": column_name},
            ).fetchall()
            if has_col:
                continue
            try:
                db.session.execute(text(ddl))
                db.session.commit()
            except Exception:
                db.session.rollback()
