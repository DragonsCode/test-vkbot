from vkbottle.bot import Blueprint, Message
from vkbottle.modules import json
from vkbottle import Keyboard, Callback, \
                        GroupEventType, GroupTypes

bot = Blueprint('callback_kb')


@bot.on.private_message(text='callback')
async def callback(message: Message):
    keyboard = (
        Keyboard(inline=True)
        .add(Callback('Click', {'call_1': 'click'}))
        .add(Callback('Click 2', {'call_1': 'click2'}))
    )

    await message.answer('callback', keyboard=keyboard)


@bot.on.raw_event(GroupEventType.MESSAGE_EVENT, dataclass=GroupTypes.MessageEvent)
async def message_event(event: GroupTypes.MessageEvent):
    if event.object.payload['call_1'] == 'click':
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'You are awesome!'})
        )
    elif event.object.payload['call_1'] == 'click2':
        await bot.api.messages.send_message_event_answer(
            event_id=event.object.event_id,
            peer_id=event.object.peer_id,
            user_id=event.object.user_id,
            event_data=json.dumps({'type': 'show_snackbar', 'text': 'You are not awesome :('})
        )