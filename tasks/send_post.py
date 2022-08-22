import random

from config import scheduler, bot
from models.db_api import methods as db


async def send_post():
    users = await db.get_user()
    adm = await db.get_user(id=-1)
    users.remove(adm)
    for user in users:
        posts = await db.get_post(category=user.category)
        post = random.choice(posts)
        creator = await db.get_user(num=post.peer)
        if creator.id == -1:
            await bot.api.messages.send(peer_id=user.id, message=f'Look at this post!\n\nCreator: {creator.name}\n\n{str(post)}', random_id=0)
        else:
            await bot.api.messages.send(peer_id=user.id, message=f'Look at this post!\n\nCreator: https://vk.com/id{creator.id}\n\n{str(post)}', random_id=0)

def post_schedule():
    scheduler.add_job(send_post, 'interval', minutes=2)