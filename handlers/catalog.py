from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database import get_genres, get_books_by_genre, take_book
from keyboards.books import genres_keyboard, book_keyboard



router = Router()


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

    genre_id = int(
        callback.data.split(":")[1]
    )

    books = await get_books_by_genre(
        genre_id
    )

    if not books:
        await callback.message.answer(
            "В этом жанре пока нет книг."
        )

        await callback.answer()
        return

    for book in books:

        book_id = book[0]
        title = book[1]
        author = book[2]
        genre = book[3]
        description = book[4]
        is_available = book[5]

        status = (
            "✅ Доступна"
            if is_available
            else "❌ Сейчас на руках"
        )

        text = (
            f"📖 {title}\n"
            f"Автор: {author}\n"
            f"Жанр: {genre}\n\n"
            f"{description}\n\n"
            f"Статус: {status}"
        )

        await callback.message.answer(
            text,
            reply_markup=book_keyboard(
                book_id,
                is_available
            )
        )

    await callback.answer()
@router.callback_query(F.data.startswith("take_book:"))
async def take_book_handler(callback: CallbackQuery):

    book_id = int(
        callback.data.split(":")[1]
    )

    result = await take_book(
        book_id=book_id,
        telegram_id=callback.from_user.id
    )

    if result == "success":
        await callback.message.answer(
            "✅ Книга отмечена как взятая."
        )

    elif result == "already_taken":
        await callback.message.answer(
            "❌ Эту книгу уже забрали."
        )

    elif result == "user_not_found":
        await callback.message.answer(
            "Сначала отправь /start."
        )

    else:
        await callback.message.answer(
            "Книга не найдена."
        )

    await callback.answer()

    await callback.answer()