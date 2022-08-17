from sqlalchemy import update
from sqlalchemy.future import select

from datetime import datetime

from database import async_db_session
from post import Post
from user import User


class methods:
    async def get_user(id: int=0):
        if id:
            user = await User.get(id=id)
            return user
        else:
            user = await User.get_all()
            return user
    
    async def create_user(id: int, name: str, about: str, coins: int, last_time=datetime.now()):
        await User.create(
            id=id,
            name=name,
            about=about,
            coins=coins,
            last_time=last_time,
        )
        return
    
    async def edit_user(id: int, name: str, about: str, coins: str, last_time=datetime.now()):
        #user = User.get(peer)
        await User.update(
            id=id,
            name=name,
            about=about,
            coins=coins,
            last_time=last_time,
        )
        return
    
    async def get_post(id: int=0, peer: int=0):
        if id:
            post = await Post.get(id=id)
            return post
        elif peer:
            post = await Post.get_all(peer=peer)
            return post
        else:
            post = await Post.get_all()
            return post

    async def create_post(peer: int, data: str):
        await Post.create(
            peer=peer,
            data=data,
        )
        return

    async def edit_post(id: int, peer: int, data: str, block: bool=False):
        if block:
            post = await Post.get(id=id)
            post.delete()
            await async_db_session.commit()
        await Post.update(
            id=id,
            peer=peer,
            data=data,
        )
        return

