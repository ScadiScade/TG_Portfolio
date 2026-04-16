import aiosqlite

DB_NAME = "shop.db"

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
        # Insert some demo items if empty
        async with db.execute('SELECT COUNT(*) FROM items') as cursor:
            count = (await cursor.fetchone())[0]
            if count == 0:
                await db.executemany(
                    'INSERT INTO items (name, description, price) VALUES (?, ?, ?)',
                    [
                        ('Telegram Bot (Basic)', 'A simple echo or forwarding bot', 1000),
                        ('Shop Bot', 'A fully functional online store in Telegram', 5000),
                        ('API Integration Bot', 'Bot with OpenAI or other API integrations', 3000)
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
