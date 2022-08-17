from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text

bot = Blueprint('inline_kb')


@bot.on.private_message(text='inline')
async def inline(message: Message):
    keyboard = (
        Keyboard(inline=True)
        .add(Text('Button1'))
        .add(Text('Button2'))
    )

    await message.answer('Inline', keyboard=keyboard)