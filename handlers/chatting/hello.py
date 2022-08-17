from vkbottle.bot import Blueprint, Message

bot = Blueprint('hello')


@bot.on.private_message(text=['Hello <name>', 'Hello'])
async def hello(message: Message, name=None):
    if name is not None:
        await message.answer(f'Hello to {name}')
    else:
        user = await bot.api.users.get(message.from_id)
        await message.answer(f'Hello {user[0].first_name} {user[0].last_name}')
