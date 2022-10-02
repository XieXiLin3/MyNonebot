from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent, GroupMessageEvent, Bot, MessageSegment, Message

exit_group=on_command("exit_group", aliases={"group_exit", "退出群组", "退群", "退出群聊"}, permission=SUPERUSER)
@exit_group.handle()
async def exit_handle(bot: Bot, event: MessageEvent, args: Message=CommandArg()):
    arg=args.extract_plain_text()
    gl=await bot.get_group_list()
    list=[]
    for i in gl:
        list.append(str(i['group_id']))
    if arg == "":
        if isinstance(event, GroupMessageEvent):
            await exit_group.send(MessageSegment.reply(event.message_id) + MessageSegment.text("收到，我将自动退出此群组。"))
            await bot.set_group_leave(group_id=event.group_id, is_dismiss=False)
        else:
            await exit_group.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("当前聊天环境不在群里，需要指定 group_id 。"))
    else:
        if arg in list:
            await exit_group.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"收到，我将尝试退出群组 {arg}。"))
            await bot.set_group_leave(group_id=int(arg), is_dismiss=False)
        else:
            await exit_group.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"我不在群组 {arg}。"))