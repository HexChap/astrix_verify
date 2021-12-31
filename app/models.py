from tortoise import Model
from tortoise.fields import *


class URLsModel(Model):
    id = IntField(pk=True)
    link_name = CharField(64)
    url = CharField(128, unique=True)
    by_user_tg_id = BigIntField()
    created_at = DatetimeField(auto_now_add=True)
    updated_at = DatetimeField(auto_now=True)

    class Meta:
        table = "urls"
