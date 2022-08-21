from unicodedata import category
from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text

from states import RegData, ctx
from models.db_api import methods as db


bot = Blueprint('registration')


@bot.on.private_message(lev='reg')
async def reg(message: Message):
    user = await db.get_user(id=message.peer_id)

    if user is not None:
        await message.answer('You already have an account')
        return
    
    ctx.set(message.peer_id, {})
    await bot.state_dispenser.set(message.peer_id, RegData.NAME)
    return 'Enter your name'


@bot.on.private_message(state=RegData.NAME)
async def name(message: Message):
    if len(message.text) > 100:
        await message.answer('Your name should not be longer than 100 characters')
        return
    
    data = ctx.get(message.peer_id)
    data['name'] = message.text
    ctx.set(message.peer_id, data)
    await bot.state_dispenser.set(message.peer_id, RegData.AGE, name=message.text)
    return 'Enter your age'


@bot.on.private_message(state=RegData.AGE)
async def age(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('News'))
    keyboard.add(Text('Gaming'))
    keyboard.add(Text('IT'))
    keyboard.add(Text('Economy'))


    if message.text.isdigit() and int(message.text) > 14 and int(message.text) < 100:
        data = ctx.get(message.peer_id)
        data['age'] = int(message.text)
        ctx.set(message.peer_id, data)
        await bot.state_dispenser.set(message.peer_id, RegData.CATEGORY, age=message.text)
        await message.answer('choose the interesting category', keyboard=keyboard)
    else:
        #await bot.state_dispenser.set(message.peer_id, RegData.AGE)
        return 'Enter your age correctly, from 15 to 99'


@bot.on.private_message(state=RegData.CATEGORY)
async def age(message: Message):
    if message.text in ['News', 'Gaming', 'IT', 'Economy']:
        data = ctx.get(message.peer_id)
        data['category'] = message.text
        ctx.set(message.peer_id, data)
        await bot.state_dispenser.set(message.peer_id, RegData.ABOUT, category=message.text)
        await message.answer('Enter something about yourself')
    else:
        #await bot.state_dispenser.set(message.peer_id, RegData.AGE)
        return 'Choose from keyboard'


@bot.on.private_message(state=RegData.ABOUT)
async def about(message: Message):
    if len(message.text) > 500:
        await message.answer('Too long, you should use no more than 500 characters')
        return
    
    data = ctx.get(message.peer_id)
    name = data['name']
    age = data['age']
    category = data['category']
    about = message.text


    await db.create_user(
        id=message.peer_id,
        name=name,
        age=age,
        about=about,
        category=category
    )

    await bot.state_dispenser.delete(message.peer_id)

    await message.answer(f'{name}, You have successfully passed registration!')
    return f'Here is your profile:\n\nName: {name}\nAge: {age}\nAbout: {about}\nInterested in: {category}'