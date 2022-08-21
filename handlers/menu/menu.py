from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

from models.db_api import methods as db

bot = Blueprint('main_menu')


@bot.on.private_message(text='menu')
@bot.on.private_message(payload={'cmd': 'menu'})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('My posts'))
    
    keyboard.add(Text('Store', {'cmd': 'store'}))

    keyboard.add(Text('Profile'))

    await message.answer('Menu', keyboard=keyboard)


@bot.on.private_message(text='menu')
@bot.on.private_message(payload={'cmd': 'store'})
async def store(message: Message):
    keyboard = Keyboard(one_time=True)

    keyboard.add(Text('Get coins'), color=KeyboardButtonColor.POSITIVE)

    keyboard.row()
    
    keyboard.add(Text('Back', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)

    await message.answer('Store', keyboard=keyboard)


@bot.on.private_message(text='Get coins')
async def get_coins(message: Message):
    in_group = await bot.api.groups.is_member(188552039, message.from_id)
    keyboard = Keyboard(one_time=True).add(Text('Back', {'cmd': 'store'}), color=KeyboardButtonColor.NEGATIVE)
    user = await db.get_user(id=message.peer_id)
    if in_group:
        if user is None:
            keyboard.add(Text('reg'))
            await message.answer('You are not registered, type "reg" to start the registration', keyboard=keyboard)
            return
        
        if not user.bonus:
            await db.edit_user(
                    id=user.id,
                    name=user.name,
                    age=user.age,
                    about=user.about,
                    coins=user.coins+1,
                    bonus=1
                    )
            await message.answer('You got 1 coin', keyboard=keyboard)
            return

        await message.answer('Retry later', keyboard=keyboard)

    else:
        await message.answer('You are not in group', keyboard=keyboard)