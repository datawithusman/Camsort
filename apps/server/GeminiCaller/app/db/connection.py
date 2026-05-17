from __future__ import annotations

import os
from functools import lru_cache

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def get_database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    return database_url


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


def connect():
    return get_engine().connect()


def check_database_connection() -> dict:
    try:
        with connect() as conn:
            value = conn.execute(text("SELECT 1")).scalar_one()
        return {"status": "ok", "result": value}
    except Exception as exc:
        return {"status": "error", "error": str(exc)}
