from vkbottle.bot import Blueprint, Message
from vkbottle import GroupEventType, GroupTypes, VKAPIError

bot = Blueprint('group_leave')


@bot.on.raw_event(GroupEventType.GROUP_LEAVE, dataclass=GroupTypes.GroupLeave)
async def group_leave(event: GroupTypes.GroupLeave):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message='You have leaved our group!',
            random_id=0
        )
    except VKAPIError(901):
        pass