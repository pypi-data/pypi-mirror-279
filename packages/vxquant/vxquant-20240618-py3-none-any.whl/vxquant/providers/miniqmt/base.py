"""MiniQMT API provider base class and collection"""

import time
import logging
import polars as pl
from enum import Enum
from typing import Dict, List, Union, Literal, Optional, Any
from xtquant import xtdata
from xtquant import xtconstant
from xtquant.xttype import XtAccountStatus, XtOrder, XtOrderError, StockAccount
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from vxutils import VXContext, loggerConfig
from vxsched import vxsched
from vxsched.subpubs import VXPublisher
from vxquant.providers.miniqmt.adapters import (
    miniqmt_cashinfo_adapter,
    miniqmt_order_adapter,
    miniqmt_position_adapter,
    miniqmt_execrpt_adapter,
    miniqmt_tick_adapter,
)
from vxquant.tdapi import (
    VXHQCallBackProvider,
    VXGetAccountProvider,
    VXGetOrderProvider,
    VXGetPositionProvider,
    VXGetExecRptProvider,
    VXOrderBatchProvider,
    VXOrderCancelProvider,
    VXTdAPI,
)

from vxquant.models.base import VXCashInfo, VXOrder, VXPosition


class VXMiniQMTHQCallBackProvider(VXHQCallBackProvider):

    def start_up(self, context: VXContext) -> None:
        super().start_up(context)
        datas = xtdata.get_full_tick(code_list=["SH", "SZ"])
        data = []
        for stock_code, tick in datas.items():
            tick["stock_code"] = stock_code
            data.append(miniqmt_tick_adapter(tick).model_dump())
        self._ticks = pl.DataFrame(data)

        def on_data(datas: Dict[str, Dict[str, Any]]) -> None:
            data = []
            for stock_code, tick in datas.items():
                tick["stock_code"] = stock_code
                data.append(miniqmt_tick_adapter(tick).model_dump())

            df = pl.DataFrame(data)
            self.on_tick(df)

        xtdata.subscribe_whole_quote(code_list=["SH", "SZ"], callback=on_data)


class VXMiniQMTGetAccountProvider(VXGetAccountProvider):
    def __call__(
        self, account_id: str = "default", account_type: str = "STOCK", df: bool = False
    ) -> VXCashInfo:
        account = StockAccount(account_id=account_id, account_type=account_type)
        xt_cash_info = self.context.xt_trader.query_stock_asset(account)
        cash_info = miniqmt_cashinfo_adapter(xt_cash_info)
        return cash_info


class VXMiniQMTGetPositionProvider(VXGetPositionProvider):
    def __call__(
        self, account_id: str = "default", account_type: str = "STOCK", df: bool = False
    ) -> Union[Dict[str, VXPosition], pl.DataFrame]:
        account = StockAccount(account_id=account_id, account_type=account_type)
        xt_positions = self.context.xt_trader.query_stock_positions(account)
        positions = dict(
            map(lambda x: miniqmt_position_adapter(x, key="symbol"), xt_positions)
        )
        if df:
            return pl.DataFrame(
                [position.model_dump() for position in positions.values()]
            )
        else:
            return positions


class VXMiniQMTGetOrderProvider(VXGetOrderProvider):

    def __call__(
        self,
        order_id: str = "",
        *,
        account_id: str = "default",
        is_finished: bool = False,
        df: bool = False,
    ) -> Union[List[VXOrder], pl.DataFrame]:

        xt_orders = self._context.xt_trader.query_stock_orders()
        for xt_order in xt_orders:
            order = miniqmt_order_adapter(xt_order)
            self._context["orders"][order.order_id] = order

        return list(self._context["orders"].values())


class VXMiniQMTGetExecRptProvider(VXGetExecRptProvider):
    def __call__(
        self,
        *,
        account_id: str = "default",
        df: bool = False,
    ) -> Union[List[VXOrder], pl.DataFrame]:
        xt_execrpts = self._context.xt_trader.query_stock_trades()
        execrpts = [miniqmt_execrpt_adapter(xt_execrpt) for xt_execrpt in xt_execrpts]
        if df:
            return pl.DataFrame([execrpt.model_dump() for execrpt in execrpts])
        else:
            return execrpts


class XtQuantAccountType(Enum):
    FUTURE_ACCOUNT = xtconstant.FUTURE_ACCOUNT
    SECURITY_ACCOUNT = xtconstant.SECURITY_ACCOUNT
    CREDIT_ACCOUNT = xtconstant.CREDIT_ACCOUNT
    FUTURE_OPTION_ACCOUNT = xtconstant.FUTURE_OPTION_ACCOUNT
    STOCK_OPTION_ACCOUNT = xtconstant.STOCK_OPTION_ACCOUNT
    HUGANGTONG_ACCOUNT = xtconstant.HUGANGTONG_ACCOUNT
    SHENGANGTONG_ACCOUNT = xtconstant.SHENGANGTONG_ACCOUNT


class XtQuantAccountStatus(Enum):
    INVALID = xtconstant.ACCOUNT_STATUS_INVALID
    OK = xtconstant.ACCOUNT_STATUS_OK
    WAITING_LOGIN = xtconstant.ACCOUNT_STATUS_WAITING_LOGIN
    STATUSING = xtconstant.ACCOUNT_STATUSING
    FAIL = xtconstant.ACCOUNT_STATUS_FAIL
    INITING = xtconstant.ACCOUNT_STATUS_INITING
    CORRECTING = xtconstant.ACCOUNT_STATUS_CORRECTING
    CLOSED = xtconstant.ACCOUNT_STATUS_CLOSED
    ASSIS_FAIL = xtconstant.ACCOUNT_STATUS_ASSIS_FAIL
    DISABLEBYSYS = xtconstant.ACCOUNT_STATUS_DISABLEBYSYS
    DISABLEBYUSER = xtconstant.ACCOUNT_STATUS_DISABLEBYUSER


class VXXtQuantTraderCallback(XtQuantTraderCallback):
    """xtquant回调函数"""

    def __init__(
        self,
        context: VXContext,
        publisher: Optional[VXPublisher] = None,
    ) -> None:
        self._context = context
        if "orders" not in self._context:
            self._context["orders"] = {}
        self._publisher = publisher or VXPublisher(vxsched.queue)

    @property
    def context(self) -> VXContext:
        """返回上下文信息"""
        return self._context

    def on_disconnected(self) -> None:
        """
        连接断开
        :return:
        """
        logging.warning("连接断开...")
        self._publisher("on_disconnected", channel="system", priority=0)

    def on_account_status(self, account_status: XtAccountStatus) -> None:
        logging.info(
            "账户类型: %s 账号: %s, 账户状态: %s",
            XtQuantAccountType(account_status.account_type),
            account_status.account_id,
            XtQuantAccountStatus(account_status),
        )

    def on_stock_order(self, xt_order: XtOrder) -> None:
        """
        委托回报推送
        :param order: XtOrder对象
        :return:
        """

        order = miniqmt_order_adapter(xt_order)
        logging.info("委托回报: %s", order)
        self._context["orders"][order.order_id] = order
        self._publisher("on_order_status", channel="system", priority=0, data=order)

    def on_order_error(self, order_error: XtOrderError) -> None:
        """
        委托失败推送
        :param order_error:XtOrderError 对象
        :return:
        """
        logging.error(
            "委托失败: %s",
            {
                "error_id": order_error.error_id,
                "error_msg": order_error.error_msg,
                "order_id": order_error.order_id,
                "account_id": order_error.account_id,
            },
        )
        vxorder = self._context["orders"].get(order_error.order_id, None)
        if vxorder is None:
            logging.warning(f"Order {order_error.order_id} not found")
            return
        vxorder.status = "Rejected"
        vxorder.reject_reason = order_error.error_msg
        vxorder.reject_code = order_error.error_id

        self._publisher(
            "on_order_status",
            channel="system",
            priority=0,
            data=vxorder,
        )


class VXMiniQMTTdAPI(VXTdAPI):
    """miniqmt tdapi"""

    __defaults__ = {
        "current": {
            "mod_path": "vxquant.providers.miniqmt.base.VXMiniQMTHQCallBackProvider",
            "params": {},
        },
        "get_positions": {
            "mod_path": "vxquant.providers.miniqmt.base.VXMiniQMTGetPositionProvider",
            "params": {},
        },
        "get_account": {
            "mod_path": "vxquant.providers.miniqmt.base.VXMiniQMTGetAccountProvider",
            "params": {},
        },
        "get_order": {
            "mod_path": "vxquant.providers.miniqmt.base.VXMiniQMTGetOrderProvider",
            "params": {},
        },
    }

    def __init__(
        self,
        miniqmt_path: str,
        account_id: str,
        account_type: Literal[
            "STOCK", "CREDIT", "HUGANGTONG", "SHENGANGTONG"
        ] = "STOCK",
        context: Optional[VXContext] = None,
        publisher: Optional[VXPublisher] = None,
    ) -> None:

        self._miniqmt_path = miniqmt_path
        self._account = StockAccount(account_id=account_id, account_type=account_type)

        self._publisher = publisher or VXPublisher(vxsched.queue)

        context = context or VXContext()
        context.xt_trader = XtQuantTrader(miniqmt_path, int(time.time()))
        context.xt_trader.start()
        connect_result = context.xt_trader.connect()
        if connect_result != 0:
            raise ConnectionError(f"连接失败: {connect_result}")
        logging.debug("连接成功, %s", connect_result)
        context.account = StockAccount(account_id=account_id, account_type=account_type)
        subscribe_result = context.xt_trader.subscribe(context.account)
        if subscribe_result != 0:
            raise ConnectionError(f"订阅失败: {subscribe_result}")
        logging.debug("订阅成功, %s", subscribe_result)
        context.xt_trader.register_callback(VXXtQuantTraderCallback(context))
        super().__init__(context=context)


if __name__ == "__main__":
    loggerConfig("INFO")
    context = VXContext()
    trader = VXMiniQMTTdAPI(
        miniqmt_path="D:\\兴业证券SMT-Q实盘交易\\userdata_mini", account_id="2660007522"
    )
    positions = trader.get_positions(account_id="2660007522", df=True)
    print(positions)
    accountinfo = trader.get_account(account_id="2660007522")
    print(accountinfo)
    ticks = trader.current(["399001.SZ", "399905.SZ", "000001.SZ", "000002.SZ"])
    positions = positions.select(["symbol", "market_value", "available"])
    ticks = ticks.select(["symbol", "lasttrade", "yclose"])
    print(positions.join(ticks, on="symbol", how="left"))
    print(ticks.join(positions, on="symbol", how="left").fill_null(0))

    # print(trader.current._ticks.columns)
    # while True:
    #    print(
    #        trader.current(["399001.SZ", "399905.SZ"]).select(
    #            [
    #                pl.col("symbol"),
    #                pl.col("lasttrade"),
    #                (pl.col("lasttrade") / pl.col("yclose") - 1).alias("pct_chg"),
    #                pl.col("amount") / 100000000,
    #                pl.col("created_dt"),
    #            ]
    #        )
    #    )
    #    print(trader.current._ticks.shape[0])
    #    time.sleep(3)
