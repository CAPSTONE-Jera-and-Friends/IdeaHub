from __future__ import annotations

from pathlib import Path

from sqlalchemy import create_engine, text

from config import Config


def run() -> None:
    sql_path = Path(__file__).with_name("add_indexes.sql")
    sql_statements = [
        line.strip()
        for line in sql_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("--")
    ]
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.begin() as conn:
        for statement in sql_statements:
            conn.execute(text(statement))
    print("Index migration complete.")


if __name__ == "__main__":
    run()
