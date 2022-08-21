from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text

from models.db_api import methods as db

bot = Blueprint('my_posts')

@bot.on.private_message(text='My posts')
async def create_post(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Create post'))
    

    user = await db.get_user(id=message.peer_id)

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))

        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return
    
    posts = await db.get_post(peer=user.num)
    text = ''

    for i, e in enumerate(posts):
        text += f'{i}. {e.title}\n'
    
    if text == '':
        await message.answer('No posts found', keyboard=keyboard)
        return
    
    await message.answer(text, keyboard=keyboard)


