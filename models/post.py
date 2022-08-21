from sqlalchemy import Column, ForeignKey, Integer, String

from config import ioloop

from models.model_admin import ModelAdmin
from models.database import Base
from models.user import User


class Post(Base, ModelAdmin):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    peer = Column(ForeignKey("users.num"))
    title = Column(String(100))
    data = Column(String(1000))
    category = Column(String(100))

    def __str__(self):
        return f'Category: {self.category}\nTitle: {self.title}\nPost: {self.data}'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"title={self.title}, "
            f"data={self.data}, "
            f"category={self.category}"
            f")>"
        )

    '''@classmethod
    async def filter_by_user_id(cls, user_id):
        query = select(cls).where(cls.user_id == user_id)
        posts = await async_db_session.execute(query)
        return posts.scalars().all()'''