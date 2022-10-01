import json
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent, Bot
import requests

api_key="MSS-ServerTap-Key-XieXiLin158"
server_api_urls=["http://10.147.20.1:3003/", "http://10.147.20.1:3002/", "http://10.147.20.1:3001/"]
allow_group_ids=[316052940]

headers={
    "accept": "application/json",
    "key": api_key
}

def seconds_to_time(s: int) -> str:
    m, s=divmod(s, 60)
    h, m=divmod(m, 60)
    d, h=divmod(h, 24)
    return f"{d}天 {h}时 {m}分 {s}秒"

def get_server_info(url: str):
    return json.loads(requests.get(f"{url}v1/server", headers=headers).text)

info=on_command("info", aliases={"i", "服务器信息", "服务器状态", "serverinfo", "server_info"})
@info.handle()
async def info_handle(bot: Bot, event: GroupMessageEvent):
    if (event.group_id in allow_group_ids) or (event.get_user_id() in bot.config.superusers.copy()):
        info_message=""
        count=0
        max_players=0
        online_players=0
        for url in server_api_urls:
            resp=get_server_info(url)
            await info.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{count+1}周目 状态:\n服务端名称: {resp['name']} ;\n服务端版本: {resp['version']} ;\nTPS: {resp['tps']} ;\n已启动时间: {seconds_to_time(resp['health']['uptime'])} ;\n最大在线玩家: {resp['maxPlayers']} ;\n在线玩家数: {resp['onlinePlayers']}。"))
            max_players+=int(resp['maxPlayers'])
            online_players+=int(resp['onlinePlayers'])
            count+=1
        await info.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"总最大在线数量: {max_players}, 总在线数量: {online_players}。"))

tps=on_command("tps")
@tps.handle()
async def tps_handle(bot: Bot, event: GroupMessageEvent):
    if (event.group_id in allow_group_ids) or (event.get_user_id() in bot.config.superusers.copy()):
        tpss=0.0
        count=0
        for url in server_api_urls:
            resp=get_server_info(url)
            await tps.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{count+1}周目 的 TPS 为 {resp['tps']}。"))
            tpss+=float(resp["tps"])
            count+=1
        tpss=tpss/count
        await tps.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"TPS 平均值 为 {tpss}。"))

list=on_command("list", aliases={"l", "在线", "在线人数"})
@list.handle()
async def list_handle(bot: Bot, event: GroupMessageEvent):
    if (event.group_id in allow_group_ids) or (event.get_user_id() in bot.config.superusers.copy()):
        players=0
        ops=0
        count=0
        for url in server_api_urls:
            message=""
            resp=json.loads(requests.get(f"{url}v1/players", headers=headers).text)
            for i in resp:
                if i['op'] == True:
                    ops+=1
                    message+=f"[OP]{i['displayName']} ({i['dimension']}, {i['gamemode']})\n"
                else:
                    message+=f"{i['displayName']} ({i['dimension']}, {i['gamemode']})\n"
                players+=1
                
            await list.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{count+1}周目 在线:\n{message}"))
            count+=1
        await list.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"总在线人数: {players}, 在线管理员: {ops}。"))

save=on_command("save", aliases={"保存", "保存世界", "saveworld","save_world", "保存服务器", "saveserver", "save_server"})
@save.handle()
async def save_handle(bot: Bot, event: GroupMessageEvent):
    if (event.group_id in allow_group_ids) or (event.get_user_id() in bot.config.superusers.copy()):
        success=0
        count=0
        for url in server_api_urls:
            resp=requests.post(f"{url}v1/worlds/save", headers=headers).text
            if resp == '''"success"''':
                await save.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{count+1}周目 已成功保存世界 ({resp}) 。"))
                success+=1
            else:
                await save.send(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{count+1}周目 保存不成功 ({resp}) 。"))
            count+=1
        await save.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(f"{success} 个服务器已成功保存世界。"))
