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
                genre_id INTEGER,
                description TEXT,
                is_available INTEGER DEFAULT 1,
                taken_by INTEGER,
                owner_id INTEGER,
                FOREIGN KEY (taken_by) REFERENCES users(id),
                FOREIGN KEY (owner_id) REFERENCES users(id),
                FOREIGN KEY (genre_id) REFERENCES genres(id)
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
    
        
        await db.execute("""
            CREATE TABLE IF NOT EXISTS genres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
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

async def get_genres():
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT id, name
            FROM genres
            ORDER BY name
            """
        )

        return await cursor.fetchall()

async def get_books_by_genre(genre_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT
                books.id,
                books.title,
                books.author,
                genres.name,
                books.description,
                books.is_available

            FROM books

            JOIN genres
                ON books.genre_id = genres.id

            WHERE books.genre_id = ?

            ORDER BY books.title
            """,
            (genre_id,)
        )

        return await cursor.fetchall()
    
async def add_user(telegram_id, username, first_name):
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute(
            """
            INSERT OR IGNORE INTO users (
                telegram_id,
                username,
                first_name
            )
            VALUES (?, ?, ?)
            """,
            (
                telegram_id,
                username,
                first_name
            )
        )

        await db.commit()
        
async def take_book(book_id, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:

        cursor = await db.execute(
            """
            SELECT is_available
            FROM books
            WHERE id = ?
            """,
            (book_id,)
        )

        book = await cursor.fetchone()

        if book is None:
            return "not_found"

        if book[0] == 0:
            return "already_taken"

        cursor = await db.execute(
            """
            SELECT id
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await cursor.fetchone()

        if user is None:
            return "user_not_found"

        user_id = user[0]

        await db.execute(
            """
            UPDATE books
            SET is_available = 0,
                taken_by = ?
            WHERE id = ?
            """,
            (
                user_id,
                book_id
            )
        )

        await db.commit()

        return "success"

async def get_user_books(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT
                books.id,
                books.title,
                books.author,
                genres.name
            FROM books

            JOIN users
                ON books.taken_by = users.id

            JOIN genres
                ON books.genre_id = genres.id

            WHERE users.telegram_id = ?

            ORDER BY books.title
            """,
            (telegram_id,)
        )

        return await cursor.fetchall()
async def return_book(book_id, telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT books.taken_by
            FROM books
            WHERE books.id = ?
            """,
            (book_id,)
        )

        book = await cursor.fetchone()

        if book is None:
            return "not_found"

        cursor = await db.execute(
            """
            SELECT id
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await cursor.fetchone()

        if user is None:
            return "user_not_found"

        user_id = user[0]

        if book[0] != user_id:
            return "not_yours"

        await db.execute(
            """
            UPDATE books
            SET is_available = 1,
                taken_by = NULL
            WHERE id = ?
            """,
            (book_id,)
        )

        await db.commit()

        return "success"  
async def add_review(user_id, book_id, rating, text):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO reviews (
                user_id,
                book_id,
                rating,
                text
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                book_id,
                rating,
                text
            )
        )

        await db.commit()


async def get_reviews(book_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT users.first_name,
                   reviews.rating,
                   reviews.text,
                   reviews.created_at
            FROM reviews
            JOIN users
                ON reviews.user_id = users.id
            WHERE reviews.book_id = ?
            ORDER BY reviews.created_at DESC
            """,
            (book_id,)
        )

        return await cursor.fetchall()
async def get_database_user_id(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT id
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = await cursor.fetchone()

        if user is None:
            return None

        return user[0]
async def search_books(query):
    async with aiosqlite.connect(DB_NAME) as db:
        search_value = f"%{query}%"

        cursor = await db.execute(
            """
            SELECT
                books.id,
                books.title,
                books.author,
                genres.name,
                books.description,
                books.is_available

            FROM books

            JOIN genres
                ON books.genre_id = genres.id

            WHERE books.title LIKE ?
               OR books.author LIKE ?

            ORDER BY books.title
            """,
            (
                search_value,
                search_value
            )
        )

        return await cursor.fetchall()
async def add_book_by_user(
    title,
    author,
    genre_id,
    description,
    owner_id
):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO books (
                title,
                author,
                genre_id,
                description,
                is_available,
                taken_by,
                owner_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title,
                author,
                genre_id,
                description,
                1,
                None,
                owner_id
            )
        )

        await db.commit()
async def add_default_genres():
    genres = [
        "Фэнтези",
        "Фантастика",
        "Детектив",
        "Роман",
        "Классика",
        "Ужасы",
        "Психология",
        "История"
    ]

    async with aiosqlite.connect(DB_NAME) as db:
        for genre in genres:
            await db.execute(
                """
                INSERT OR IGNORE INTO genres (name)
                VALUES (?)
                """,
                (genre,)
            )

        await db.commit()
async def get_genre_name(genre_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT name
            FROM genres
            WHERE id = ?
            """,
            (genre_id,)
        )

        genre = await cursor.fetchone()

        if genre is None:
            return "Неизвестный жанр"

        return genre[0]