from finalsa.dynamo.client.interface import AsyncDynamoClient as Interface
from typing import List, Dict
from .implementation import DynamoClientImpl as Impl


class AsyncDynamoClient(Interface):

    def __init__(self):
        self.__client__ = Impl()

    async def write_transaction(self, transactions: List):
        self.__client__.write_transaction(transactions)

    async def query(self, TableName: str, **kwargs):
        return self.__client__.query(TableName, **kwargs)

    async def put(self, TableName: str, item: Dict):
        self.__client__.put(TableName, item)

    async def delete(self, TableName: str, key: Dict):
        self.__client__.delete(TableName, key)

    async def get(self, table_name: str, key: Dict) -> Dict:
        return self.__client__.get(table_name, key)

    async def scan(self, TableName: str, **kwargs):
        return self.__client__.scan(TableName, **kwargs)

    async def update(self, TableName: str, key: Dict, item: Dict):
        return self.__client__.update(TableName, key, item)
