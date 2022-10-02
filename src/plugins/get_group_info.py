from email import message
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

get_ginfo=on_command("get_group_info", aliases={"get_ginfo", "getgroupinfo", "getgroup", "ggi", "gg", "获取群组信息", "获取群聊信息", "获取群信息"}, permission=SUPERUSER)
@get_ginfo.handle()
async def ggi_handle(bot: Bot, event: MessageEvent):
    info=await bot.get_group_list()
    list=[]
    for i in info:
        list.append(i['group_id'])
    await get_ginfo.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(",".join(list)))