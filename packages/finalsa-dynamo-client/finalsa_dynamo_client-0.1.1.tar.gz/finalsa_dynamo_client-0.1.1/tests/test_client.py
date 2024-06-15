from finalsa.dynamo.client import (SyncDynamoClientTestImpl, __version__)
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))


def test_version():
    assert __version__ is not None


def test_dynamo_client_test_impl():
    client = SyncDynamoClientTestImpl()
    assert client is not None
    assert client.put is not None
    assert client.query is not None
    assert client.delete is not None
    assert client.scan is not None
    assert client.write_transaction is not None
    assert client.get is not None


def test_dynamo_client_put():
    client = SyncDynamoClientTestImpl()
    client.put("test", {"id": "1", "name": "test"})


def test_dynamo_client_query():
    client = SyncDynamoClientTestImpl()
    client.put("test", {"id": "1", "name": "test"})
    client.put("test", {"id": "2", "name": "test"})
    client.put("test", {"id": "3", "name": "test"})
    assert client.get("test", {"id": "1"}) is not None
    assert client.get("test", {"id": "2"}) is not None
    assert client.get("test", {"id": "3"}) is not None


def test_dynamo_client_delete():
    client = SyncDynamoClientTestImpl()
    client.put("test", {"id": "1", "name": "test"})
    client.put("test", {"id": "2", "name": "test"})
    client.put("test", {"id": "3", "name": "test"})
    assert client.get("test", {"id": "1"}) is not None
    assert client.get("test", {"id": "2"}) is not None
    assert client.get("test", {"id": "3"}) is not None
    client.delete("test", {"id": "1"})
    assert client.get("test", {"id": "1"}) is None


def test_dynamo_client_scan():
    client = SyncDynamoClientTestImpl()
    client.put("test", {"id": "a1", "name": "test"})
    client.put("test", {"id": "a2", "name": "test"})
    client.put("test", {"id": "b3", "name": "test"})
    assert client.scan("test", FilterExpression="begins_with(id,:id)", ExpressionAttributeValues={
        ":id": "a"
    }) is not None
    assert client.scan("test").get("Items") is not None
    assert len(client.scan("test",  FilterExpression="begins_with(id,:id)", ExpressionAttributeValues={
        ":id": "a"
    }).get("Items")) == 2

    assert len(client.scan("test",  FilterExpression="begins_with(id,:id)", ExpressionAttributeValues={
        ":id": {"S": "a"}
    }).get("Items")) == 2
    assert len(client.scan("test").get("Items")) == 3


def test_dynamo_client_write_transaction():
    client = SyncDynamoClientTestImpl()
    client.write_transaction(
        [{"Put": {"TableName": "test", "Item": {"id": "1", "name": "test"}}}])
    assert client.get("test", {"id": "1"}) is not None


def test_overwrite_client():
    client = SyncDynamoClientTestImpl()
    key = {"PK": "1", "SK": "1"}
    client.write_transaction(
        [{"Put": {"TableName": "test", "Item": {"name": "test", **key}}}])

    client.write_transaction(
        [{"Put": {"TableName": "test", "Item": {"name": "23123", **key}}}])

    assert client.get("test", key) is not None
    assert client.get("test", key).get("name") == "23123"


def test_multilple_writes_to_same_item():
    client = SyncDynamoClientTestImpl()
    key = {"PK": " 1", "SK": "1"}
    with pytest.raises(Exception):
        client.write_transaction(
            [{"Put": {"TableName": "test", "Item":
                      {"name": "test", **key}}},
             {"Put": {"TableName": "test", "Item": {"name": "23123", **key
                                                    }}},])
    assert client.get("test", key) is None
