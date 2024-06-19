"""常用常量定义"""

from enum import Enum


class BarFreqType(Enum):
    """K线周期类型定义"""

    Tick = "tick"
    Min1 = "1m"
    Min5 = "5m"
    Min15 = "15m"
    Min30 = "30m"
    Hour1 = "1h"
    Day1 = "1d"
    Week1 = "1w"


class OrderStatus(Enum):
    """订单状态定义"""

    New = "New"  # 已报
    PartiallyFilled = "PartiallyFilled"  # 部成
    Filled = "Filled"  # 已成
    Canceled = "Canceled"  # 已撤
    Rejected = "Rejected"  # 已拒绝
    PendingNew = "PendingNew"  # 待报
    Expired = "Expired"  # 已过期


class OrderSide(Enum):
    """订单方向定义"""

    Buy = "Buy"
    Sell = "Sell"


class OrderType(Enum):
    """订单类型定义"""

    Limit = "Limit"
    Market = "Market"
    Stop = "Stop"
    StopLimit = "StopLimit"
    TrailingStop = "TrailingStop"
    TrailingStopLimit = "TrailingStopLimit"


class ExecType(Enum):
    """成交类型定义"""

    Trade = "Trade"  # 成交
    CancelRejected = "CancelRejected"  # 撤单被拒绝


class PositionEffect(Enum):
    """持仓效果定义"""

    Open = "Open"  # 开仓
    Close = "Close"  # 平仓, 具体语义取决于对应的交易所（实盘上期所和上海能源所不适用，上期所和上海能源所严格区分平今平昨，需要用3和4）
    CloseToday = "CloseToday"  # 平今仓
    CloseYesterday = "CloseYesterday"  # 平昨仓(只适用于期货，不适用股票，股票用2平仓)


class PositionSide(Enum):
    """持仓方向定义"""

    Long = "Long"  # 多头
    Short = "Short"  # 空头


class OrderRejectCode(Enum):
    """委托拒绝代码定义"""

    Unknown = "Unknown"  # 未知原因
    RiskRuleCheckFailed = "RiskRuleCheckFailed"  # 不符合风控规则
    NoEnoughCash = "NoEnoughCash"  # 资金不足
    NoEnoughPosition = "NoEnoughPosition"  # 仓位不足
    IllegalAccountId = "IllegalAccountId"  # 非法账户ID
    IllegalStrategyId = "IllegalStrategyId"  # 非法策略ID
    IllegalSymbol = "IllegalSymbol"  # 非法交易标的
    IllegalVolume = "IllegalVolume"  # 非法委托量
    IllegalPrice = "IllegalPrice"  # 非法委托价
    AccountDisabled = "AccountDisabled"  # 交易账号被禁止交易
    AccountDisconnected = "AccountDisconnected"  # 交易账号未连接
    AccountLoggedout = "AccountLoggedout"  # 交易账号未登录
    NotInTradingSession = "NotInTradingSession"  # 非交易时段
    OrderTypeNotSupported = "OrderTypeNotSupported"  # 委托类型不支持
    Throttle = "Throttle"  # 流控限制


class CancelOrderRejectCode(Enum):
    """取消订单拒绝原因"""

    OrderFinalized = "OrderFinalized"  # 委托已完成
    UnknownOrder = "UnknownOrder"  # 未知委托
    BrokerOption = "BrokerOption"  # 柜台设置
    AlreadyInPendingCancel = "AlreadyInPendingCancel"  # 委托撤销中


class CashPositionChangeReason(Enum):
    """现金持仓变动原因"""

    Deposit = "Deposit"  # 存入
    Withdraw = "Withdraw"  # 取出
    Trade = "Trade"  # 交易
    Fee = "Fee"  # 手续费
    Interest = "Interest"  # 利息
    Dividend = "Dividend"  # 分红
    Transfer = "Transfer"  # 转账
    Other = "Other"  # 其他


class SecType(Enum):
    """标的类别"""

    REPO = "REPO"  # 回购
    STOCK = "STOCK"  # 股票
    FUND = "FUND"  # 基金
    ETFLOF = "ETFLOF"  # ETF/LOF
    INDEX = "INDEX"  # 指数
    FUTURE = "FUTURE"  # 期货
    OPTION = "OPTION"  # 期权
    CREDIT = "CREDIT"  # 信用交易
    BOND = "BOND"  # 债券
    BOND_CONVERTIBLE = "BOND_CONVERTIBLE"  # 可转债
    CONFUTURE = "CONFUTURE"  # 期货连续合约


class AccountStatus(Enum):
    """账户状态"""

    CONNECTING = "CONNECTING"  # 连接中
    CONNECTED = "CONNECTED"  # 已连接
    LOGGEDIN = "LOGGEDIN"  # 已登录
    DISCONNECTING = "DISCONNECTING"  # 断开中
    DISCONNECTED = "DISCONNECTED"  # 已断开
    ERROR = "ERROR"  # 错误
