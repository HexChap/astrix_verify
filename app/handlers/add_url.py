import re

import tortoise.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from ..config import dispatcher
from ..models import URLsModel


class RegisterURL(StatesGroup):
    link_name = State()
    url = State()


@dispatcher.message_handler(commands="register")
async def register_link(msg: Message):
    await RegisterURL.link_name.set()

    await msg.answer("Введите название линка.")


@dispatcher.message_handler(state=RegisterURL.link_name)
async def process_link_name(msg: Message, state: FSMContext):
    await state.update_data(link_name=msg.text)

    await RegisterURL.url.set()

    await msg.reply("Введите ссылку.")


@dispatcher.message_handler(state=RegisterURL.url)
async def process_url(msg: Message, state: FSMContext):
    msg.text = msg.text.split("?start")[0]
    msg.text = re.sub(r"(http|https)://", "", msg.text)

    if not re.match(r"^t\.me\/[-a-zA-Z0-9_.]+$", msg.text):
        await msg.reply("Ссылка должна быть формата: t.me/example")
        return

    data = await state.get_data()
    data["url"] = msg.text
    data["by_user_tg_id"] = msg.from_user.id

    try:
        await URLsModel(**data).save()
    except tortoise.exceptions.IntegrityError:
        await msg.reply("Эта ссылка уже присутствует в базе данных!\n")
        await msg.answer("❌ Операция по добавлению завершена ошибкой")
        await state.finish()
        return

    link = (await URLsModel.filter(url=data["url"]))[0]

    await state.finish()

    await msg.reply(
        f"✅ Выполнено!\n\n"
        f"Название линка: {link.link_name}\n"
        f"Ссылка: {link.url}"
    )


@dispatcher.callback_query_handler(lambda cb: cb.data == "add_url")
async def process_callback_add_btn(cb_query: CallbackQuery):
    await register_link(cb_query.message)

    await cb_query.message.delete()
