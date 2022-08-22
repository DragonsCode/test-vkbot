from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models.db_api import methods as db

bot = Blueprint('my_posts')

@bot.on.private_message(text='My posts')
@bot.on.private_message(payload={'cmd': 'my_posts'})
async def create_post(message: Message):
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Create post'))
    keyboard.add(Text('Back', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    

    user = await db.get_user(id=message.peer_id)

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))

        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return
    
    posts = await db.get_post(peer=user.num)
    text = ''

    for i, e in enumerate(posts, 1):
        text += f'{i}. {e.title}\n'
    
    if text == '':
        await message.answer('No posts found', keyboard=keyboard)
        return
    text+='\ntype "Show post <num>" to open post\ntype "Change post <num>" to change post\ntype "Delete post <num>" to delete post\n'
    await message.answer(text, keyboard=keyboard)


