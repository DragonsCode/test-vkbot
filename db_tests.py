import asyncio
from unicodedata import category
from models.database import async_db_session
from models.db_api import methods as db
async def new_user():
    a = await db.create_user(id=-1, name='GOD OF THIS BOT', age=999, about='............', coins=999999)
    print(a)
    user = await db.get_user(id=-1) #549425694 my vk id
    return user
async def new_post(peer, title, data, category):
    a = await db.create_post(peer=peer, title=title, data=data, category=category)
    print(a)
    post = await db.get_post(peer=peer)
    return post
async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()
async def async_main():
    await init_app()
    user = await new_user()
    print(str(user))
    all_users = await db.get_user()
    print(all_users)
    post = await new_post(peer=user.num, title='They are coming', data='Machines... I believe that they will make our future more beautiful, but there is still one thing that we do not know...', category='IT')
    for i in post:
        print('LOOK AT THIS AMAZING POST!!!!', str(i))
asyncio.run(async_main())