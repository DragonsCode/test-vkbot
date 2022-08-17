from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, \
                        Text, OpenLink, Location, EMPTY_KEYBOARD

bot = Blueprint('simple_kb')


@bot.on.private_message(text='keyboard')
async def keyboard(message: Message):
    keyboard = Keyboard()

    keyboard.add(Text('RED'), color=KeyboardButtonColor.NEGATIVE)
    keyboard.add(Text('GREEN'), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('BLUE'), color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text('SECONDARY'), color=KeyboardButtonColor.SECONDARY)

    keyboard.row()

    keyboard.add(Text('WHITE'))

    keyboard.row()

    keyboard.add(OpenLink('https://google.com/', 'Go to Google'))
    keyboard.add(Location())

    await message.answer('Keyboard', keyboard=keyboard)


@bot.on.private_message(text='no board')
async def no_board(message: Message):
    await message.answer('No board', keyboard=EMPTY_KEYBOARD)