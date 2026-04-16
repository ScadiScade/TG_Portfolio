import aiosqlite

DB_NAME = "showcase.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS cart (
                user_id INTEGER,
                item_id INTEGER,
                quantity INTEGER DEFAULT 1,
                PRIMARY KEY (user_id, item_id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT
            )
        ''')
        async with db.execute('SELECT COUNT(*) FROM items') as cursor:
            count = (await cursor.fetchone())[0]
            if count == 0:
                await db.executemany(
                    'INSERT INTO items (name, description, price) VALUES (?, ?, ?)',
                    [
                        ('Telegram Bot (Basic)', 'Simple bot logic', 1000),
                        ('Shop Bot', 'Fully functional e-commerce', 5000),
                        ('Web App (TMA)', 'Interactive Mini App', 8000),
                        ('Website / Landing', 'Single page website or landing page', 10000),
                        ('Fullstack Website', 'Complex website with backend and database', 25000)
                    ]
                )
        await db.commit()

async def get_items():
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM items') as cursor:
            return await cursor.fetchall()

async def get_item(item_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('SELECT * FROM items WHERE id = ?', (item_id,)) as cursor:
            return await cursor.fetchone()

async def add_to_cart(user_id: int, item_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO cart (user_id, item_id) 
            VALUES (?, ?) 
            ON CONFLICT(user_id, item_id) 
            DO UPDATE SET quantity = quantity + 1
        ''', (user_id, item_id))
        await db.commit()

async def get_cart(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute('''
            SELECT i.name, i.price, c.quantity, i.id 
            FROM cart c 
            JOIN items i ON c.item_id = i.id 
            WHERE c.user_id = ?
        ''', (user_id,)) as cursor:
            return await cursor.fetchall()

async def clear_cart(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
        await db.commit()

async def get_user_lang(user_id: int) -> str:
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT language FROM users WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else None

async def set_user_lang(user_id: int, lang: str):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO users (user_id, language) 
            VALUES (?, ?) 
            ON CONFLICT(user_id) 
            DO UPDATE SET language = ?
        ''', (user_id, lang, lang))
        await db.commit()

