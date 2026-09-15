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