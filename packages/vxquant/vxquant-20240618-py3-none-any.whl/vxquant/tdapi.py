"""tdapi"""

import logging

import polars as pl
from typing import Any, Dict, Optional, Union, List
from multiprocessing import Lock
from vxutils import VXContext
from vxutils.provider import (
    AbstractProvider,
    AbstractProviderCollection,
    ProviderConfig,
)
from vxquant.models.base import VXTick
from vxquant.models.base import VXOrder, VXCashInfo, VXPosition, VXExecRpt
from vxquant.models.preset import VXMarketPreset
from vxquant.models.nomalize import to_symbol

__all__ = [
    "VXTdAPI",
    "VXOrderBatchProvider",
    "VXGetAccountProvider",
    "VXGetOrderProvider",
    "VXGetPositionProvider",
    "VXGetExecRptProvider",
]


class VXTdAPI(AbstractProviderCollection):
    __defaults__ = {
        "current": {
            "mod_path": "vxquant.mdapi.VXHQProvider",
            "params": {},
        },
        "order_batch": {"mod_path": "vxquant.tdapi.VXOrderBatchProvider", "params": {}},
        "get_positions": {
            "mod_path": "vxquant.tdapi.VXGetPositionProvider",
            "params": {},
        },
        "get_orders": {"mod_path": "vxquant.tdapi.VXGetOrderProvider", "params": {}},
        "get_execrpts": {
            "mod_path": "vxquant.tdapi.VXGetExecRptProvider",
            "params": {},
        },
        "get_account": {
            "mod_path": "vxquant.tdapi.VXGetAccountProvider",
            "params": {},
        },
        "order_cancel": {
            "mod_path": "vxquant.tdapi.VXOrderCancelProvider",
            "params": {},
        },
    }

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = None,
    ) -> VXOrder:
        """下单函数

        Arguments:
            symbol {str} -- 证券代码
            volume {int} -- 下单数量，正数为买，负数为卖
            price {Optional[float]} -- 委托价格 (default: {None})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        symbol = to_symbol(symbol)
        order_side = "Buy" if volume > 0 else "Sell"
        order_type = (
            "Market"
            if price is None
            and VXMarketPreset(symbol=symbol).security_type.name != "BOND_CONVERTIBLE"
            else "Limit"
        )
        if price is None:
            tick = self.current(symbol).get(symbol, None)
            price = tick.ask1_p if order_side == "Buy" else tick.bid1_p

        order = VXOrder(
            account_id=self.context.get("account_id", ""),
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_side=order_side,
            order_type=order_type,
        )
        return self.order_batch([order], df=False)[0]

    def auto_repo(
        self,
        reversed_balance: float = 0.0,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> Optional[VXOrder]:
        """自动回购函数

        Arguments:
            reversed_balance {float} -- 回购金额
            symbols {List[str]} -- 证券代码列表

        Keyword Arguments:
            strategy_id {str} -- 策略ID (default: {""})
            order_remark {str} -- 下单备注 (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        cash = self.get_cash()
        if cash.available < reversed_balance:
            raise ValueError("Available cash is not enough for repo...")

        target_repo_balance = cash.available - reversed_balance
        target_repo_volume = int(target_repo_balance // 100 // 10 * 10)
        if target_repo_volume <= 0:
            return None

        if not symbols:
            symbols = ["131810.SZ", "204001.SH"]

        ticks = self.current(*symbols)
        target_repo_symbol = ""
        for symbol in symbols:
            tick = ticks.get(symbol, None)
            if not tick:
                logging.warning(f"Tick data for {symbol} is not available...")
                continue
            if (
                target_repo_symbol == ""
                or tick.ask1_p > ticks[target_repo_symbol].ask1_p
            ):
                target_repo_symbol = symbol
        if target_repo_symbol == "":
            logging.warning("No available tick data for repo...")
            return None

        logging.info(f"Auto repo: {target_repo_symbol} {target_repo_volume}")
        return self.order_volume(
            symbol=symbols[0],
            volume=-target_repo_volume,
            price=ticks[target_repo_symbol].ask2_p,
            order_remark=order_remark,
            strategy_id=strategy_id,
        )


class VXHQCallBackProvider(AbstractProvider):
    """行情回调接口"""

    def start_up(self, context: VXContext) -> None:
        """启动函数"""
        self._ticks = pl.DataFrame({col: [] for col in VXTick.model_fields.keys()})
        self._lock = Lock()

    def __call__(
        self, *symbols: str, df: bool = False
    ) -> Union[pl.DataFrame, Dict[str, VXTick]]:
        """行情回调函数"""
        if len(symbols) == 1 and isinstance(symbols[0], list):
            symbols = symbols[0]

        with self._lock:
            ticks = self._ticks.filter(pl.col("symbol").is_in(symbols))
            if df:
                return ticks
            return {row["symbol"]: VXTick(**row) for row in ticks.rows(named=True)}

    def on_price_change(self, ticks: pl.DataFrame) -> None:
        """行情回调函数"""
        if ticks.shape[0] == 0:
            return

        with self._lock:
            self._ticks = pl.concat(
                [
                    self._ticks.filter(pl.col("symbol").is_in(ticks["symbol"]).not_()),
                    ticks,
                ]
            )


class VXOrderBatchProvider(AbstractProvider):
    """批量下单接口"""

    def __call__(
        self, orders: List[VXOrder], *, df: bool = False
    ) -> Union[Dict[str, VXOrder], pl.DataFrame]:
        """下单函数

        Arguments:
            orders {List[VXOrder]} -- 订单列表
            df {bool} -- 是否返回DataFrame (default: {False})

        Returns:
            Union[VXOrder, pl.DataFrame]  -- 委托订单信息
        """
        raise NotImplementedError


class VXOrderCancelProvider(AbstractProvider):
    def __call__(self, order_id: str) -> str:
        """撤单函数

        Arguments:
            order_id {str} -- 订单ID

        Returns:
            str -- 返回撤单订单id
        """
        raise NotImplementedError


class VXGetAccountProvider(AbstractProvider):
    """获取账户信息接口"""

    def __call__(self) -> VXCashInfo:
        """获取账户信息

        Returns:
            Any -- 账户信息
        """
        raise NotImplementedError


class VXGetOrderProvider(AbstractProvider):
    """获取订单信息接口"""

    def __call__(
        self,
        order_id: str = "",
        *,
        is_finished: bool = False,
        df: bool = False,
    ) -> Union[List[VXOrder], pl.DataFrame]:
        """获取订单信息

        Keyword Arguments:
            order_id: str -- 订单ID (default: {""})
            account_id {str} -- 账户ID (default: {"default"})
            is_finished {bool} -- 是否已完成 (default: {False})
            df {bool} -- 是否返回dataframe格式 (default: {False})

        Returns:
            Union[List[VXOrder],pl.DataFrame] -- 订单信息
        """
        raise NotImplementedError


class VXGetPositionProvider(AbstractProvider):
    """获取持仓信息接口"""

    def __call__(
        self, symbol: Optional[str] = None, df: bool = False
    ) -> Union[Dict[str, VXPosition], pl.DataFrame]:
        """获取持仓信息

        Returns:
            Union[List[VXPosition],pl.DataFrame] -- 持仓信息
        """
        raise NotImplementedError


class VXGetExecRptProvider(AbstractProvider):
    """获取成交信息接口"""

    def __call__(
        self, execrpt_id: str = "", *, df: bool = False
    ) -> Union[List[VXExecRpt], pl.DataFrame]:
        """获取成交信息

        Keyword Arguments:
            execrpt_id {str} -- 成交信息订单号 (default: {""})
            df {bool} -- 是否返回dataframe格式 (default: {False})

        Returns:
            Union[List[VXExecRpt], pl.DataFrame] -- 成交信息
        """
        raise NotImplementedError


if __name__ == "__main__":
    tdapi = VXTdAPI()
