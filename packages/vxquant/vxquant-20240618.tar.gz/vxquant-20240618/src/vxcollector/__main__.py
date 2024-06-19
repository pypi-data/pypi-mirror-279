"""数据采集"""

import logging
import json
from pathlib import Path
from argparse import ArgumentParser
from typing import Union
from vxsched import vxsched, load_modules, VXEvent
from vxsched.core import ON_INIT_EVENT
from vxutils import loggerConfig, VXContext


def init(context: VXContext, mod: Union[str, Path]) -> None:
    """初始化"""

    # 创建相应目录
    (Path.home() / ".data" / "industry").mkdir(parents=True, exist_ok=True)
    logging.info(f"创建目录: {Path.home() / '.data' / 'industry'}")

    (Path.home() / ".data" / "instruments").mkdir(parents=True, exist_ok=True)
    logging.info(f"创建目录: {Path.home() / '.data' / 'instruments'}")
    load_modules(Path(__file__).parent / "init_mod")
    vxsched.trigger_event(VXEvent(type=ON_INIT_EVENT))


def run_collector(context: VXContext, mod: Union[str, Path]) -> None:
    vxsched.set_context(context)
    logging.info(f"加载基础collector 基础消息")
    load_modules(Path(__file__).parent / "mod")
    mod = Path(mod)
    if mod.exists():
        load_modules(mod_path=mod)
    vxsched.run()


def main() -> None:
    parser = ArgumentParser(description="数据采集")
    parser.add_argument("-c", "--config", default="config.json", help="配置文件")
    parser.add_argument("-m", "--mod", default="", help="事件列表")
    parser.add_argument("-l", "--log", default="", help="日志目录")
    parser.add_argument(
        "-d", "--debug", default=False, help="调试模式", action="store_true"
    )
    parser.add_argument(
        "-i", "--init", default=False, help="初始化", action="store_true"
    )
    args = parser.parse_args()
    level = "DEBUG" if args.debug else "INFO"
    if args.log:
        loggerConfig(level=level, filename=args.log)
        logging.debug("启用日志文件: %s", args.log)
    else:
        loggerConfig(level=level, colored=True)

    configfile = Path(args.config)
    if configfile.exists():
        with open(configfile, "r") as f:
            config = json.load(f)
    else:
        config = {}
    context = VXContext(**config)

    if args.init:
        init(context, args.mod)
    else:
        run_collector(context, args.mod)


if __name__ == "__main__":
    main()
