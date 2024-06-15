<!-- markdownlint-disable MD041 -->
<p align="center">
  <a href="https://nonebot.dev/"><img src="https://nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# nonebot-plugin-daily-task

_✨ NoneBot 每日任务插件 ✨_


<a href="https://github.com/WMGray/nonebot-plugin-daily-task/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/WMGray/nonebot-plugin-daily-task" alt="license">
</a>
<a href="https://pypi.org/project/nonebot-plugin-daily-task/">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-daily-task" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 💿 安装

<summary>使用 nb-cli 安装</summary>

    nb plugin install nonebot-plugin-daily-task

<summary>pip</summary>

    pip install nonebot-plugin-daily-task

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_daily_task"]

## ⚙️ 配置

在 插件 的`config.py`文件中修改下表中的配置

|           配置项            |  类型  |  默认值  |     说明     |
|:------------------------:|:----:|:-----:|:----------:|
|    daily_task_bot_id     | str  |   无   |   Bot QQ   |
|    daily_task_db_name    | str  | daily |   数据库名称    |
|  daily_task_start_hour   | int  |  10   | 每日任务提醒开始时间 |
|   daily_task_end_hour    | int  |  23   | 每日任务提醒结束时间 |
| daily_task_interval_hour | int  |   2   | 每日任务提醒间隔时间 |
|   daily_task_priority    | int  |  10   | 每日任务提醒优先级  |
|    daily_task_enabled    | bool | False | 是否启用每日任务提醒 |

## 🎉 使用nonebot-plugin-daily-task

### 指令表

|       指令       |    功能    |    权限     |
|:--------------:|:--------:|:---------:|
|     daily      |   插件简介   |    所有人    |
|  daily.help/h  | 查看插件帮助信息 |    所有人    |
|  daily.add/a   |  添加每日任务  |    所有人    |
|  daily.del/d   |  删除每日任务  |    所有人    |
| daily.modify/m |  修改每日任务  |    所有人    |
| daily.query/q  |  查询每日任务  |    所有人    |
| daily.finish/f |  完成每日任务  |    所有人    |
| daily.start/s  |  启用每日任务  | SUPERUSER |
| daily.stop/st  |  停用每日任务  | SUPERUSER |

