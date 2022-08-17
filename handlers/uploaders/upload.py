from vkbottle.bot import Blueprint, Message
from vkbottle import PhotoMessageUploader, DocMessagesUploader, VoiceMessageUploader

bot = Blueprint('uploaders')

@bot.on.private_message(text='up')
async def upload(message: Message):
    photo_upd = PhotoMessageUploader(bot.api)
    doc_upd = DocMessagesUploader(bot.api)
    voice_upd = VoiceMessageUploader(bot.api)

    photo = await photo_upd.upload('logo.jpg')
    doc = await doc_upd.upload('script.txt', 'doc.txt', peer_id=message.peer_id)
    voice = await voice_upd.upload('1.wav', 'voice.wav', peer_id=message.peer_id)

    await message.answer(attachment=photo)
    await message.answer(attachment=doc)
    await message.answer(attachment=voice)