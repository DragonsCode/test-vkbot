import asyncio
from database import async_db_session
from db_api import methods as db
async def new_user():
    try:
        await db.create_user(id=549425694, name='Dima', about='I am not an engineer', coins=0)
    except:
        print(1)
    user = await db.get_user(id=549425694)
    return user
async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()
async def async_main():
    await init_app()
    user = await new_user()
    print(str(user))
    all_users = await db.get_user()
    print(all_users)
asyncio.run(async_main())