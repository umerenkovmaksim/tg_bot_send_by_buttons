import aiomysql

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


async def get_connection():
    return await aiomysql.create_pool(host=DB_HOST, port=int(DB_PORT), user=DB_USER, password=DB_PASSWORD, db=DB_NAME)


async def init_db():
    conn = await get_connection()
    cur = await conn.cursor()
    await cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            sent_m1 BOOLEAN DEFAULT FALSE,
            sent_m2 BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.close()
    conn.close()


async def add_user(telegram_id: int):
    conn = await get_connection()
    cur = await conn.cursor()
    await cur.execute("""
        INSERT INTO users (telegram_id) 
        VALUES (%s)
        ON DUPLICATE KEY UPDATE telegram_id = telegram_id
    """, (telegram_id,))
    cur.close()
    conn.close()


async def get_users_for_m1():
    conn = await get_connection()
    cur = await conn.cursor()
    await cur.execute("""
        SELECT * FROM users 
        WHERE sent_m1 = FALSE
    """)
    users = await cur.fetchall()
    cur.close()
    conn.close()
    return users


async def get_users_for_m2():
    conn = await get_connection()
    cur = await conn.cursor()
    await cur.execute("""
        SELECT * FROM users 
        WHERE sent_m1 = TRUE AND sent_m2 = FALSE
    """)
    users = await cur.fetchall()
    cur.close()
    conn.close()
    return users


async def mark_message_sent(telegram_id: int, message_type: str):
    conn = await get_connection()
    cur = await conn.cursor()
    if message_type == "1":
        await cur.execute("""
            UPDATE users 
            SET sent_m1 = TRUE 
            WHERE telegram_id = %s
        """, (telegram_id,))
    elif message_type == "2":
        await cur.execute("""
            UPDATE users 
            SET sent_m2 = TRUE 
            WHERE telegram_id = %s
        """, (telegram_id,))
    cur.close()
    conn.close()