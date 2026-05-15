from __future__ import annotations

import os

import psycopg


def get_database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")

    return database_url


def connect():
    return psycopg.connect(get_database_url())
