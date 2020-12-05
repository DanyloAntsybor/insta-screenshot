import os
import datetime
from airtable import Airtable

AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_KEY = os.environ['AIRTABLE_BASE_KEY']


def get_airtable_table(table_name):
    return Airtable(AIRTABLE_BASE_KEY, table_name, api_key=AIRTABLE_API_KEY)


def get_existing_clients():
    print('Start getting info on all clients')
    client_table = get_airtable_table('Клиенты')
    all_clients = client_table.get_all()
    print(type(all_clients))
    print(f'Returned {len(all_clients)} clients')
    return {c['fields']['Name']: c['id'] for c in all_clients if c and c['fields']}


def insert_new_client(client_name):
    print(f'Start Insertnig new client: {client_name}')
    client_table = get_airtable_table('Клиенты')
    result = client_table.insert({'Name': client_name})
    print(result)
    return result['id']


def insert_new_order(client_id):
    order_table = get_airtable_table('Заказы')
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    result = order_table.insert({'Клиент': [client_id], 'Дата создания заказа': today_str})
    print(result)
    return result['id']


def process_client_airtable(client_name):
    existing_clients = get_existing_clients()
    client_id = existing_clients.get(client_name)
    if not client_id:
        print('Need to create a new client row')
        client_id = insert_new_client(client_name)
    else:
        print('Client already exists in the database')

    print('Start creating new order')
    insert_new_order(client_id)
