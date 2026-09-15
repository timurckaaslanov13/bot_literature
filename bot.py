import asyncio
import os

from database import create_tables, add_test_books
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from handlers.catalog import router as catalog_router


load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(catalog_router)

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Привет! Выбери действие:",
        reply_markup=main_keyboard
    )

@dp.message(lambda message: message.text == "🤖 AI чат")
async def ai_chat(message: Message):
    await message.answer("AI чат пока в разработке.")


@dp.message(lambda message: message.text == "👤 Профиль")
async def profile(message: Message):
    await message.answer(
        f"Твой Telegram ID: {message.from_user.id}\n"
        f"Имя: {message.from_user.first_name}"
    )


@dp.message(lambda message: message.text == "ℹ️ Помощь")
async def help_button(message: Message):
    await message.answer(
        "Пока бот умеет показывать профиль и открывать AI-раздел."
    )

@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start — запуск бота\n"
        "/help — помощь"
    )


@dp.message()
async def echo_message(message: Message):
    await message.answer(
        f"Ты написал: {message.text}"
    )


async def main():

    await create_tables()

    await add_test_books()

    print("База данных готова")
    print("Бот запущен")

    await dp.start_polling(bot)

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🤖 AI чат"),
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="ℹ️ Помощь")
        ]
    ],
    resize_keyboard=True
)

if __name__ == "__main__":
    asyncio.run(main())