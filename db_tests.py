import asyncio
from models.database import async_db_session
from models.db_api import methods as db
async def new_user():
    a = await db.create_user(id=549425694, name='Dima', age=16, about='I am not an engineer', coins=0)
    print(a)
    user = await db.get_user(id=549425694)
    return user
async def new_post(peer, data):
    a = await db.create_post(peer=peer, data=data)
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
    post = await new_post(peer=user.num, data='Can you see this?')
    for i in post:
        print('LOOK AT THIS AMAZING POST!!!!', str(i))
asyncio.run(async_main())