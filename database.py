import asyncpg
from contextlib import asynccontextmanager
from config import *


@asynccontextmanager
async def get_connection():
    conn = await asyncpg.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    try:
        yield conn
    finally:
        await conn.close()


async def init_db():
    async with get_connection() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id BIGINT PRIMARY KEY,
                sent_m1 BOOLEAN DEFAULT FALSE,
                sent_m2 BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)


async def add_user(telegram_id: int):
    async with get_connection() as conn:
        await conn.execute("""
            INSERT INTO users (telegram_id) 
            VALUES ($1)
            ON CONFLICT (telegram_id) DO NOTHING
        """, telegram_id)


async def get_users_for_m1():
    async with get_connection() as conn:
        return await conn.fetch("""
            SELECT * FROM users 
            WHERE sent_m1 = FALSE
        """)


async def get_users_for_m2():
    async with get_connection() as conn:
        return await conn.fetch("""
            SELECT * FROM users 
            WHERE sent_m1 = TRUE AND sent_m2 = FALSE
        """)


async def mark_message_sent(telegram_id: int, message_type: str):
    async with get_connection() as conn:
        if message_type == "1":
            await conn.execute("""
                UPDATE users 
                SET sent_m1 = TRUE 
                WHERE telegram_id = $1
            """, telegram_id)
        elif message_type == "2":
            await conn.execute("""
                UPDATE users 
                SET sent_m2 = TRUE 
                WHERE telegram_id = $1
            """, telegram_id)