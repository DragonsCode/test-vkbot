from sqlalchemy import update
from sqlalchemy.future import select

from database import async_db_session


class ModelAdmin:
    @classmethod
    async def create(cls, **kwargs):
        async_db_session.add(cls(**kwargs))
        await async_db_session.commit()

    @classmethod
    async def update(cls, id, **kwargs):
        query = (
            update(cls)
            .where(cls.id == id)
            .values(**kwargs)
            #.execution_options(synchronize_session="fetch")
        )

        await async_db_session.execute(query)
        await async_db_session.commit()

    @classmethod
    async def get(cls, peer=False, id=False):
        query = None
        if peer:
            query = select(cls).where(cls.peer == peer)
        elif id:
            query = select(cls).where(cls.id == id)
        else:
            query = select(cls)
        results = await async_db_session.execute(query)
        result = results.scalars().first()
        return result
    
    @classmethod
    async def get_all(cls, peer=False, id=False):
        query = None
        if peer:
            query = select(cls).where(cls.peer == peer)
        elif id:
            query = select(cls).where(cls.id == id)
        else:
            query = select(cls)
        results = await async_db_session.execute(query)
        result = results.scalars().all()
        return result