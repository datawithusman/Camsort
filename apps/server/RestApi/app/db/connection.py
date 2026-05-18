from __future__ import annotations
import os
from functools import lru_cache
from decimal import Decimal
from datetime import date, datetime
from typing import Any
from sqlalchemy import create_engine, text


def get_database_url() -> str:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set")
    return url.replace("postgresql://", "postgresql+psycopg://", 1) if url.startswith("postgresql://") else url

@lru_cache(maxsize=1)
def get_engine():
    return create_engine(get_database_url(), pool_pre_ping=True)

def connect():
    return get_engine().connect()

def camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p[:1].upper() + p[1:] for p in parts[1:])

def j(v: Any) -> Any:
    if isinstance(v, Decimal): return float(v)
    if isinstance(v, datetime): return v.isoformat().replace("+00:00", "Z")
    if isinstance(v, date): return v.isoformat()
    return v

def row_to_dict(row):
    return None if row is None else {camel(k): j(v) for k,v in dict(row._mapping).items()}

def rows_to_dicts(rows):
    return [row_to_dict(r) for r in rows]

def check_database_connection():
    try:
        with connect() as c:
            return {"status":"ok", "result": c.execute(text("SELECT 1")).scalar_one()}
    except Exception as e:
        return {"status":"error", "error": str(e)}
