from abc import ABC, abstractmethod
from typing import List, Dict


class SyncDynamoClient(ABC):

    @abstractmethod
    def write_transaction(self, transactions: List):
        pass

    @abstractmethod
    def query(self, table_name: str, **kwargs):
        pass

    @abstractmethod
    def put(self, table_name: str, item: Dict):
        pass

    @abstractmethod
    def delete(self, table_name: str, key: Dict):
        pass

    @abstractmethod
    def scan(self, table_name: str, **kwargs):
        pass

    @abstractmethod
    def get(self, table_name: str, key: Dict) -> Dict:
        pass

    @abstractmethod
    def update(self, TableName: str, key: Dict, item: Dict):
        pass
