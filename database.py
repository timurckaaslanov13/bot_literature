import aiosqlite


DB_NAME = "library.db"


async def create_tables():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE NOT NULL,
                username TEXT,
                first_name TEXT
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                genre TEXT NOT NULL,
                description TEXT,
                is_available INTEGER DEFAULT 1,
                taken_by INTEGER,
                FOREIGN KEY (taken_by) REFERENCES users(id)
            )
        """)

        await db.execute("""
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (book_id) REFERENCES books(id)
            )
        """)

        await db.commit()
async def add_book(title, author, genre, description=""):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT INTO books (
                title,
                author,
                genre,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                title,
                author,
                genre,
                description
            )
        )

        await db.commit()
async def add_test_books():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            "SELECT COUNT(*) FROM books"
        )

        result = await cursor.fetchone()

        if result[0] > 0:
            return

        books = [
            (
                "Ведьмак: Последнее желание",
                "Анджей Сапковский",
                "Фэнтези",
                "Сборник рассказов о ведьмаке Геральте."
            ),
            (
                "Дюна",
                "Фрэнк Герберт",
                "Фантастика",
                "История планеты Арракис и Пола Атрейдеса."
            ),
            (
                "Убийство в Восточном экспрессе",
                "Агата Кристи",
                "Детектив",
                "Эркюль Пуаро расследует загадочное убийство."
            ),
            (
                "1984",
                "Джордж Оруэлл",
                "Антиутопия",
                "Роман о тоталитарном государстве."
            ),
            (
                "Мастер и Маргарита",
                "Михаил Булгаков",
                "Классика",
                "Один из самых известных романов Булгакова."
            )
        ]

        await db.executemany(
            """
            INSERT INTO books (
                title,
                author,
                genre,
                description
            )
            VALUES (?, ?, ?, ?)
            """,
            books
        )

        await db.commit()