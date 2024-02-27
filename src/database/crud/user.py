"""
    CRUD modules for User model.
"""

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

