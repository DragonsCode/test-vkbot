from datetime import datetime, timedelta
from unicodedata import category

from config import scheduler, bot
from models.db_api import methods as db


async def get_bonus():
    users = await db.get_user()
    for user in users:
        if user.bonus:
            await db.edit_user(
                id=user.id,
                name=user.name,
                age=user.age,
                about=user.about,
                coins=user.coins,
                category=user.category,
                bonus=0
            )
            await bot.api.messages.send(peer_id=user.id, message='You can get a free coin', random_id=0)

def bonus_schedule():
    scheduler.add_job(get_bonus, 'interval', minutes=10)