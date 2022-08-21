from unicodedata import category
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sqlalchemy.future import select

from models.model_admin import ModelAdmin
from models.database import Base, async_db_session


class User(Base, ModelAdmin):
    __tablename__ = "users"

    num = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer)
    name = Column(String(100))
    age = Column(Integer)
    about = Column(String(500))
    coins = Column(Integer)
    posts = relationship("Post")
    category = Column(String(100))
    bonus = Column(Integer, default=0)
    last_time = Column(DateTime)

    # required in order to acess columns with server defaults
    # or SQL expression defaults, subsequent to a flush, without
    # triggering an expired load
    #__mapper_args__ = {"eager_defaults": True}

    def __str__(self):
        return f'Name: {self.name}\nAge: {self.age}\nBalance: {self.coins} coins\nAbout: {self.about}\nInterested in: {self.category}'

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id={self.id}, "
            f"full_name={self.name}, "
            f"about={self.about}, "
            f"coins={self.coins}, "
            f"category={self.category}"
            #f"posts={self.posts}, "
            f")>"
        )
