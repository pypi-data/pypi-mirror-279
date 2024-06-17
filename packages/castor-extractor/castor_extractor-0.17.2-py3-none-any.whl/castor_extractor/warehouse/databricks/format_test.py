from datetime import datetime

from .format import (
    DatabricksFormatter,
    _column_payload,
    _table_payload,
    _to_datetime_or_none,
)


def test__to_datetime_or_none():
    time_ms = 1707734459947
    expected = datetime(2024, 2, 12, 10, 40, 59, 947000)

    assert _to_datetime_or_none(time_ms) == expected

    time_ms = None
    assert _to_datetime_or_none(time_ms) is None


def test_DatabricksFormatter__primary():
    emails = [
        {"type": "work", "value": "louis@evilcorp.com", "primary": False},
        {"type": "work", "value": "thomas@evilcorp.com", "primary": True},
    ]
    assert DatabricksFormatter._primary(emails) == "thomas@evilcorp.com"

    assert DatabricksFormatter._primary([]) is None


def test__table_payload():
    schema = {"id": "id123"}

    table = {
        "name": "baz",
        "catalog_name": "foo",
        "schema_name": "bar",
        "table_type": "MANAGED",
        "owner": "pot@ato.com",
        "table_id": "732pot5e-8ato-4c27-b701-9fa51febc192",
    }
    host = "https://some.cloud.databricks.net/"
    workspace_id = "123456"

    payload = _table_payload(schema, table, host, workspace_id)

    expected = {
        "description": None,
        "id": "732pot5e-8ato-4c27-b701-9fa51febc192",
        "owner_email": "pot@ato.com",
        "schema_id": "id123",
        "table_name": "baz",
        "tags": [],
        "type": "MANAGED",
        "url": "https://some.cloud.databricks.net/explore/data/foo/bar/baz?o=123456",
    }
    assert payload == expected


def test__column_payload():
    table = {
        "id": "18175cd5-9b9b-4d78-9d28-caaa12c21ce0",
        "schema_id": "dv_microservices.company_silver",
        "table_name": "companyrepository_organization_v1",
        "description": "some description",
        "tags": [],
        "type": "TABLE",
    }
    column = {
        "name": "Uid",
        "type_text": "string",
        "type_name": "STRING",
        "position": 0,
        "type_precision": 0,
        "type_scale": 0,
        "type_json": '{"name":"Uid","type":"string","nullable":true,"metadata":{}}',
        "nullable": True,
        "comment": "some description",
    }
    payload = _column_payload(table, column)

    expected = {
        "id": "`18175cd5-9b9b-4d78-9d28-caaa12c21ce0`.`Uid`",
        "column_name": "Uid",
        "table_id": "18175cd5-9b9b-4d78-9d28-caaa12c21ce0",
        "description": "some description",
        "data_type": "STRING",
        "ordinal_position": 0,
    }
    assert payload == expected

    # case where there are spaces in the name
    column["name"] = "column name with spaces"
    payload = _column_payload(table, column)
    expected_id = (
        "`18175cd5-9b9b-4d78-9d28-caaa12c21ce0`.`column name with spaces`"
    )
    assert payload["id"] == expected_id
