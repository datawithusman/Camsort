from __future__ import annotations

import dataclasses
import datetime as dt
import decimal
from typing import Any

JsonObject = dict[str, Any]


def camel_case(name: str) -> str:
    parts = name.split("_")
    return parts[0] + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def to_jsonable(value: Any) -> Any:
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, (dt.datetime, dt.date)):
        text = value.isoformat()
        if isinstance(value, dt.datetime) and text.endswith("+00:00"):
            text = text[:-6] + "Z"
        return text
    if dataclasses.is_dataclass(value):
        return record_to_dict(value)
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, tuple):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {camel_case(str(k)): to_jsonable(v) for k, v in value.items()}
    return value


def raw_record_dict(record: Any) -> JsonObject:
    if record is None:
        return {}
    if dataclasses.is_dataclass(record):
        return dataclasses.asdict(record)
    if isinstance(record, dict):
        return dict(record)
    if hasattr(record, "_asdict"):
        return dict(record._asdict())

    raw: JsonObject = {}
    for key in dir(record):
        if key.startswith("_"):
            continue
        value = getattr(record, key)
        if callable(value):
            continue
        raw[key] = value
    return raw


def record_to_dict(record: Any) -> JsonObject:
    raw = raw_record_dict(record)
    return {camel_case(key): to_jsonable(value) for key, value in raw.items()}


def records_to_dicts(rows: Any) -> list[JsonObject]:
    return [record_to_dict(row) for row in rows]


def make_querier(module: Any, conn: Any) -> Any:
    if hasattr(module, "Querier"):
        return module.Querier(conn)
    if hasattr(module, "SyncQuerier"):
        return module.SyncQuerier(conn)
    raise RuntimeError(f"Generated DB module {module!r} does not expose Querier or SyncQuerier.")


def generated_method(querier: Any, name: str) -> Any:
    if not hasattr(querier, name):
        raise RuntimeError(f"Generated DB querier is missing method: {name}")
    return getattr(querier, name)
