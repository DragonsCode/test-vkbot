import random

from config import scheduler, bot
from models.db_api import methods as db


async def send_post():
    users = await db.get_user()
    for user in users:
        posts = await db.get_post(category=user.category)
        post = random.choice(posts)
        creator = await db.get_user(peer=post.peer)
        await bot.api.messages.send(peer_id=user.id, message=f'Look at this post!\n\nCreator: https://vk.com/id{creator.id}\n\n{str(post)}', random_id=0)

def post_schedule():
    scheduler.add_job(send_post, 'interval', minutes=2)