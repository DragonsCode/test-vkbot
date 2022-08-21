from sqlalchemy import update
from sqlalchemy.future import select

from datetime import datetime

from models.database import async_db_session
from models.post import Post
from models.user import User


class methods:
    async def get_user(id: int=0, peer: int=0, category: str=0):
        if id:
            user = await User.get(num=id)
            return user
        elif peer:
            user = await User.get_by_id(id=peer)
            return user
        elif category:
            user = await User.get_all(category=category)
            return user
        else:
            user = await User.get_all()
            return user
    
    async def create_user(id: int, name: str, age: int, about: str, coins: int=0, category: str='No category', last_time=datetime.now()):
        user = await User.get(id=id)
        if user is not None:
            return 'duplicate for this peer id'
        await User.create(
            id=id,
            name=name,
            age=age,
            about=about,
            coins=coins,
            category=category,
            last_time=last_time
        )
        return 'created successfully'
    
    async def edit_user(id: int, name: str, age:int, about: str, coins: str, category: str, bonus: int, last_time=datetime.now()):
        #user = User.get(peer)
        await User.updater(
            id=id,
            name=name,
            age=age,
            about=about,
            coins=coins,
            category=category,
            bonus=bonus,
            last_time=last_time
        )
        return
    
    async def get_post(id: int=0, peer: int=0, category: str=0):
        if id:
            post = await Post.get(id=id)
            return post
        elif peer:
            post = await Post.get_all(peer=peer)
            return post
        elif category:
            post = await Post.get_all(category=category)
            return post
        else:
            post = await Post.get_all()
            return post

    async def create_post(peer: int, title: str, data: str, category: str):
        await Post.create(
            peer=peer,
            title=title,
            data=data,
            category=category
        )
        return

    async def edit_post(id: int, peer: int, title: str, data: str, category: str, block: bool=False):
        if block:
            post = await Post.get(id=id)
            post.delete()
            await async_db_session.commit()
        await Post.updater(
            id=id,
            peer=peer,
            title=title,
            data=data,
            category=category
        )
        return

