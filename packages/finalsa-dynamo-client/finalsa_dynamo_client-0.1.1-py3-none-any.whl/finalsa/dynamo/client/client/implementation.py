import boto3
from finalsa.dynamo.client.interface import SyncDynamoClient
from typing import List, Dict


class DynamoClientImpl(SyncDynamoClient):

    def __init__(self):
        self.client = boto3.client("dynamodb")

    def write_transaction(self, transactions: List):
        self.client.transact_write_items(TransactItems=transactions)

    def query(self, TableName: str, **kwargs):
        return self.client.query(TableName=TableName, **kwargs)

    def put(self, TableName: str, item: Dict):
        self.client.put_item(TableName=TableName, Item=item)

    def get(self, TableName: str, key: Dict):
        return self.client.get_item(TableName=TableName, Key=key)

    def delete(self, TableName: str, key: Dict):
        self.client.delete_item(TableName=TableName, Key=key)

    def scan(self, TableName: str, **kwargs):
        return self.client.scan(TableName=TableName, **kwargs)

    def update(self, TableName: str, key: Dict, item: Dict):
        self.client.update_item(TableName=TableName, Key=key, AttributeUpdates=item)
