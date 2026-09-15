from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def genres_keyboard(genres):
    buttons = []

    for genre in genres:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=genre,
                    callback_data=f"genre:{genre}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def book_keyboard(book_id, is_available):
    buttons = []

    if is_available:
        buttons.append(
            [
                InlineKeyboardButton(
                    text="📚 Забрать книгу",
                    callback_data=f"take_book:{book_id}"
                )
            ]
        )

    buttons.append(
        [
            InlineKeyboardButton(
                text="⭐ Читать отзывы",
                callback_data=f"reviews:{book_id}"
            )
        ]
    )

    buttons.append(
        [
            InlineKeyboardButton(
                text="✍️ Написать отзыв",
                callback_data=f"write_review:{book_id}"
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
    
def my_book_keyboard(book_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="↩️ Вернуть книгу",
                    callback_data=f"return_book:{book_id}"
                )
            ]
        ]
    )
def rating_keyboard(book_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 ⭐",
                    callback_data=f"rating:{book_id}:1"
                ),
                InlineKeyboardButton(
                    text="2 ⭐",
                    callback_data=f"rating:{book_id}:2"
                ),
                InlineKeyboardButton(
                    text="3 ⭐",
                    callback_data=f"rating:{book_id}:3"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="4 ⭐",
                    callback_data=f"rating:{book_id}:4"
                ),
                InlineKeyboardButton(
                    text="5 ⭐",
                    callback_data=f"rating:{book_id}:5"
                ),
            ]
        ]
    )
def add_book_genres_keyboard():
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

    buttons = []

    for genre in genres:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=genre,
                    callback_data=f"add_genre:{genre}"
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )