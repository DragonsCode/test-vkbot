import asyncio

from vkbottle.bot import Message
from vkbottle import load_blueprints_from_package
'''from vkbottle.modules import json
from vkbottle import Keyboard, KeyboardButtonColor, Callback, \
                        Text, OpenLink, Location, EMPTY_KEYBOARD, \
                        template_gen, TemplateElement, \
                        GroupEventType, GroupTypes, VKAPIError, \
                        CtxStorage, BaseStateGroup,\
                        PhotoMessageUploader, DocMessagesUploader, VoiceMessageUploader, \
                        load_blueprints_from_package'''

from models.database import async_db_session
from config import token, bot, scheduler, ioloop
from middlewares.db_timer import InfoMiddleware
from tasks.notify import notify_schedule
from tasks.send_post import post_schedule
from tasks.bonus import bonus_schedule


scheduler.start()

for bp in load_blueprints_from_package('handlers'):
    bp.load(bot)



@bot.on.private_message()
async def chat(message: Message):
    await message.answer('Type "menu"')
    await message.answer(f'Here is the message object: {message}')


async def init_app():
    await async_db_session.init()
    await async_db_session.create_all()

async def main():
    await init_app()

def run_main():
    ioloop.run_until_complete(main())
    notify_schedule()
    bonus_schedule()
    post_schedule()
    #ioloop.close()

run_main()

bot.labeler.message_view.register_middleware(InfoMiddleware)

bot.run_forever()


