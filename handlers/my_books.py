from aiogram import Router, F
from aiogram.types import Message

from database import get_user_books


router = Router()


@router.message(F.text == "👤 Мои книги")
async def my_books_handler(message: Message):
    books = await get_user_books(
        message.from_user.id
    )

    if not books:
        await message.answer(
            "У тебя сейчас нет взятых книг."
        )
        return

    text = "📚 Твои книги:\n\n"

    for book in books:
        book_id = book[0]
        title = book[1]
        author = book[2]
        genre = book[3]

        text += (
            f"📖 {title}\n"
            f"Автор: {author}\n"
            f"Жанр: {genre}\n\n"
        )

    await message.answer(text)