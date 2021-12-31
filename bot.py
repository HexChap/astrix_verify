import aiogram

import app.handlers
from app.config import dispatcher, configure_database


async def on_startup(dispatcher):
    await configure_database()


aiogram.executor.start_polling(dispatcher, on_startup=on_startup)
