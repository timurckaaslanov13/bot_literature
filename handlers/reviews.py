from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from database import add_review, get_reviews
from keyboards.books import rating_keyboard


router = Router()


class ReviewState(StatesGroup):
    waiting_for_text = State()

@router.callback_query(F.data.startswith("write_review:"))
async def write_review_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    book_id = int(
        callback.data.split(":")[1]
    )

    await state.update_data(
        book_id=book_id
    )

    await callback.message.answer(
        "Поставь оценку книге:",
        reply_markup=rating_keyboard(book_id)
    )

    await callback.answer()
@router.callback_query(F.data.startswith("rating:"))
async def rating_handler(
    callback: CallbackQuery,
    state: FSMContext
):
    parts = callback.data.split(":")

    book_id = int(parts[1])
    rating = int(parts[2])

    await state.update_data(
        book_id=book_id,
        rating=rating
    )

    await state.set_state(
        ReviewState.waiting_for_text
    )

    await callback.message.answer(
        f"Ты поставил {rating} ⭐\n\n"
        "Теперь напиши текст отзыва:"
    )

    await callback.answer()
@router.message(ReviewState.waiting_for_text)
async def review_text_handler(
    message: Message,
    state: FSMContext
):
    data = await state.get_data()

    book_id = data["book_id"]
    rating = data["rating"]

    review_text = message.text

    user_id = message.from_user.id

    from database import get_database_user_id

    db_user_id = await get_database_user_id(
        user_id
    )

    if db_user_id is None:
        await message.answer(
            "Не удалось найти пользователя."
        )

        await state.clear()
        return

    await add_review(
        user_id=db_user_id,
        book_id=book_id,
        rating=rating,
        text=review_text
    )

    await message.answer(
        "✅ Спасибо! Отзыв сохранён."
    )

    await state.clear()

@router.callback_query(F.data.startswith("reviews:"))
async def read_reviews_handler(
    callback: CallbackQuery
):
    book_id = int(
        callback.data.split(":")[1]
    )

    reviews = await get_reviews(book_id)

    if not reviews:
        await callback.message.answer(
            "У этой книги пока нет отзывов."
        )

        await callback.answer()
        return

    await callback.message.answer(
        "⭐ Отзывы:"
    )

    for review in reviews:
        first_name = review[0]
        rating = review[1]
        text = review[2]

        stars = "⭐" * rating

        review_text = (
            f"👤 {first_name}\n"
            f"{stars}\n\n"
            f"{text}"
        )

        await callback.message.answer(
            review_text
        )

    await callback.answer()