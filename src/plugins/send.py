from nonebot import on_command
from nonebot.permission import SUPERUSER
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment, Bot
import os

cancel_word=["取消", "取消发送", "cancel", "Cancel"]
group_word=["群组", "讨论组", "group", "Group", "群"]
private_word=["好友", "私聊", "私信", "私", "private", "Private", "friend", "Friend"]

send=on_command("send", aliases={"发送", "发送消息", "传送消息"}, permission=SUPERUSER)
@send.handle()
async def send_wait(event: MessageEvent, bot: Bot):
    os.environ['select']=""
    os.environ['id']=""
    await send.pause(MessageSegment.reply(event.message_id) + MessageSegment.text("请选择发送的类型 (group / private)。"))

@send.handle()
async def send_select(event: MessageEvent, bot: Bot):
    logger.info(f"用户 {event.user_id} 选择类型: <{event.message.extract_plain_text()}>")
    if event.message.extract_plain_text() in cancel_word:
         await send.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("已取消发送。"))
    else:
        if event.message.extract_plain_text() in group_word:
            os.environ['select']="group"
        elif event.message.extract_plain_text() in private_word:
            os.environ['select']="private"
        else:
            await send.reject(MessageSegment.reply(event.message_id) + MessageSegment.text(f"无法判断 ({event.message.extract_plain_text()}), 请重新选择发送的类型 (group / private)。"))
        await send.pause(MessageSegment.reply(event.message_id) + MessageSegment.text(f"选择了 {os.environ['select']} , 请继续发送需要发送到的 群号 / QQ号 。"))

@send.handle()
async def send_set(event: MessageEvent, bot: Bot):
    logger.info(f"用户 {event.user_id} 选择发送到: {event.message.extract_plain_text()}")
    if event.message.extract_plain_text() in cancel_word:
        await send.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("已取消发送。"))
    else:
        os.environ['id']=event.message.extract_plain_text()
        await send.pause(MessageSegment.reply(event.message_id) + MessageSegment.text(f"已设定发送到 {os.environ['id']} , 请继续发送需要发送的消息。"))

@send.handle()
async def send_send(event: MessageEvent, bot: Bot):
    logger.info(f"用户 {event.user_id} 选择发送: {event.message.extract_plain_text()}")
    logger.info(f"汇总: 用户 {event.user_id} 选择发送到 {os.environ['id']} ({os.environ['select']}): {event.message.extract_plain_text()}")
    if event.message.extract_plain_text() in cancel_word:
        await send.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("已取消发送。"))
    else:
        if os.environ['select'] == "group":
            await bot.send_msg(message_type=os.environ['select'], group_id=int(os.environ['id']), message=event.message)
        elif os.environ['select'] == "private":
            await bot.send_msg(message_type=os.environ['select'], user_id=int(os.environ['id']), message=event.message)
        else:
            await send.finish(MessageSegment.text("我去, 非法请求!"))
        await send.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"已成功向 {os.environ['id']} ({os.environ['select']}) 发送消息。"))
