from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models.db_api import methods as db

bot = Blueprint('profile')

@bot.on.private_message(text='Profile')
async def get_coins(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Back', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text('Change profile'))
    
    user = await db.get_user(id=message.peer_id)

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))
        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return

    await message.answer(str(user), keyboard=keyboard)