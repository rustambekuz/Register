from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

aiogram_keys = InlineKeyboardMarkup(inline_keyboard=[
        [  InlineKeyboardButton(text="Kurslar", url="https://python.sariq.dev"),
           InlineKeyboardButton(text="Batafsil", callback_data="course_info"),
    ],
    [
           InlineKeyboardButton(text="Ulashish", switch_inline_query="shere:group"),
    ]

])