"""抽象基类"""

import logging
from uuid import uuid4
from typing import Dict, Union, Optional, Any
from collections import defaultdict
from pydantic import UUID4, Field, PlainValidator, computed_field
from multiprocessing import Lock
from vxquant.models.constants import (
    ExecType,
    OrderStatus,
    OrderSide,
    OrderType,
    PositionEffect,
    OrderRejectCode,
    SecType,
)
from vxutils.datamodel.core import VXDataModel

# from vxutils.decorators import singleton
from vxutils import to_enum
from vxquant.models.preset import VXMarketPreset
from vxquant.models.nomalize import to_symbol

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated


class VXTick(VXDataModel):
    """行情数据"""

    tick_id: str = Field(
        default_factory=uuid4, title="ID", description="行情ID", strict=False
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    open: float = Field(default=0.0, title="Open", description="开盘价")
    high: float = Field(default=0.0, title="High", description="最高价")
    low: float = Field(default=0.0, title="Low", description="最低价")
    yclose: float = Field(default=0.0, title="YClose", description="昨收价")
    ysettle: float = Field(default=0.0, title="YSettle", description="昨结算价")
    lasttrade: float = Field(default=0.0, title="LastTrade", description="最新价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    amount: float = Field(default=0.0, title="Amount", description="成交额")
    ask1_p: float = Field(default=0.0, title="Ask1P", description="卖一价")
    ask1_v: int = Field(default=0, title="Ask1V", description="卖一量")
    bid1_p: float = Field(default=0.0, title="Bid1P", description="买一价")
    bid1_v: int = Field(default=0, title="Bid1V", description="买一量")
    ask2_p: float = Field(default=0.0, title="Ask2P", description="卖二价")
    ask2_v: int = Field(default=0, title="Ask2V", description="卖二量")
    bid2_p: float = Field(default=0.0, title="Bid2P", description="买二价")
    bid2_v: int = Field(default=0, title="Bid2V", description="买二量")
    ask3_p: float = Field(default=0.0, title="Ask3P", description="卖三价")
    ask3_v: int = Field(default=0, title="Ask3V", description="卖三量")
    bid3_p: float = Field(default=0.0, title="Bid3P", description="买三价")
    bid3_v: int = Field(default=0, title="Bid3V", description="买三量")
    ask4_p: float = Field(default=0.0, title="Ask4P", description="卖四价")
    ask4_v: int = Field(default=0, title="Ask4V", description="卖四量")
    bid4_p: float = Field(default=0.0, title="Bid4P", description="买四价")
    bid4_v: int = Field(default=0, title="Bid4V", description="买四量")
    ask5_p: float = Field(default=0.0, title="Ask5P", description="卖五价")
    ask5_v: int = Field(default=0, title="Ask5V", description="卖五量")
    bid5_p: float = Field(default=0.0, title="Bid5P", description="买五价")
    bid5_v: int = Field(default=0, title="Bid5V", description="买五量")


class VXBar(VXDataModel):
    """k线信息"""

    bar_id: UUID4 = Field(
        default_factory=uuid4,
        title="ID",
        description="K线ID",
        strict=False,
    )
    symbol: str = Field(default="", title="Symbol", description="代码")
    name: str = Field(default="", title="Name", description="名称")
    open: float = Field(default=0.0, title="Open", description="开盘价")
    high: float = Field(default=0.0, title="High", description="最高价")
    low: float = Field(default=0.0, title="Low", description="最低价")
    close: float = Field(default=0.0, title="Close", description="收盘价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    amount: float = Field(default=0.0, title="Amount", description="成交额")
    # frequency: Annotated[
    #    BarFreqType, PlainValidator(lambda x: to_enum(x, default=BarFreqType.Day1))
    # ] = Field(default="1m", title="Frequency", description="k线周期类型")


class VXExecRpt(VXDataModel):
    """成交回报"""

    execrpt_id: str = Field(
        default_factory=uuid4, title="ID", description="成交ID", strict=False
    )
    account_id: str = Field(
        default="", title="AccountID", description="账户ID", strict=False
    )
    order_id: str = Field(
        default="", title="OrderID", description="订单ID", strict=False
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    order_side: Annotated[
        OrderSide, PlainValidator(lambda x: to_enum(x, default=OrderSide.Buy))
    ] = Field(default=OrderSide.Buy, title="Side", description="买卖方向")
    position_effect: Annotated[
        PositionEffect,
        PlainValidator(lambda x: to_enum(x, default=PositionEffect.Open)),
    ] = Field(
        default=PositionEffect.Open, title="PositionEffect", description="持仓效果"
    )
    price: float = Field(default=0.0, title="Price", description="成交价")
    volume: int = Field(default=0, title="Volume", description="成交量")
    commission: float = Field(default=0.0, title="Fee", description="手续费")
    execrpt_type: Annotated[
        ExecType, PlainValidator(lambda x: to_enum(x, default=ExecType.Trade))
    ] = Field(default=ExecType.Trade, title="ExecType", description="成交类型")
    order_remark: str = Field(default="", title="Remark", description="备注")
    strategy_id: str = Field(default="", title="StrategyID", description="策略ID")


class VXOrder(VXDataModel):
    """委托信息"""

    order_id: str = Field(default="", title="ID", description="委托ID", strict=False)

    account_id: str = Field(
        default="", title="AccountID", description="账户ID", frozen=True
    )
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    order_side: Annotated[
        OrderSide, PlainValidator(lambda x: to_enum(x, default=OrderSide.Buy))
    ] = Field(default=OrderSide.Buy, title="Side", description="买卖方向", frozen=True)
    order_type: Annotated[
        OrderType, PlainValidator(lambda x: to_enum(x, default=OrderType.Market))
    ] = Field(
        default=OrderType.Market, title="Type", description="委托类型", frozen=True
    )
    position_effect: Annotated[
        PositionEffect,
        PlainValidator(lambda x: to_enum(x, default=PositionEffect.Open)),
    ] = Field(
        default=PositionEffect.Open,
        title="PositionEffect",
        description="持仓效果",
        frozen=True,
    )
    price: float = Field(default=0.0, title="Price", description="委托价", frozen=True)
    volume: int = Field(default=0, title="Volume", description="委托量", frozen=True)

    filled_volume: int = Field(default=0, title="FilledVolume", description="成交量")
    filled_vwap: float = Field(default=0.0, title="FilledVWAP", description="成交均价")
    filled_amount: float = Field(
        default=0.0, title="FilledAmount", description="成交额"
    )
    filled_commission: float = Field(
        default=0.0, title="FilledFee", description="手续费"
    )

    status: Annotated[
        OrderStatus,
        PlainValidator(lambda x: to_enum(x, default=OrderStatus.PendingNew)),
    ] = Field(default=OrderStatus.PendingNew, title="Status", description="委托状态")
    reject_code: Annotated[
        OrderRejectCode,
        PlainValidator(lambda x: to_enum(x, default=OrderRejectCode.Unknown)),
    ] = Field(
        default=OrderRejectCode.Unknown, title="RejectCode", description="拒绝代码"
    )
    reject_reason: str = Field(default="", title="RejectReason", description="拒绝原因")
    order_remark: str = Field(default="", title="Remark", description="备注")
    strategy_id: str = Field(default="", title="StrategyID", description="策略ID")


class VXPosition(VXDataModel):
    """持仓信息"""

    account_id: str = Field(default="", title="AccountID", description="账户ID")
    symbol: Annotated[str, PlainValidator(to_symbol)] = Field(
        default="", title="Symbol", description="代码"
    )
    sec_type: SecType = Field(
        default=SecType.STOCK, title="SecType", description="证券类型"
    )
    currency: str = Field(default="CNY", title="Currency", description="币种")
    volume_today: int = Field(default=0, title="VolumeToday", description="今仓量")
    volume_his: int = Field(default=0, title="VolumeHis", description="昨仓量")
    frozen: int = Field(default=0, title="Frozen", description="冻结量")
    lasttrade: float = Field(default=0.0, title="LastTrade", description="最新价")
    cost: float = Field(default=0.0, title="Cost", description="持仓成本")
    allow_t0: bool = Field(default=False, title="AllowT0", description="是否允许T+0")

    def model_post_init(self, _: Any) -> None:
        self.sec_type = VXMarketPreset(symbol=self.symbol).security_type
        self.allow_t0 = VXMarketPreset(symbol=self.symbol).allow_t0

    @computed_field(title="Volume", description="持仓量")
    def volume(self) -> int:
        return self.volume_today + self.volume_his

    @computed_field(title="Volume", description="持仓市值")
    def market_value(self) -> float:
        return self.lasttrade * (self.volume_today + self.volume_his)

    @computed_field(title="Available", description="可用量")
    def available(self) -> int:
        return max(
            0,
            (
                (self.volume_today + self.volume_his - self.frozen)
                if self.allow_t0
                else self.volume_his - self.frozen
            ),
        )

    @computed_field(title="VWAP", description="持仓均价")
    def vwap(self) -> float:
        return (
            self.cost / (self.volume_today + self.volume_his)
            if (self.volume_today + self.volume_his) > 0
            else 0.0
        )

    @computed_field(title="PnL", description="浮动盈亏")
    def fpnl(self) -> float:
        return self.lasttrade * (self.volume_today + self.volume_his) - self.cost


class VXCashInfo(VXDataModel):
    """账户资金或负债信息"""

    account_id: str = Field(default="", title="ID", description="账户ID")
    currency: str = Field(default="CNY", title="Currency", description="币种")
    balance: float = Field(default=0.0, title="Cash", description="资金余额")
    order_frozen: float = Field(
        default=0.0, title="OrderFrozen", description="订单冻结资金"
    )
    on_way: float = Field(default=0.0, title="OnWay", description="在途资金")
    market_value: float = Field(
        default=0.0, title="MarketValue", description="持仓市值"
    )
    fpnl: float = Field(default=0.0, title="Fpnl", description="浮动盈亏")
    ynav: float = Field(default=0.0, title="YesterdayNav", description="昨日净资产")

    @computed_field(title="nav", description="总资产")
    def nav(self) -> float:
        return self.balance + self.market_value

    @computed_field(title="Available", description="可用资金")
    def available(self) -> float:
        return self.balance - self.order_frozen - self.on_way

    @computed_field(title="PnL", description="今日盈亏")
    def today_fpnl(self) -> float:
        return self.balance + self.market_value - self.ynav if self.ynav > 0 else 0.0


if __name__ == "__main__":
    tick = VXTick()
    print(tick)
    print(tick.model_dump())

    bar = VXBar()
    print(bar)
    print(bar.model_dump())

    position = VXPosition(
        symbol="SHSE.600000",
        volume_today=100,
        volume_his=100,
        frozen=10,
        # available=100,
        lasttrade=10.0,
        cost=1000.0,
    )
    print(position)
