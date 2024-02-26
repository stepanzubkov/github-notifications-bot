from tortoise.models import Model
from tortoise import fields


class User(Model):
    """
    Telegram user model.
    """
    user_id = fields.IntField(null=False, unique=True)
    gh_access_token = fields.CharField(max_length=255, null=False)
    last_checked = fields.DatetimeField(null=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
