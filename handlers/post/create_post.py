from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models.db_api import methods as db
from states import PostData, ctx

bot = Blueprint('create_post')

@bot.on.private_message(lev='Create post')
async def create_post(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('News'))
    keyboard.add(Text('Gaming'))
    keyboard.add(Text('IT'))
    keyboard.add(Text('Economy'))

    
    user = await db.get_user(id=message.peer_id)

    ctx.set(message.peer_id, {})

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))

        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return
    elif user.coins < 1:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('Back', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

        await message.answer('You do not have enough coins!\nRemember that creating one post will cost you one coin', keyboard=keyboard)
        return
    
    await db.edit_user(
        id=user.id,
        name=user.name,
        age=user.age,
        about=user.about,
        coins=user.coins-1,
        category=user.category,
        bonus=user.bonus
    )

    await message.answer('Choose the category for your post', keyboard=keyboard)
    await bot.state_dispenser.set(message.peer_id, PostData.CATEGORY)


@bot.on.private_message(state=PostData.CATEGORY)
async def post_category(message: Message):
    if message.text in ['News', 'Gaming', 'IT', 'Economy']:
        data = ctx.get(message.peer_id)
        data['category'] = message.text
        ctx.set(message.peer_id, data)
        await bot.state_dispenser.set(message.peer_id, PostData.TITLE, category=message.text)
        await message.answer('Enter title of your post')
    else:
        #await bot.state_dispenser.set(message.peer_id, PostData.CATEGORY)
        return 'Choose from keyboard'


@bot.on.private_message(state=PostData.TITLE)
async def post_title(message: Message):
    if len(message.text) > 100:
        await message.answer('The title should not be longer than 100 characters')
        return
    
    data = ctx.get(message.peer_id)
    data['title'] = message.text
    ctx.set(message.peer_id, data)
    await bot.state_dispenser.set(message.peer_id, PostData.TEXT, title=message.text)
    return 'Enter the text for your post'


@bot.on.private_message(state=PostData.TEXT)
async def post_title(message: Message):
    if len(message.text) > 1000:
        await message.answer('The text should not be longer than 1000 characters')
        return
    
    data = ctx.get(message.peer_id)
    category = data['category']
    title = data['title']
    text = message.text

    user = await db.get_user(id=message.peer_id)

    await db.create_post(
        peer=user.num,
        title=title,
        data=text,
        category=category
    )
    await bot.state_dispenser.delete(message.peer_id)

    return f'Post was successfully created!\nHere it is:\n\nCategory: {category}\nTitle: {title}\nPost: {text}'