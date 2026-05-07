"""Compatibility proxy for SQLAlchemy object when `app.db` package is imported."""

from __future__ import annotations

import importlib


def __getattr__(name: str):
    app_pkg = importlib.import_module("app")
    sql_db = app_pkg.__dict__.get("_sqlalchemy_db")
    if sql_db is None:
        raise AttributeError(name)
    return getattr(sql_db, name)
