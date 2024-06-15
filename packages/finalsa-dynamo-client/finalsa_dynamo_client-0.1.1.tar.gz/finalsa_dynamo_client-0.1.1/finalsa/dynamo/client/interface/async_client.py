from abc import ABC, abstractmethod
from typing import List, Dict


class AsyncDynamoClient(ABC):

    @abstractmethod
    async def write_transaction(self, transactions: List):
        pass

    @abstractmethod
    async def query(self, table_name: str, **kwargs):
        pass

    @abstractmethod
    async def put(self, table_name: str, item: Dict):
        pass

    @abstractmethod
    async def delete(self, table_name: str, key: Dict):
        pass

    @abstractmethod
    async def scan(self, table_name: str, **kwargs):
        pass

    @abstractmethod
    async def get(self, table_name: str, key: Dict) -> Dict:
        pass

    @abstractmethod
    async def update(self, TableName: str, key: Dict, item: Dict):
        pass
