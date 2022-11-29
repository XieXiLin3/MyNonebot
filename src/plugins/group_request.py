from nonebot import on_notice, on_command
from nonebot.permission import SUPERUSER
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageSegment, GroupRequestEvent, Event, Bot, GROUP_OWNER, GROUP_ADMIN, GroupMessageEvent, Message
import re, os, json

def _check(event: Event):
    return isinstance(event, GroupRequestEvent)

request=on_notice(rule=_check)
@request.handle()
async def request_handle(event: GroupRequestEvent, bot: Bot):
    # -----========== 文件判断 ==========----- #
    if os.path.exists("./config/group_request_config.json"):
        with open("./config/group_request_config.json", "r") as f:
            file=f.read()
            f.close()
        config=json.loads(file)
    else:
        os.mkdir("config")
        config=[{"768176998": { "enable": True, "need_review": False, "answer": "", "allow_invite": True }}]
        file=json.dumps(config)
        with open("./config/group_request_config.json", "w") as f:
            f.write(file)
            f.close()
    # -----========== 文件判断 ==========----- #
    group_id=event.group_id
    user_id=event.user_id
    commect=event.comment
    answer = re.findall(re.compile('答案：(.*)'), commect)[0]
    type=event.sub_type
    # -----========== 逻辑判断 ==========----- #
    if group_id not in config or (config[group_id]["enable"] is False):
        await request.finish()
    else:
        if type is "add":
            if config[group_id]["need_review"] is False:
                await request.send(MessageSegment.text(f"[√] 有新同学 ") + MessageSegment.at(user_id=user_id) + MessageSegment.text(f" 申请加入本群聊，已自动同意！"))
                await event.approve(bot=bot)
                await request.finish()
            else:
                if str(answer) is str(config[group_id]["answer"]):
                    await request.send(MessageSegment.text(f"[√] 有新同学 ") + MessageSegment.at(user_id=user_id) + MessageSegment.text(f" 申请加入本群聊，答案正确！ ({answer})"))
                    await event.approve(bot=bot)
                    await request.finish()
                else:
                    await request.finish(MessageSegment.text(f"[X] 有新同学 ") + MessageSegment.at(user_id=user_id) + MessageSegment.text(f" 申请加入本群聊，但答案不正确（忽略）！ ({answer})"))
        else:
            if config[group_id]["allow_invite"]:
                await request.send(MessageSegment.text(f"[√] 有新同学被邀请加入本群聊，已自动同意！"))
                await event.approve(bot=bot)
                await request.finish()
            else:
                await request.finish(MessageSegment.text(f"[X] 有新同学被邀请加入本群聊，但不会自动同意！"))
    # -----========== 逻辑判断 ==========----- #
    
set_enable=on_command("set_group_join_config", aliases={"设置加群配置"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
@set_enable.handle()
async def set_enable_handle(bot: Bot, event: GroupMessageEvent, command: Message=CommandArg()):
    # # -----========== 文件判断 ==========----- #
    # if os.path.exists("./config/group_request_config.json"):
    #     with open("./config/group_request_config.json", "r") as f:
    #         file=f.read()
    #         f.close()
    #     config=json.loads(file)
    # else:
    #     os.mkdir("config")
    #     config=[{"768176998": { "enable": True, "need_review": False, "answer": "", "allow_invite": True }}]
    #     file=json.dumps(config)
    #     with open("./config/group_request_config.json", "w") as f:
    #         f.write(file)
    #         f.close()
    # # -----========== 文件判断 ==========----- #
    # arg=command.extract_plain_text()
    # args=arg.split(" ")
    # group_id=event.group_id
    await set_enable.finish(MessageSegment.reply(event.message_id) + MessageSegment.text("功能尚未支持！"))