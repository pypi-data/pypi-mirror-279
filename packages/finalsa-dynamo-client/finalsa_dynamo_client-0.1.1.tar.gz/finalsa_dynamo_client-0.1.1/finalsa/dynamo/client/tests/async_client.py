from typing import List, Dict
from finalsa.dynamo.client.interface import AsyncDynamoClient as Interface
from .implementation import DynamoClientTestImpl as Impl


class AsyncDynamoClientTestImpl(Interface):

    def __init__(self):
        self.__impl__ = Impl()

    async def write_transaction(self, transactions: List):
        self.__impl__.write_transaction(transactions)

    async def query(self, TableName: str, **kwargs):
        return self.__impl__.query(TableName, **kwargs)

    async def get(self, TableName: str, item: Dict):
        return self.__impl__.get(TableName, item)

    async def put(self, TableName: str, item: Dict):
        self.__impl__.put(TableName, item)

    async def delete(self, TableName: str, key: Dict):
        self.__impl__.delete(TableName, key)

    async def scan(self, TableName: str, **kwargs):
        return self.__impl__.scan(TableName, **kwargs)

    async def update(self, TableName: str, key: Dict, item: Dict):
        return self.__impl__.update(TableName, key, item)

    def clear(self):
        self.__impl__.clear()
