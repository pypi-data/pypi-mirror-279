from typing import List, Dict
from finalsa.dynamo.client.interface import SyncDynamoClient as Interface


def is_equal(item: Dict, key: Dict):
    for k, v in key.items():
        if item.get(k) != v:
            return False
    return True


def eval_expressions(item, filters, actions):
    for filter in filters:
        if filter[0] in actions and filter[1]['key'] in item:
            action_eval = actions[filter[0]](
                item[filter[1]['key']], filter[1]['value'])
            if not action_eval:
                return False
    return True



def get_key_from_dict(a: Dict) -> Dict:
    if 'Put' in a:
        item = a['Put']['Item']
    elif 'Update' in a:
        item = a['Update']['Key']
    result = {}
    if 'PK' in item:
        result['PK'] = item['PK']
    if 'SK' in item:
        result['SK'] = item['SK']
    return result


def are_affecting_same_dict(a: Dict, b: Dict):
    return get_key_from_dict(a) == get_key_from_dict(b)


def clean_transactions(transactions: List[Dict]) -> List[Dict]:
    unique_transactions = []
    for transaction in transactions:
        if not any(are_affecting_same_dict(transaction, unique_transaction) for unique_transaction in unique_transactions):
            unique_transactions.append(transaction)
    diff = list(filter(lambda x: x not in unique_transactions, transactions))
    if diff and len(diff) > 0:
        raise Exception(
            f"Transactions are affecting the same item: {diff}")
    return unique_transactions

class DynamoClientTestImpl(Interface):

    def __init__(self):
        self.tables = {}

    def get_table(self, TableName: str):
        if TableName not in self.tables:
            self.tables[TableName] = []
        return self.tables[TableName]

    def put_transaction(self, transaction: Dict):
        self.get_table(transaction['TableName'])
        item = transaction['Item']
        if 'PK' in item and 'SK' in item:
            self.delete(transaction['TableName'], {
                'PK': item['PK'],
                'SK': item['SK']
            })
        self.tables[transaction['TableName']].append(transaction['Item'])

    def delete_transaction(self, transaction: Dict):
        self.get_table(transaction['TableName'])
        self.tables[transaction['TableName']] = list(filter(
            lambda x: x != transaction['Item'], self.tables[transaction['TableName']]))

    def update_transaction(self, transaction: Dict):
        self.get_table(transaction['TableName'])
        for item in self.tables[transaction['TableName']]:
            if is_equal(item, transaction['Key']):
                update_expression = transaction['UpdateExpression']
                update_expression = update_expression.replace('SET', '')
                update_expression = update_expression.replace(' ', '')
                update_expression = update_expression.split(',')
                update_expression_dict = {}
                for expression in update_expression:
                    key, value = expression.split('=')
                    update_expression_dict[key] = value
                for key, value in update_expression_dict.items():
                    attr = transaction["ExpressionAttributeNames"][key]
                    val = transaction["ExpressionAttributeValues"][value]
                    item[attr] = val
                return
        raise Exception('Item not found')

    def write_transaction(self, transactions: List):
        accepted_transaction_types = ['Put', 'Update', 'Delete']
        transactions = clean_transactions(transactions)
        for transaction in transactions:
            for key in transaction:
                item = transaction[key]
                if key not in accepted_transaction_types:
                    raise Exception('Invalid transaction type')
                if key == 'Put':
                    self.put_transaction(item)
                elif key == 'Update':
                    self.update_transaction(item)
                elif key == 'Delete':
                    self.delete_transaction(item)

    def query(self, TableName: str, **kwargs):
        if TableName not in self.tables:
            return {'Items': [], 'Count': 0}
        expression_attribute_values = kwargs.get(
            'ExpressionAttributeValues', {})
        key_condition_expression = kwargs.get('KeyConditionExpression', '')
        key_condition_expression = key_condition_expression.replace(' ', '')
        key_condition_expression = key_condition_expression.split('AND')
        key_condition_expression_dict = {}
        for expression in key_condition_expression:
            key, value = expression.split('=')
            key_condition_expression_dict[key] = expression_attribute_values[
                value]
        items = []
        for item in self.tables[TableName]:
            if is_equal(item, key_condition_expression_dict):
                items.append(item)
        return {'Items': items, 'Count': len(items)}

    def get(self, TableName: str, key: Dict):
        self.get_table(TableName)
        for i in self.tables[TableName]:
            if is_equal(i, key):
                return i
        return None

    def put(self, TableName: str, item: Dict):
        self.get_table(TableName)
        self.tables[TableName].append(item)

    def delete(self, TableName: str, key: Dict):
        self.get_table(TableName)
        self.tables[TableName] = list(filter(
            lambda x: not is_equal(x, key), self.tables[TableName]))

    def scan(self, TableName: str, **kwargs):
        if TableName not in self.tables:
            return {'Items': []}

        def begins_with(x: str, y):
            if isinstance(x, dict):
                return begins_with(x['S'], y)
            if isinstance(y, dict):
                return begins_with(x, y['S'])
            return x.startswith(y)
        actions = {
            "begins_with": begins_with
        }
        if not kwargs or len(kwargs) == 0:
            return {'Items': self.tables[TableName]}
        filters = []
        if 'FilterExpression' in kwargs:
            expresions = kwargs['FilterExpression']
            expresions = expresions.replace(' ', '')
            expresions = expresions.split('AND')
            values = kwargs['ExpressionAttributeValues']

            for expresion in expresions:
                if 'begins_with' in expresion:
                    expresion = expresion.replace('begins_with', '')
                    expresion = expresion.replace('(', '')
                    expresion = expresion.replace(')', '')
                    key, value = expresion.split(',')
                    filters.append(('begins_with', {
                        "key": key,
                        "value": values[value]
                    }))

        items = []
        for item in self.tables[TableName]:
            if eval_expressions(item, filters, actions):
                items.append(item)
        return {'Items': items}

    def update(self, TableName: str, key: Dict, item: Dict):
        self.get_table(TableName)
        for i in self.tables[TableName]:
            if is_equal(i, key):
                for k, v in item.items():
                    i[k] = v
                return i
        return {'Item': None}

    def clear(self):
        self.tables = {}
