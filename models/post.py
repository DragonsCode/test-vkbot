from sqlalchemy import Column, ForeignKey, Integer, String

from model_admin import ModelAdmin
from database import Base


class Post(Base, ModelAdmin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    peer = Column(ForeignKey("users.id"))
    data = Column(String(1000))

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}(" f"id={self.id}, " f"data={self.data}" f")>"
        )

    '''@classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()'''