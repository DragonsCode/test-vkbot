from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

bot = Blueprint('main_menu')


@bot.on.private_message(text='menu')
@bot.on.private_message(payload={'cmd': 'menu'})
async def menu(message: Message):
    keyboard = Keyboard(one_time=True).add(Text('Store', {'cmd': 'store'}))

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
    keyboard = Keyboard(one_time=True).add(Text('Back', {'cmd': 'menu'}), color=KeyboardButtonColor.NEGATIVE)
    await message.answer('Very soon...', keyboard=keyboard)