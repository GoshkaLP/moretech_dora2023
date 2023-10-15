import asyncpg

import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

POSTGRES_HOST = 'localhost'
POSTGRES_PORT = 5435

if os.path.exists('/proc/1'):
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = 5432


async def get_db():
    db = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        database=POSTGRES_DB,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    try:
        yield db
    finally:
        await db.close()
