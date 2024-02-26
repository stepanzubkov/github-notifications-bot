from tortoise import Tortoise

from config import settings


async def init(create_all: bool = False):
    """
    Database initialization function.
    """
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["database.models"]}
    )
    if create_all:
        await Tortoise.generate_schemas()
