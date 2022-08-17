from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text, \
                        template_gen, TemplateElement

bot = Blueprint('carousel')


@bot.on.private_message(text='carousel')
async def carousel(message: Message):
    keyboard = Keyboard().add(Text('Do not click!'), color=KeyboardButtonColor.NEGATIVE)
    carousel = template_gen(
        TemplateElement(
            'Some title',
            'With no description',
            None,
            keyboard.get_json()
        )
    )
    await message.answer('Carousel', template=carousel)