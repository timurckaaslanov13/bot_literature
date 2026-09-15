from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from database import get_user_books, return_book
from keyboards.books import my_book_keyboard


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

    await message.answer("📚 Твои книги:")

    for book in books:
        book_id = book[0]
        title = book[1]
        author = book[2]
        genre = book[3]

        text = (
            f"📖 {title}\n"
            f"Автор: {author}\n"
            f"Жанр: {genre}"
        )

        await message.answer(
            text,
            reply_markup=my_book_keyboard(book_id)
        )


@router.callback_query(F.data.startswith("return_book:"))
async def return_book_handler(callback: CallbackQuery):
    book_id = int(
        callback.data.split(":")[1]
    )

    result = await return_book(
        book_id=book_id,
        telegram_id=callback.from_user.id
    )

    if result == "success":
        await callback.message.edit_text(
            callback.message.text
            + "\n\n✅ Книга возвращена"
        )

    elif result == "not_yours":
        await callback.message.answer(
            "Эта книга не записана на тебя."
        )

    elif result == "user_not_found":
        await callback.message.answer(
            "Пользователь не найден."
        )

    else:
        await callback.message.answer(
            "Книга не найдена."
        )

    await callback.answer()