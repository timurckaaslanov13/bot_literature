from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import add_book_by_user, get_database_user_id
from keyboards.books import add_book_genres_keyboard


router = Router()


class AddBookState(StatesGroup):
    title = State()
    author = State()
    genre = State()
    description = State()
@router.message(F.text == "➕ Добавить книгу")
async def add_book_start(
    message: Message,
    state: FSMContext
):
    await state.set_state(
        AddBookState.title
    )

    await message.answer(
        "Введите название книги:"
    )
@router.message(AddBookState.title)
async def add_book_title(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        title=message.text.strip()
    )

    await state.set_state(
        AddBookState.author
    )

    await message.answer(
        "Введите автора книги:"
    )
@router.message(AddBookState.author)
async def add_book_author(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        author=message.text.strip()
    )

    await state.set_state(
    AddBookState.genre
    )

    await message.answer(
        "Выберите жанр книги:",
    reply_markup=add_book_genres_keyboard()
    )
@router.callback_query(
    AddBookState.genre,
    F.data.startswith("add_genre:")
)
async def add_book_genre(
    callback: CallbackQuery,
    state: FSMContext
):
    genre = callback.data.split(":", 1)[1]

    await state.update_data(
        genre=genre
    )

    await state.set_state(
        AddBookState.description
    )

    await callback.message.answer(
        f"Жанр: {genre}\n\n"
        "Теперь введи краткое описание книги:"
    )

    await callback.answer()
@router.message(AddBookState.description)
async def add_book_description(
    message: Message,
    state: FSMContext
):
    await state.update_data(
        description=message.text.strip()
    )

    data = await state.get_data()

    owner_id = await get_database_user_id(
        message.from_user.id
    )

    if owner_id is None:
        await message.answer(
            "Пользователь не найден. Отправь /start."
        )

        await state.clear()
        return

    await add_book_by_user(
        title=data["title"],
        author=data["author"],
        genre=data["genre"],
        description=data["description"],
        owner_id=owner_id
    )

    await message.answer(
        "✅ Книга добавлена в каталог!\n\n"
        f"📖 {data['title']}\n"
        f"Автор: {data['author']}\n"
        f"Жанр: {data['genre']}"
    )

    await state.clear()