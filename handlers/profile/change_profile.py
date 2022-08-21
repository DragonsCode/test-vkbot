from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text

from states import ChangeData, ctx
from models.db_api import methods as db


bot = Blueprint('change_profile')


@bot.on.private_message(lev='Change profile')
async def choose_change(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('Name'))
    keyboard.add(Text('Age'))
    keyboard.add(Text('Category'))
    keyboard.add(Text('About'))

    user = await db.get_user(id=message.peer_id)

    if user is None:
        await message.answer('You do not have an account')
        return
    
    ctx.set(message.peer_id, {})
    await bot.state_dispenser.set(message.peer_id, ChangeData.WHAT)
    await message.answer('What do you want to change?', keyboard=keyboard)


@bot.on.private_message(state=ChangeData.WHAT)
async def enter_change(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('News'))
    keyboard.add(Text('Gaming'))
    keyboard.add(Text('IT'))
    keyboard.add(Text('Economy'))


    data = ctx.get(message.peer_id)
    data['what'] = message.text.lower()
    ctx.set(message.peer_id, data)
    if message.text in ['Name', 'Age', 'About']:
        await message.answer(f'Enter your {message.text.lower()}')
        await bot.state_dispenser.set(message.peer_id, ChangeData.CHANGE)
    elif message.text == 'Category':
        await message.answer(f'Choose your {message.text.lower()}', keyboard=keyboard)
    else:
        await message.answer('Please choose from keyboard')


@bot.on.private_message(state=ChangeData.CHANGE)
async def change(message: Message):
    data = ctx.get(message.peer_id)
    what = data['what']
    user = await db.get_user(id=message.peer_id)
    text = f'Your {what} has been changed to {message.text}'
    if what == 'name':
        if len(message.text) > 100:
            await message.answer('Your name should not be longer than 100 characters')
            return
        
        await db.change_user(
            id=user.id,
            name=message.text,
            age=user.age,
            about=user.about,
            coins=user.coins,
            category=user.category,
            bonus=user.bonus
            )
        await bot.state_dispenser.delete(message.peer_id)
        return text
    elif what == 'age':
        if message.text.isdigit() and int(message.text) > 14 and int(message.text) < 100:
            await db.change_user(
                id=user.id,
                name=user.name,
                age=int(message.text),
                about=user.about,
                coins=user.coins,
                category=user.category,
                bonus=user.bonus
                )
            await bot.state_dispenser.delete(message.peer_id)
            return text
        else:
            return 'Enter your age correctly, from 15 to 99'
    elif what == 'about':
        if len(message.text) > 500:
            await message.answer('Too long, you should use no more than 500 characters')
            return
        
        await db.change_user(
            id=user.id,
            name=user.name,
            age=user.age,
            about=message.text,
            coins=user.coins,
            category=user.category,
            bonus=user.bonus
            )
        await bot.state_dispenser.delete(message.peer_id)
        return text
    elif what == 'category':
        if message.text not in ['News', 'Gaming', 'IT', 'Economy']:
            await message.answer('Choose from keyboard')
        
        await db.change_user(
            id=user.id,
            name=user.name,
            age=user.age,
            about=user.about,
            coins=user.coins,
            category=message.text,
            bonus=user.bonus
            )
        await bot.state_dispenser.delete(message.peer_id)
        return text