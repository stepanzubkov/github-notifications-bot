"""
    CRUD modules for User model.
"""

from datetime import datetime
from database.models import User


async def create_or_update_user(
    user_id: int,
    gh_access_token: str,
) -> User:
    """
    Creates User model.
    """
    user = await User.filter(user_id=user_id).first()
    if user is None:
        user = User(user_id=user_id, gh_access_token=gh_access_token)
    else:
        user.gh_access_token = gh_access_token

    await user.save()
    return user


async def get_user_by_user_id(user_id: int) -> User:
    user = await User.filter(user_id=user_id).first()
    return user


async def update_last_checked_by_user_id(user_id: int):
    user = await User.filter(user_id=user_id).first()
    user.last_checked = datetime.now()
    await user.save()
