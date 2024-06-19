"""异常定义"""


class VXQuantError(Exception):
    """VxQuant异常基类"""


class RiskRuleCheckFailed(VXQuantError):
    """不符合风控规则"""


class NoEnoughCash(VXQuantError):
    """资金不足"""


class NoEnoughPosition(VXQuantError):
    """仓位不足"""


class IllegalAccountId(VXQuantError):
    """非法账户ID"""


class IllegalStrategyId(VXQuantError):
    """非法策略ID"""


class IllegalSymbol(VXQuantError):
    """非法交易标的"""


class IllegalVolume(VXQuantError):
    """非法委托量"""


class IllegalPrice(VXQuantError):
    """非法委托价"""


class AccountDisabled(VXQuantError):
    """交易账号被禁止交易"""


class AccountDisconnected(VXQuantError):
    """交易账号未连接"""


class AccountLoggedout(VXQuantError):
    """交易账号未登录"""


class NotInTradingSession(VXQuantError):
    """非交易时段"""


class OrderTypeNotSupported(VXQuantError):
    """委托类型不支持"""


class Throttle(VXQuantError):
    """流控限制"""
