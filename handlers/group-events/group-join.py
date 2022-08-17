from vkbottle.bot import Blueprint, Message
from vkbottle import GroupEventType, GroupTypes, VKAPIError

bot = Blueprint('group_join')


@bot.on.raw_event(GroupEventType.GROUP_JOIN, dataclass=GroupTypes.GroupJoin)
async def group_join(event: GroupTypes.GroupJoin):
    try:
        await bot.api.messages.send(
            peer_id=event.object.user_id,
            message='You have joined to our group!',
            random_id=0
        )
    except VKAPIError(901):
        pass