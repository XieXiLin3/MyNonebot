from nonebot import on_request
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import GroupRequestEvent, MessageSegment, Bot, Event
import json, requests, re

mojang_verify_groups=[316052940]
auto_allow_groups=[768176998]
allow_do_not_minecraft=True

def check(event: Event):
    return isinstance(event, GroupRequestEvent)

def getQQName(QID: int) -> str:
    url=f"https://users.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={QID}"
    headers={
        "Referer": "https://skin.cakemc.top/",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    resp=requests.get(url=url, headers=headers).text
    resp=resp.encode("iso-8859-1").decode("gbk").split(",")[6]
    resp=re.findall("\"(.*?)\"", resp)[0]
    return resp

def Request_Mojang_API(name: str):
    resp=requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    return resp
    
request_app=on_request(rule=check)
async def request_app_handle(bot: Bot, event: GroupRequestEvent):
    if event.group_id in auto_allow_groups or event.group_id in mojang_verify_groups:
        raw=json.loads(event.json())
        sub_type=raw["sub_type"]
        comment=raw["comment"]
        if sub_type == "add":
            answer=str(re.findall(re.compile('答案：(.*)'), comment)[0])
            await request_app.send(MessageSegment.text(f"[i] Group Add Request: {getQQName(event.user_id)} ({event.user_id})\nAnswer: {answer}"))
            logger.info(f"[i] Group Add Request: {getQQName(event.user_id)} ({event.user_id}), Answer: {answer}")
        elif sub_type == "invite":
            await request_app.send(MessageSegment.text(f"[i] Group Invite Request: {getQQName(event.user_id)} ({event.user_id}), Message: {event.comment}"))
            logger.info(f"[i] Group Invite Request: {getQQName(event.user_id)} ({event.user_id}), Message: {event.comment}")
        if event.group_id in auto_allow_groups:
            await request_app.send(MessageSegment.text("在自动同意列表内, 自动同意入群申请!"))
            await event.approve(bot=bot)
            await request_app.finish(MessageSegment.text("欢迎新人!"))
        if event.group_id in mojang_verify_groups:
            if sub_type == "invite":
                await request_app.send(MessageSegment.text("是邀请, 自动同意!"))
                await event.approve(bot=bot)
                await request_app.finish(MessageSegment.text("欢迎新人!"))
            elif sub_type == "add":
                if answer == "无正版":
                    if allow_do_not_minecraft:
                        await request_app.send(MessageSegment.text("无正版 在 允许范围!"))
                        await event.approve(bot=bot)
                        await request_app.finish("欢迎新人!")
                    else:
                        await event.reject(bot=bot, reason="不能没有正版哦!")
                        await request_app.finish(MessageSegment.text("未开启 允许没有正版的人 加入服务器, 已拒绝!"))
                else:
                    r=Request_Mojang_API(answer)
                    if r.status_code == 204:
                        if allow_do_not_minecraft:
                            await event.reject(bot=bot, reason="用户名不正确! 如果你没有正版请直接回答 无正版")
                            await request_app.finish(MessageSegment.text("无法验证, 已拦截! (可通过回答 无正版 直接加群)"))
                        else:
                            await event.reject(bot=bot, reason="用户名不正确!")
                            await request_app.finish(MessageSegment.text("无法验证, 已拦截!"))
                    elif r.status_code == 200:
                        user_info=json.loads(r.text)
                        await request_app.send(f"能够验证!\n{user_info['name']} ({user_info['id']})")
                        await event.approve(bot=bot)
                        await request_app.finish(MessageSegment.text("欢迎新人!"))
                    else:
                        await request_app.finish(MessageSegment.text(f"未知的状态码 ({r.status_code})!\n{r.text}"))
