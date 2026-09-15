from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from database import get_genres, get_books_by_genre
from keyboards.books import genres_keyboard


router = Router()

@router.message(Command("catalog"))
async def catalog_command(message: Message):
    genres = await get_genres()

    if not genres:
        await message.answer("В каталоге пока нет книг.")
        return

    await message.answer(
        "Выберите жанр:",
        reply_markup=genres_keyboard(genres)
    )

@router.message(F.text == "📚 Каталог книг")
async def catalog_button(message: Message):
    genres = await get_genres()

    if not genres:
        await message.answer("В каталоге пока нет книг.")
        return

    await message.answer(
        "Выберите жанр:",
        reply_markup=genres_keyboard(genres)
    )

@router.callback_query(F.data.startswith("genre:"))
async def genre_selected(callback: CallbackQuery):

    genre = callback.data.split(":", 1)[1]

    books = await get_books_by_genre(genre)

    if not books:
        await callback.message.answer(
            "В этом жанре пока нет книг."
        )

        await callback.answer()
        return

    await callback.message.answer(
        f"📚 Книги жанра: {genre}"
    )

    for book in books:
        book_id = book[0]
        title = book[1]
        author = book[2]
        description = book[4]
        is_available = book[5]

        if is_available:
            status = "✅ Доступна"
        else:
            status = "❌ Сейчас на руках"

        text = (
            f"📖 {title}\n"
            f"Автор: {author}\n\n"
            f"{description}\n\n"
            f"Статус: {status}"
        )

        await callback.message.answer(text)

    await callback.answer()