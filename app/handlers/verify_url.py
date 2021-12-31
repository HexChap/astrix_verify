import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from ..config import dispatcher
from ..models import URLsModel


class URLState(StatesGroup):
    url = State()


@dispatcher.message_handler(commands="verify")
async def start_verifying(msg: Message):
    await URLState.url.set()

    await msg.answer("Введите ссылку в поле сообщения")


@dispatcher.message_handler(state=URLState.url)
async def process_url(msg: Message, state: FSMContext):
    msg.text = msg.text.split("?start")[0]
    msg.text = re.sub(r"(http|https)://", "", msg.text)

    if not re.match(r"^t\.me\/[-a-zA-Z0-9_.]+$", msg.text):
        await msg.reply("Ссылка должна быть формата: t.me/example")
        return

    await state.finish()

    if await URLsModel.filter(url=msg.text):
        await msg.reply(
            "✅\nАккаунт подлинный.\n"
            "ASTRIX гарантирует законность и честность действий данного линка. \n\n"
            "Благодарим за участие в проекте и желаем удачи!"
        )

    else:
        await msg.reply(
            "❌\nАккаунт поддельный!\n"
            "ASTRIX не рекомендует иметь какие-либо взаимоотношения с данным линком и не несёт ответственности за его действия.\n\n"
            "Благодарим за участие в проекте и желаем удачи!"
        )


@dispatcher.callback_query_handler(lambda cb: cb.data == "verify")
async def process_callback_verify_btn(cb_query: CallbackQuery):
    await start_verifying(cb_query.message)

    await cb_query.message.delete()
