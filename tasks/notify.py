from datetime import datetime, timedelta

from config import scheduler, bot
from models.db_api import methods as db


async def notify():
    users = await db.get_user()
    for user in users:
        date = datetime.now() - user.last_time
        if date > timedelta(minutes=5):
            await bot.api.messages.send(peer_id=user.id, message='This is the notify, type "menu"', random_id=0)

def notify_schedule():
    scheduler.add_job(notify, 'interval', minutes=5)