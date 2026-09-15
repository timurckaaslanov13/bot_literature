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