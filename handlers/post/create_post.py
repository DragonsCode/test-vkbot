from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text

from models.db_api import methods as db
from states import PostData, ctx

bot = Blueprint('create_post')

@bot.on.private_message(lev='Create post')
async def create_post(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('Name'))
    keyboard.add(Text('Age'))
    keyboard.add(Text('Category'))
    keyboard.add(Text('About'))

    
    user = await db.get_user(id=message.peer_id)

    ctx.set(message.peer_id, {})

    if user is None:
        keyboard = Keyboard(one_time=True)
        keyboard.add(Text('reg'))

        await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
        return

    await message.answer('Choose the category for your post')
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


@bot.on.private_message(state=PostData.TITLE)
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

    return 'Post was successfully created!\nHere it is:\n\nCategory: {category}\nTitle: {title}\nPost: {text}'