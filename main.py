from vkbottle.bot import Bot, Message
from vkbottle import load_blueprints_from_package
'''from vkbottle.modules import json
from vkbottle import Keyboard, KeyboardButtonColor, Callback, \
                        Text, OpenLink, Location, EMPTY_KEYBOARD, \
                        template_gen, TemplateElement, \
                        GroupEventType, GroupTypes, VKAPIError, \
                        CtxStorage, BaseStateGroup,\
                        PhotoMessageUploader, DocMessagesUploader, VoiceMessageUploader, \
                        load_blueprints_from_package'''

from config import token
from middlewares.db_timer import InfoMiddleware

bot = Bot(token=token)

for bp in load_blueprints_from_package('handlers'):
    bp.load(bot)



@bot.on.private_message()
async def chat(message: Message):
    await message.answer(message.text)
    await message.answer(f'Here is the message object: {message}')


bot.labeler.message_view.register_middleware(InfoMiddleware)

bot.run_forever()



