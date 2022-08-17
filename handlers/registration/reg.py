from vkbottle.bot import Blueprint, Message

from states import RegData, ctx


bot = Blueprint('registration')


@bot.on.private_message(lev='reg')
async def reg(message: Message):
    ctx.set(message.peer_id, {})
    await bot.state_dispenser.set(message.peer_id, RegData.NAME)
    return 'Enter your name'


@bot.on.private_message(state=RegData.NAME)
async def name(message: Message):
    data = ctx.get(message.peer_id)
    data['name'] = message.text
    ctx.set(message.peer_id, data)
    await bot.state_dispenser.set(message.peer_id, RegData.AGE, name=message.text)
    return 'Enter your age'


@bot.on.private_message(state=RegData.AGE)
async def age(message: Message):
    if message.text.isdigit() and int(message.text) > 14 and int(message.text) < 100:
        data = ctx.get(message.peer_id)
        data['age'] = int(message.text)
        ctx.set(message.peer_id, data)
        await bot.state_dispenser.set(message.peer_id, RegData.ABOUT, age=message.text)
        return 'Enter about yourself'
    else:
        #await bot.state_dispenser.set(message.peer_id, RegData.AGE)
        return 'Enter your age correctly, from 15 to 99'


@bot.on.private_message(state=RegData.ABOUT)
async def about(message: Message):
    data = ctx.get(message.peer_id)
    name = data['name']
    age = data['age']
    about = message.text

    await bot.state_dispenser.delete(message.peer_id)

    await message.answer(f'{name}, You have successfully passed registration!')
    return f'Here is your profile:\n\nName: {name}\nAge: {age}\nAbout: {about}'