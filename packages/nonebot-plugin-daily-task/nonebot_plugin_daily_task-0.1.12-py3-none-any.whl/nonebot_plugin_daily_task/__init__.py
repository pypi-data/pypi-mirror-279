from nonebot import require

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from nonebot.log import logger
import datetime
from pathlib import Path
from tinydb import TinyDB, Query
from typing import Optional
from nonebot import get_driver, get_plugin_config
from nonebot.rule import to_me
from nonebot.adapters import Message, MessageTemplate, Event
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.permission import SUPERUSER

from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.onebot.v11 import Bot as OneBot
from nonebot import CommandGroup

from .config import Config

# 插件信息
__plugin_meta__ = PluginMetadata(
    name="Daily Task",
    description="这个插件可以帮助用户管理每日任务，包括添加任务、完成任务、查询任务等功能。",
    usage="帮助 daily.h daily.help",
    type="application",
    homepage="https://github.com/WMGray/nonebot-plugin-daily-task/",
    # 发布必填。
    config=Config,
    # 插件配置项类，如无需配置可不填写。
    supported_adapters={"~onebot.v11"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

# 加载插件配置
cfg = get_plugin_config(Config)
driver = get_driver()
db = None


async def is_enable() -> bool:
    return cfg.daily_task_enabled


# 配置响应器组
daily_group = CommandGroup(
    'daily',
    rule=to_me(),
    prefix_aliases=True,
    priority=cfg.daily_task_priority,
    block=True,
)
Rules = to_me() & is_enable

daily = daily_group.command(tuple())
daily_add = daily_group.command("add", aliases={"a"}, rule=Rules)
daily_modify = daily_group.command('modify', aliases={'m'}, rule=Rules)
daily_finish = daily_group.command('finish', aliases={'f'}, rule=Rules)
daily_del = daily_group.command("del", aliases={"delete", "d"}, rule=Rules)
daily_query = daily_group.command('query', aliases={'q'}, rule=Rules)
daily_help = daily_group.command('help', aliases={"h"}, rule=Rules)

# 设置只有管理员才可以使用的命令
daily_start = daily_group.command('start', aliases={"s"}, permission=SUPERUSER)
daily_stop = daily_group.command('stop', aliases={"st"}, permission=SUPERUSER)


# 初始化插件数据库
async def _init_db():
    global db, db_name
    try:
        if hasattr(cfg, 'daily_task_db_name'):
            db_name = cfg.daily_task_db_name  # 数据库名字
            base_dir = Path(__file__).parent  # 当前插件路径
            db_path = base_dir / f'{db_name}.json'
            db = TinyDB(db_path)  # 创建/加载数据库
            logger.success(f"Load Database {db_name} Successfully!")
        else:
            logger.error("ERROR: config.db_name is not defined.")
    except FileNotFoundError:
        logger.error(f"ERROR: Database file {db_name}.json not found.")
    except OSError as e:
        logger.error(f"ERROR: Failed to load database {db_name}. Error: {e}")

    logger.success("Daily Task Plugin Started")


# daily -- 简单介绍一下插件信息
@daily.handle()
async def send_info():
    """
    向用户发送一些插件信息
    """
    msg = MessageTemplate("插件名称: {}\n插件介绍: {}\n插件帮助: daily.help/h".format(
        __plugin_meta__.name,
        __plugin_meta__.description
    ))
    await daily.finish(msg)


# daily.help -- 发送插件相关命令
@daily_help.handle()
async def handle_daily_command():
    """
    添加任务: add、 添加
    删除任务: del、 delete、 删除
    查询任务: query、 查询
    """
    # 构建帮助信息
    message = MessageSegment.text("添加任务: daily.add/a\n"
                                  "删除任务: daily.del/d\n"
                                  "完成任务: daily.finish/f\n"
                                  "修改任务: daily.modify/m\n"
                                  "查询任务: daily.query/q status/task\n"
                                  "启用插件: daily.start/s\n"
                                  "停用插件: daily.stop/st\n"
                                  "帮助: daily.help/h")
    await daily_help.finish(message=message)


# daily.add -- 向数据库中添加任务
@daily_add.handle()
async def add_task(bot: OneBot, event: Event, args: Message = CommandArg()):
    global db
    user_id = event.get_user_id()  # 用户id
    job = args.extract_plain_text()  # 任务信息
    if job:
        # 检查 job 是否已存在
        if db.table('Task').search((Query().user_id == user_id) &
                                   (Query().task == job)):
            await daily_add.finish("任务已存在")
        # job_id = str(uuid.uuid4())  # Task ID
        start_date = datetime.date.today()  # 开始时间
        end_date = "None"  # 结束时间
        # 向'Task'数据库中添加数据
        db.table('Task').insert({'user_id': user_id,
                                 'task': job,
                                 # 'task_id': job_id,
                                 'start_date': start_date.isoformat(),
                                 'end_date': end_date})
        # 返回信息
        msg = MessageTemplate("任务已记录:\nid: {}\ntask: {}\nstart time: {}"
                              .format(user_id, job, start_date))
        await daily_add.send(msg)
        # 更新‘Status’数据库
        await update_status_add(bot=bot, uid=user_id)
    else:
        await daily_add.finish("请在命令后加上要添加的任务..")


# 查询'Task'数据库中的任务
async def query_task(uid: str, **kwargs):
    """查询指定user的任务"""
    # 必需参数: user_id  可选参数: task, start_date, end_date(不为None --> 查询)
    query = Query().user_id == uid
    for k, v in kwargs.items():
        query &= Query()[k] == v
    tasks = db.table('Task').search(query)
    return tasks


# 查询'Status'数据库中的任务
async def query_status(uid: str, **kwargs):
    """查询指定user的任务"""
    # 必需参数: user_id  可选参数: task, date, status
    query = Query().user_id == uid
    for k, v in kwargs.items():
        query &= Query()[k] == v
    tasks = db.table('Status').search(query)
    return tasks


@daily_finish.handle()
async def update_status_finish(bot: OneBot, event: Event, args: Message = CommandArg()):
    """完成指定用户的指定任务  -- Task & Status"""
    text = args.extract_plain_text().strip().split()
    # 长度不为2 或者 第二个参数不为数字
    if len(text) != 2 or not text[1].isdigit() or text[0] not in ['f', 't']:
        await daily_finish.finish("参数错误, 请使用 'daily.finish/f f/t 1' 格式")

    # 获取参数: 用户id, 任务id, 完成情况
    user_id = event.get_user_id()  # 用户id
    index = int(text[1]) - 1  # 任务序号

    status = text[0]  # 完成情况

    # 获取指定index的任务信息
    task_info = await query_task_by_id(uid=user_id, index=index)

    today = datetime.date.today().isoformat()  # 今日
    if status == 'f':  # 任务完成 --> Task: end_date = today
        tasks = await query_task(uid=user_id, task=task_info)
        for task in tasks:
            db.table('Task').update({'end_date': today}, doc_ids=[task.doc_id])

    # 今日完成情况 -- status == t (不论status, 都要更改)
    tasks = await query_status(uid=user_id, task=task_info, date=today)

    for task in tasks:
        db.table('Status').update({'status': True}, doc_ids=[task.doc_id])  # 更新任务信息

    await daily_finish.send("任务状态已更新")
    await query_today_task_status(bot=bot, uid=user_id)

    if status == 'f':
        await daily_finish.send("剩余任务:")
        await query_user_tasks(bot=bot, uid=user_id)


@daily_del.handle()
async def update_status_del(event: Event, args: Message = CommandArg()):
    """删除指定用户的指定任务  -- Task & Status"""
    # 获取参数: 用户id, 任务id
    text = args.extract_plain_text().strip().split()
    if len(text) != 1 or not text[0].isdigit():
        await daily_del.finish("参数错误, 请使用 'daily.del/d 1' 格式")
    user_id = event.get_user_id()  # 用户id
    index = int(text[0]) - 1  # 任务序号

    # 找出对应的任务
    task_info = await query_task_by_id(uid=user_id, index=index)

    # 更新'Status'数据库
    tasks = await query_status(uid=user_id, task=task_info)
    for task in tasks:
        db.table('Status').remove(doc_ids=[task.doc_id])

    # 更新'Task'数据库
    tasks = await query_task(uid=user_id, task=task_info)
    for task in tasks:
        db.table('Task').remove(doc_ids=[task.doc_id])
    await daily_del.send("任务已删除")


# 根据job_id返回今日任务信息
async def query_task_by_id(uid: str, index: int):
    """查询指定user的任务"""
    # 必需参数: user_id  可选参数: task, start_date, end_date(不为None --> 查询)
    today = datetime.date.today().isoformat()  # 今日

    tasks = await query_status(uid=uid, date=today)  # 获取当前用户的所有任务
    if len(tasks) > index:  # 如果存在指定index的任务
        task_info = tasks[index].get('task')  # 获取指定index的任务信息
    else:
        await daily_modify.finish("任务不存在, 请重新输入")
    return task_info


@daily_modify.handle()
async def update_status_modify(bot: OneBot, event: Event, args: Message = CommandArg()):
    """修改指定用户的指定任务  -- Task & Status"""
    text = args.extract_plain_text().strip().split()
    # 长度不为2 或者 第一个参数不为数字
    if len(text) != 2 or not text[0].isdigit():
        await daily_modify.finish("参数错误, 请使用 'daily.modify/m 1 new-task' 格式")

    # 获取参数: 用户id, 任务id, 新任务
    user_id = event.get_user_id()  # 用户id
    index = int(text[0]) - 1  # 任务序号
    new_job = text[1]  # 新任务

    """
    1. 更新 'Task' 数据库
    1.1 查询当前用户的所有任务（处于未结束状态）
    1.2 获取指定index的旧任务信息
    1.3 更新任务信息
    """
    task_info = await query_task_by_id(uid=user_id, index=index)  # 获取指定index的任务信息

    tasks = await query_task(uid=user_id, task=task_info)  # 获取当前用户的所有任务
    for task in tasks:
        db.table('Task').update({'task': new_job}, doc_ids=[task.doc_id])  # 更新任务信息

    """
    2. 更新 'Status' 数据库
    2.1 查询当前用户的所有任务
    2.2 更新任务信息
    """
    tasks = await query_status(uid=user_id, task=task_info)  # 获取当前用户的所有任务
    for task in tasks:
        db.table('Status').update({'task': new_job}, doc_ids=[task.doc_id])  # 更新任务信息

    await daily_modify.send("任务修改成功")
    await query_user_tasks(bot=bot, uid=user_id)


# 'Status' 数据库更新: 1. 每天定时更新  2. 用户操作(add)
async def update_status_add(bot: OneBot, uid: Optional[str] = None):
    """
    每天定时查询'Task'数据库, 并更新'Status'
    """
    global db
    today = datetime.date.today().isoformat()  # 今日
    # 构建查询条件
    query = (Query().end_date == "None")
    if uid:
        query &= (Query().user_id == uid)
    # 遍历 Task 数据集,更新 Status
    for task in db.table('Task').search(query):
        user_id = task['user_id']  # User ID
        job = task['task']  # Task info
        # job_id = task['task_id']  # Task info

        existing_status = await query_status(uid=user_id, task=job, date=today)

        if not existing_status:
            db.table('Status').insert({
                'user_id': user_id,
                'task': job,
                # 'task_id': job_id,
                'date': today,
                'status': False
            })
    if uid:  # 如果更新指定user, 向user发送消息
        await query_today_task_status(bot=bot, uid=uid)


@daily_query.handle()
async def query_info(bot: OneBot, event: Event, args: Message = CommandArg()):
    """
    查询任务
    """
    user_id = event.get_user_id()  # 用户id
    if detail := args.extract_plain_text():
        if "status" in detail:
            await query_today_task_status(bot=bot, uid=user_id)
        else:
            await query_user_tasks(bot=bot, uid=user_id)
    else:
        await daily_query.send("请在命令后指定查询内容: status / task")


# daily.query -- 查询当日完成情况
async def query_today_task_status(bot: OneBot, uid: str):
    """
    查询指定user的今日任务完成状况
    """
    user_info = await bot.call_api('get_stranger_info', user_id=uid)
    today = datetime.date.today().isoformat()
    if uid:  # 如果更新指定user, 向user发送消息
        tasks = await query_status(uid=uid, date=today)
        msg = f"{user_info['nickname']} 当天任务完成情况:\n"
        for i, task in enumerate(tasks):
            msg += f"{i + 1}. {task['task']} [{'√' if task['status'] else '×'}]\n"
        await bot.send_private_msg(user_id=uid, message=msg)
    else:
        await daily_query.send("未指定User")


# # daily.query -- 查询用户任务
async def query_user_tasks(bot: OneBot, uid: str):
    """
    查询指定user的任务
    """
    user_info = await bot.call_api('get_stranger_info', user_id=uid)
    if uid:  # 如果更新指定user, 向user发送消息
        tasks = await query_task(uid=uid, end_date='None')
        msg = f"User: {user_info['nickname']} 当前任务情况:\n"
        for i, task in enumerate(tasks):
            msg += f"{i + 1}. {task['task']} [{task['start_date']}]\n"
        await daily_query.send(msg)
    else:
        await daily_query.send("未指定User")


@daily_start.handle()
async def start_task(bot: OneBot):
    """启动定时任务"""
    cfg.daily_task_enabled = True
    if not scheduler.get_jobs():
        await send_init_msg(bot)
    await daily_start.finish("定时任务已启动")


@daily_stop.handle()
async def stop_task(event: Event):
    """停止定时任务"""
    cfg.daily_task_enabled = False
    scheduler.remove_all_jobs()
    await daily_stop.finish("定时任务已停止")


@driver.on_bot_connect
async def send_init_msg(bot: OneBot):
    await _init_db()
    start_h, end_h = cfg.daily_task_start_hour, cfg.daily_task_end_hour
    interval_h = cfg.daily_task_interval_hour
    # 创建两个定时任务： 每日0点更新任务状态 & 每日10-22点每分钟提醒
    scheduler.add_job(update_status_add, "cron", hour=0, args=[bot])
    # scheduler.add_job(update_status_add, "cron", hour=f"{start_h}-{end_h}/{interval_h}"
    #                   , minute='*')
    # 查询那些数据库存在未完成任务的用户
    user_ids = set([user['user_id'] for user in db.table('Task').search(Query().end_date == "None")])
    for user_id in set(user_ids):
        # 定时提醒
        scheduler.add_job(query_today_task_status, "cron", hour=f"{start_h}-{end_h}/{interval_h}"
                          , minute='0', args=[bot, user_id], id=user_id)
    logger.success("Daily Task Plugin Init Successfully!")
