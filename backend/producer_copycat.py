from kafka import KafkaProducer
import json
import asyncio
import random
import time
from datetime import datetime
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

# Параметры подключения к базе данных
db_params = {
    'dbname': POSTGRES_DB,
    'user': POSTGRES_USER,
    'password': POSTGRES_PASSWORD,
    'host': 'localhost',
    'port': '5435'
}

random.seed(time.time())

# status = added, processing, done
# Словарик, где будем хранить ключ по формату: <id отделения>_<id услуги>, а значением будет статус
# нужно, чтобы ненасоздавать неправильных ивентов
branches_events_status = {}


async def generate_event(kafka_producer, postgres_conn, branch_id):
    print('----------------------')
    cursor = postgres_conn.cursor()
    cursor.execute(f'SELECT service_id FROM branches_services WHERE branch_id={branch_id}')
    services = cursor.fetchall()
    cursor.close()

    services_ids = [service[0] for service in services]

    service_id = random.choice(services_ids)
    branch_event_key = f'{branch_id}_{service_id}'

    event_status = None

    if not (status := branches_events_status.get(branch_event_key)):
        event_status = 'added'

    elif status == 'added':
        await asyncio.sleep(random.choice(range(10, 120)))
        event_status = 'processing'

    elif status == 'processing':
        await asyncio.sleep(random.choice(range(10, 120)))
        event_status = 'done'

    if not event_status:
        await asyncio.sleep(random.choice(range(10, 120)))
        event_status = 'added'

    branches_events_status[branch_event_key] = event_status
    res = {
        "branch_id": branch_id,
        "status": event_status,
        "service_id": service_id,
        "event_time": datetime.now().isoformat(),
    }
    print(res)
    kafka_producer.send('events', res)
    print('----------------------')
    await asyncio.sleep(1)


async def generate_events():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    cursor.execute('SELECT id FROM branches')
    branches = cursor.fetchall()
    cursor.close()

    producer = KafkaProducer(bootstrap_servers='localhost:9094',
                             value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    while True:
        tasks = [generate_event(producer, connection, branch[0]) for branch in branches]
        await asyncio.gather(*tasks)


asyncio.get_event_loop().run_until_complete(generate_events())
