"""A股运作"""

import logging
import json
import polars as pl
from argparse import ArgumentParser
from pathlib import Path
from vxsched.core import ON_EXIT_EVENT, ON_INIT_EVENT
from vxsched import vxsched, EVERY, DAILY, ONCE, VXEvent, load_modules
from vxutils import loggerConfig, VXContext, VXDatetime
from vxquant.mdapi import VXMdAPI


@vxsched.register(ON_INIT_EVENT)
def init_system(context: VXContext, event: VXEvent) -> None:
    """初始化系统"""
    logging.info("添加before_trade事件 每日09:10:00触发")
    vxsched.publish(
        "before_trade", channel="system", priority=0, trigger=DAILY("09:10:00")
    )
    if (
        VXDatetime.today(timestr="09:10:00")
        < VXDatetime.now()
        < VXDatetime.today(timestr="15:30:00")
    ):
        vxsched.publish(
            "before_trade", channel="system", priority=0, trigger=ONCE(VXDatetime.now())
        )


@vxsched.register("before_trade")
def before_trade_system(context: VXContext, event: VXEvent) -> None:
    """开盘前执行系统任务"""
    if not context.calendar.is_trade_day(VXDatetime.now()):
        logging.info(
            "今日非交易日,下一个交易日是: %s ", context.calendar.get_next_n_day()
        )
        return

    logging.info("添加on_trade事件 每日09:30:01触发")
    vxsched.publish(
        "on_trade",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="09:30:01")),
    )

    logging.info("添加on_hans事件 每日10:00:00触发")
    vxsched.publish(
        "on_hans",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="10:00:00")),
    )

    logging.info("添加on_trade事件 每日14:50:00触发")
    vxsched.publish(
        "on_trade",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="14:50:00")),
    )

    logging.info("添加on_repo事件 每日15:15:00触发")
    vxsched.publish(
        "on_repo",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="15:15:00")),
    )

    logging.info("添加after_trade事件 每日15:30:00触发")
    vxsched.publish(
        "after_trade",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="15:30:00")),
    )

    logging.info("添加on_settle事件 每日22:00:00触发")
    vxsched.publish(
        "on_settle",
        channel="system",
        priority=0,
        trigger=ONCE(VXDatetime.today(timestr="22:00:00")),
    )

    logging.info("添加on_tick事件 每3秒触发一次")
    vxsched.publish(
        "on_tick",
        channel="system",
        priority=0,
        trigger=EVERY(
            3,
            start_dt=VXDatetime.today(timestr="09:30:00"),
            end_dt=VXDatetime.today(timestr="11:31:00"),
        ),
    )

    vxsched.publish(
        "on_tick",
        channel="system",
        priority=0,
        trigger=EVERY(
            3,
            start_dt=VXDatetime.today(timestr="13:00:00"),
            end_dt=VXDatetime.today(timestr="15:00:00"),
        ),
    )

    logging.info("添加on_min事件 每60秒触发一次")
    vxsched.publish(
        "on_min",
        channel="system",
        priority=0,
        trigger=EVERY(
            60,
            start_dt=VXDatetime.today(timestr="09:30:00"),
            end_dt=VXDatetime.today(timestr="11:31:00"),
        ),
    )

    vxsched.publish(
        "on_min",
        channel="system",
        priority=0,
        trigger=EVERY(
            60,
            start_dt=VXDatetime.today(timestr="13:00:00"),
            end_dt=VXDatetime.today(timestr="15:00:00"),
        ),
    )


def main() -> None:
    parser = ArgumentParser(description="调度器")
    parser.add_argument("-c", "--config", default="etc/config.json", help="配置文件")
    parser.add_argument("-m", "--mod", default="mod", help="事件列表")
    parser.add_argument("-o", "--output", default="", help="日志目录")
    parser.add_argument(
        "-v", "--verbose", default=False, help="调试模式", action="store_true"
    )
    args = parser.parse_args()
    level = "DEBUG" if args.verbose else "INFO"
    if args.output:
        loggerConfig(level=level, filename=args.output)
        logging.debug("启用日志文件: %s", args.output)
    else:
        loggerConfig(level=level, colored=True)

    configfile = Path(args.config)
    if configfile.exists():
        with open(configfile, "r") as f:
            config = json.load(f)
    else:
        config = {}
    context = VXContext(**config)
    if "mdapi" in config:
        context.mdapi = VXMdAPI(config["mdapi"], context=context)
    else:
        context.mdapi = VXMdAPI(context=context)

    if "tdapi" in config:
        context.tdapi = VXTdAPI(config["tdapi"], context=context)
    else:
        context.tdapi = VXTdAPI(context=context)

    vxsched.set_context(context)
    mod = Path(args.mod)
    if not mod.exists():
        logging.error("模块目录不存在: %s", mod)
    else:
        load_modules(mod_path=mod)
    vxsched.run()


if __name__ == "__main__":
    main()
