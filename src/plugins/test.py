from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment
import random

num=on_command("num")
@num.handle()
async def num_handle(event: MessageEvent, args: Message = CommandArg()):
    random.seed(int(args.extract_plain_text()))
    await num.reject(MessageSegment.reply(event.message_id) + MessageSegment.text(str(random.randint(1, 1000))))

@num.handle()
async def num_handle_for(event: MessageEvent):
    if event.message.extract_plain_text() is "cancel":
        await num.finish("1")
    else:
        await num.reject(MessageSegment.reply(event.message_id) + MessageSegment.text(str(random.randint(1, 1000))))
