import json
import os
from pathlib import Path

from pydantic import BaseModel
from aiogram import Bot, Dispatcher
from aiogram.types.message import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from tortoise import Tortoise


class BotSettings(BaseModel):
    token: str
    id: int
    username: str
    admin_ids: list[int]


class DBSettings(BaseModel):
    address: str
    port: int
    user: str
    password: str
    database: str


class Settings(BaseModel):
    bot: BotSettings
    db_server: DBSettings


with open(Path("data") / "config.json") as file:
    settings = json.load(file)

settings = Settings(**settings)

bot = Bot(token=settings.bot.token, parse_mode=ParseMode.MARKDOWN)
storage = MemoryStorage()
dispatcher = Dispatcher(bot, storage=storage)


async def configure_database():
    models = ["app.models"]

    DB_CONN = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.asyncpg',
                'credentials': {
                    'host': settings.db_server.address,
                    'port': settings.db_server.port,
                    'user': settings.db_server.user,
                    'password': settings.db_server.password,
                    'database': settings.db_server.database
                }
            }
        },
        'apps': {
            'default': {
                'models': models,
                'default_connection': 'default'
            }
        }
    }

    await Tortoise.init(config=DB_CONN)

    await Tortoise.generate_schemas()
