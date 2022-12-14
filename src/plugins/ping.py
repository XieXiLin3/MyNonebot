from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

ping=on_command("ping", aliases={"Ping", "呼叫", "在线", "check"})
@ping.handle()
async def ping_handle(event: MessageEvent):
    await ping.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("Pong!"))
