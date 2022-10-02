from email import message
from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment

get_glist=on_command("get_group_list", aliases={"get_glist", "getgrouplist", "getgroup", "ggl", "获取群组列表", "获取群聊列表", "获取群列表"}, permission=SUPERUSER)
@get_glist.handle()
async def ggi_handle(bot: Bot, event: MessageEvent):
    list=await bot.get_group_list()
    list=[]
    for i in list:
        list.append(str(i['group_id']))
    await get_glist.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(", ".join(list)))