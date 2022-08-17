from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.future import select

from model_admin import ModelAdmin
from database import Base, async_db_session


class User(Base, ModelAdmin):
    __tablename__ = "users"

    #id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    about = Column(String(500))
    coins = Column(Integer)
    posts = relationship("Post")
    last_time = Column(DateTime)

    # required in order to acess columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    #__mapper_args__ = {"eager_defaults": True}

    @classmethod
    async def get_by_id(cls, id):
        query = select(cls).where(cls.id == id)
        results = await async_db_session.execute(query)
        result = results.one()
        return result

    def __str__(self):
        return f'Name: {self.name}\nAge: {self.age}\nBalance: {self.coins} coins\nAbout: {self.about}'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f"about={self.about}, "
            f"coins={self.coins}, "
            f"posts={self.posts}, "
            f")>"
        )
