from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import search_books
from keyboards.books import book_keyboard


router = Router()


class SearchState(StatesGroup):
    waiting_for_query = State()

@router.message(F.text == "🔎 Поиск книги")
async def search_button(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        SearchState.waiting_for_query
    )

    await message.answer(
        "Напиши название книги или автора:"
    )

@router.message(SearchState.waiting_for_query)
async def search_query_handler(
    message: Message,
    state: FSMContext
):
    query = message.text.strip()

    books = await search_books(query)

    if not books:
        await message.answer(
            "Ничего не найдено."
        )

        await state.clear()
        return

    await message.answer(
        f"Найдено книг: {len(books)}"
    )

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

        await message.answer(
            text,
            reply_markup=book_keyboard(
                book_id,
                is_available
            )
        )

    await state.clear()