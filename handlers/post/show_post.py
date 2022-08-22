from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models.db_api import methods as db

bot = Blueprint('show_post')

@bot.on.private_message(text='Show post <ind>')
async def create_post(message: Message, ind=None):
    if ind is None:
        await message.answer('Please use command correctly: "Show post <num>')
        return
    keyboard = Keyboard(one_time=True)
    keyboard.add(Text('Create post'))
    keyboard.add(Text('Back', {'cmd': 'my_posts'}), color=KeyboardButtonColor.NEGATIVE)
    

    user = await db.get_user(id=message.peer_id)

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))

        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return
    
    posts = await db.get_post(peer=user.num)

    if ind.isdigit() and int(ind) > 0 and int(ind) <= len(posts):
        index = int(ind)-1
        post = posts[index]

        await message.answer(f'{str(post)}')
    else:
        await message.answer(f'No post found for number {ind}')