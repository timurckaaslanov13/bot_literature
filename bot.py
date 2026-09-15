import asyncio
import os

from database import create_tables, add_user, add_default_genres
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from handlers.catalog import router as catalog_router
from handlers.my_books import router as my_books_router
from handlers.reviews import router as reviews_router
from handlers.search import router as search_router
from handlers.add_book import router as add_book_router


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(catalog_router)
dp.include_router(my_books_router)
dp.include_router(reviews_router)
dp.include_router(search_router)
dp.include_router(add_book_router)

@dp.message(Command("start"))
async def start_command(message: Message):

    await add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )

    await message.answer(
        "Привет! Это библиотечный бот 📚\n"
        "Выбери действие:",
        reply_markup=main_keyboard
    )


@dp.message(F.text == "⭐ Отзывы")
async def reviews(message: Message):
    await message.answer("Раздел отзывов скоро добавим.")





@dp.message(F.text == "ℹ️ Помощь")
async def help_button(message: Message):
    await message.answer(
        "Здесь можно смотреть каталог книг, брать книги и оставлять отзывы."
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — помощь"
    )


async def main():

    await create_tables()
    await add_default_genres()
    

    print("База данных готова")
    print("Бот запущен")

    await dp.start_polling(bot)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📚 Каталог книг"),
            KeyboardButton(text="🔎 Поиск книги")
        ],
        [
            KeyboardButton(text="➕ Добавить книгу"),
            KeyboardButton(text="👤 Мои книги")
        ],
        [
            KeyboardButton(text="⭐ Отзывы"),
            KeyboardButton(text="ℹ️ Помощь")
        ]
    ],
    resize_keyboard=True
)

if __name__ == "__main__":
    asyncio.run(main())