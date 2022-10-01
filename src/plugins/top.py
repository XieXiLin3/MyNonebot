from nonebot import on_command
from nonebot.params import CommandArg, ArgPlainText, Arg
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent, MessageSegment, Message
import psutil ,datetime

allow_groups=[768176998, 316052940]

top=on_command("top", aliases={"系统信息", "信息", "sinfo", "si", "t"})
@top.handle()
async def top_handle(event: MessageEvent, bot: Bot, args: Message=CommandArg()):
    arg=args.extract_plain_text()
    if (event.get_user_id() in bot.config.superusers.copy()) or (isinstance(event, GroupMessageEvent) and event.group_id in allow_groups):
        head="System INFO / 系统信息"
        cpu=f"物理 CPU 个数: {psutil.cpu_count(logical=False)}\nCPU 使用率: {str(psutil.cpu_percent(1))} %"
        memoey=f"内存大小: {str(round(psutil.virtual_memory().total / (1024.0 * 1024.0 * 1024.0), 2))} G\n剩余内存: {str(round(psutil.virtual_memory().free / (1024.0 * 1024.0 * 1024.0), 2))} G\n内存使用率: {int(psutil.virtual_memory().total - psutil.virtual_memory().free) / float(psutil.virtual_memory().total) * 100}"
        started_time=f"系统启动时间: {datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}"
        users=f"在线用户数: {len(psutil.users())}\n在线用户: {','.join([u.name for u in psutil.users()])}"
        pids=f"进程数: {len(psutil.pids())}"
        # disks=f"硬盘信息: "
        # for i in psutil.disk_partitions():
        #     disks+="\n"
        #     o = psutil.disk_usage(i.device)
        #     disks+=f"总容量: {str(int(o.total / (1024.0 * 1024.0 * 1024.0)))} G\n"
        #     disks+=f"已用容量: {str(int(o.used / (1024.0 * 1024.0 * 1024.0)))} G\n"
        #     disks+=f"可用容量: {str(int(o.free / (1024.0 * 1024.0 * 1024.0)))} G"
        if arg == "cpu" or arg == "CPU" or arg == "处理器":
            message=f"{cpu}"
        elif arg == "memory" or arg == "Memory" or arg == "内存":
            message=f"{memoey}"
        elif arg == "started_time" or arg == "Started_Time" or arg == "started time" or arg == "Started Time" or arg == "启动时间" or arg == "已启动时间" or arg == "系统启动时间" or arg == "系统已启动时间":
            message=f"{started_time}"
        elif arg == "users" or arg == "Users" or arg == "user" or arg == "User" or arg == "用户" or arg == "用户数" or arg == "在线用户" or arg == "在线用户数":
            message=f"{users}"
        elif arg == "进程数" or arg == "pids" or arg == "Pids" or arg == "进程":
            message=f"{pids}"
        # elif arg == "disks" or arg == "Disks" or arg == "disk" or arg == "Disks" or arg == "硬盘" or arg == "硬盘信息":
        #     message=f"{disks}"
        else:
            message=f"{head}\n{cpu}\n{memoey}\n{started_time}\n{pids}"
        await top.finish(MessageSegment.reply(event.message_id) + MessageSegment.text(message))
        
