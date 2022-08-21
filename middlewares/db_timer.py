from vkbottle import BaseMiddleware
from vkbottle.bot import Message

from datetime import datetime
from models.db_api import methods as db

class InfoMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if not self.handlers:
            self.stop("Сообщение не было обработано")
        
        user = await db.get_user(id=self.event.peer_id)
        await db.edit_user(
            id=user.id,
            name=user.name,
            age=user.age,
            about=user.about,
            coins=user.coins,
            category=user.category,
            bonus=user.bonus
        )

        '''await self.event.answer(
            "Сообщение было обработано:\n\n"
            f'peer - {self.event.peer_id}\n\n'
            f"View - {self.view}\n\n"
            f"Handlers - {self.handlers}"
        )'''