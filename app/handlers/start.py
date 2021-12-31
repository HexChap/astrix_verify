from aiogram.types import (
    Message, InlineKeyboardButton,
    InlineKeyboardMarkup
)

from ..config import dispatcher, settings


@dispatcher.message_handler(commands="start")
async def start(msg: Message):
    text = (
        "Добро пожаловать!\n"
        "Тут вы можете проверить подлинность аккаунта ASTRIX.\n"
        "Для продолжения нажмите \"Проверить\""
    )

    verify_btn = InlineKeyboardButton("Проверить!", callback_data="verify")
    add_url_btn = InlineKeyboardButton("Добавить!", callback_data="add_url")

    kb = InlineKeyboardMarkup()
    kb.add(verify_btn)

    if msg.from_user.id in settings.bot.admin_ids:
        kb.add(add_url_btn)

    await msg.reply(text, reply_markup=kb)
