import uuid

from aiogram import Router
from aiogram import types

from inline_bot_with_api.kepboards.inline.button import aiogram_keys

wiki_router = Router()


@wiki_router.inline_query()
async def rasm_handler(query: types.InlineQuery):
    if "kurs" in query.query.lower():
        await query.answer(
            results=[
                types.InlineQueryResultPhoto(
                    id=str(uuid.uuid4()),
                    photo_url="https://i.ytimg.com/vi/zsYIw6RXjfM/maxresdefault.jpg",
                    thumbnail_url="https://static-assets.codecademy.com/assets/course-landing-page/meta/4x3/learn-python-3.jpg",
                    caption="Python darslari",
                    description="Python darslari uchun rasm lavhasi",
                    reply_markup=aiogram_keys
                ),
                types.InlineQueryResultPhoto(
                    id=str(uuid.uuid4()),
                    photo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSHNamGOXmmvdVX8rgYHkZ_UUHHcjBjLJeocw&s",
                    thumbnail_url="https://www.youtube.com/watch?v=_aDyBPYAeyU",
                    caption="Python courses",
                    description="Python darslari",
                    reply_markup=aiogram_keys
                ),

            ],
            cache_time=1
        )
    elif "video" in query.query.lower():
        await query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Mukammal Telegram bot",
                    input_message_content=types.InputTextMessageContent(
                        message_text="Mukammal Telegram bot yaratish darslari uchun <a href='https://youtu.be/oRSa8NXWMXQ?feature=shared'>YouTube kanaliga</a> tashrif buyuring"
                    ),
                    thumbnail_url='https://i.ytimg.com/vi/oRSa8NXWMXQ/maxresdefault.jpg',
                    description="Mukammal Telegram bot yaratish"

        )
        ],
           cache_time = 1
        )

    elif "loc" in query.query.lower():
        await query.answer(
            results=[
                types.InlineQueryResultLocation(
                    id=str(uuid.uuid4()),
                    latitude=38.862235624059444,
                    longitude=65.78218118015802,
                    title="Qashqadaryo viloyati"
                )
            ],
            cache_time=1
        )

    else:
        await query.answer(
            results=[
                types.InlineQueryResultArticle(
                    id=str(uuid.uuid4()),
                    title="Python darslari",
                    input_message_content=types.InputTextMessageContent(
                        message_text='darslar uchun <a href="https://python.sariq.dev">sariq.dev</a> saytiga tashrif buyuring'
                    ),
                    url="https://python.sariq.dev",
                    thumbnail_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSxDvHfyQS5HJ-3oU_pFC6AzgNarmSU1uB5Q&s",
                    description="Python dasturlash tili darslari"
                )

            ],
            cache_time=1
        )
