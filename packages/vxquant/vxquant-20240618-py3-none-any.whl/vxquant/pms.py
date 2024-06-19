"""账户交易操作类"""

import polars as pl
import logging
from typing import Dict, Union, Optional, Any, List, Tuple
from collections import defaultdict
from pydantic import UUID4, Field
from multiprocessing import Lock
from itertools import chain
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
from vxutils import VXDatetime, to_json, singleton
from vxquant.models.preset import VXMarketPreset
from vxquant.models.base import VXExecRpt, VXOrder, VXCashInfo, VXPosition


@singleton
class VXOrderManager:
    """订单管理器"""

    def __init__(self) -> None:
        self._orders = pl.DataFrame(VXOrder.model_fields)
        self._execrpts: Dict[str, Dict[UUID4, VXExecRpt]] = defaultdict(dict)
        self._lock = Lock()

        return

    def get_order(self, order_id: str) -> Optional[VXOrder]:
        return self._orders.get(order_id)

    def get_execrpt(self, order_id: str) -> Dict[UUID4, VXExecRpt]:
        return self._execrpts.get(order_id, {})

    def _update_order_info(self, order_id: str) -> None:
        if order_id not in self._orders:
            logging.warning(f"Order {order_id} not found")
            return

        order = self._orders[order_id]
        if order.status in [
            OrderStatus.Canceled,
            OrderStatus.Rejected,
            OrderStatus.Expired,
            OrderStatus.Filled,
        ]:
            return

        order.filled_volume = 0
        order.filled_commission = 0
        order.filled_vwap = 0
        order.filled_amount = 0
        for execrpt in self._execrpts[order_id].values():
            order.filled_volume += execrpt.volume
            order.filled_amount += execrpt.price * execrpt.volume
            order.filled_commission += execrpt.commission

        if order.filled_volume <= 0:
            order.status = OrderStatus.New
            return
        order.filled_vwap = (
            (order.filled_amount + order.filled_commission) / order.filled_volume
            if order.order_side == OrderSide.Buy
            else (order.filled_amount - order.filled_commission) / order.filled_volume
        )
        if order.filled_volume < order.volume:
            order.status = OrderStatus.PartiallyFilled
        else:
            order.status = OrderStatus.Filled
            order.filled_volume = order.volume

    def on_execution_report(self, execrpt: VXExecRpt) -> None:
        if execrpt.execrpt_id in self._execrpts[execrpt.order_id]:
            logging.warning(f"ExecRpt {execrpt.execrpt_id} already exists")
            return

        with self._lock:
            self._execrpts[execrpt.order_id][execrpt.execrpt_id] = execrpt
            self._update_order_info(execrpt.order_id)

    def on_order_status(self, order: VXOrder) -> None:
        with self._lock:
            if order.order_id not in self._orders:
                self._orders[order.order_id] = order
                self._update_order_info(order.order_id)
                return

            if order.status in [
                OrderStatus.Canceled,
                OrderStatus.Rejected,
                OrderStatus.Expired,
            ]:

                self._orders[order.order_id].filled_amount = order.filled_amount
                self._orders[order.order_id].filled_commission = order.filled_commission
                self._orders[order.order_id].filled_volume = order.filled_volume
                self._orders[order.order_id].filled_vwap = order.filled_vwap
                self._orders[order.order_id].status = order.status
                self._orders[order.order_id].reject_code = order.reject_code
                self._orders[order.order_id].reject_reason = order.reject_reason
                return

    def place_order(
        self, account_id: str, symbol: str, volume: int, price: float = 0.0
    ) -> VXOrder:
        """设置委托"""
        order = VXOrder(
            order_id="",
            account_id=account_id,
            symbol=symbol,
            order_side=OrderSide.Buy if volume > 0 else OrderSide.Sell,
            position_effect=PositionEffect.Open if volume > 0 else PositionEffect.Close,
            order_type=OrderType.Limit if price > 0 else OrderType.Market,
            volume=abs(volume),
            price=price,
            status=OrderStatus.PendingNew,
        )
        return order

    def on_settle(
        self, settle_date: VXDatetime
    ) -> Tuple[List[VXOrder], List[VXExecRpt]]:
        """结算"""

        list(map(self._update_order_info, self._orders.keys()))
        settled_orders: List[VXOrder] = []
        for order in self._orders.values():
            if order.status in [
                OrderStatus.Canceled,
                OrderStatus.Rejected,
                OrderStatus.Expired,
                OrderStatus.Filled,
            ]:
                settled_orders.append(order)
                continue
            order.status = OrderStatus.Expired
            settled_orders.append(order)
            logging.warning(f"Order {order.order_id} expired...")

        settled_execrpts: List[VXExecRpt] = []
        for execrpt in self._execrpts.values():
            settled_execrpts.extend(execrpt.values())

        self._orders.clear()
        self._execrpts.clear()

        logging.info(
            f"结算日: {settle_date.date()}Settled {len(settled_orders)} orders and {len(settled_execrpts)} execrpts"
        )
        return (settled_orders, settled_execrpts)


class VXAccount:
    """账户信息"""

    __accounts__: Dict[str, "VXAccount"] = {}

    def __new__(cls, account_id: str, balance: float = 0.00) -> "VXAccount":
        if account_id not in cls.__accounts__:
            instance = super().__new__(cls)
        return cls.__accounts__[account_id]

    def __init__(self, account_id: str, balance: float = 0.00) -> None:

        if account_id in self.__accounts__:
            return
        print(f"Initializing account {account_id}")
        self.account_id = account_id
        self.cash_info = VXCashInfo(
            account_id=account_id, balance=balance, ynav=balance
        )
        self.positions: Dict[str, VXPosition] = {}
        self.orders: Dict[str, VXOrder] = {}
        self.execrpts: Dict[str, Dict[str, VXExecRpt]] = {}
        self._lock = Lock()
        return

    @classmethod
    def from_message(cls, message: Dict[str, Any]) -> "VXAccount":
        instance = cls.__new__(cls, message["account_id"])
        instance.__setstate__(message)
        return instance

    def message(self) -> Dict[str, Any]:
        with self._lock:
            execrpts: List[Dict[str, Any]] = []
            for execrpt_in_order in self.execrpts.values():
                for execrpt in execrpt_in_order.values():
                    execrpts.append(execrpt.model_dump())

            return {
                "account_id": self.account_id,
                "cash_info": self.cash_info.model_dump(),
                "positions": [pos.model_dump() for pos in self.positions.values()],
                "orders": [order.model_dump() for order in self.orders.values()],
                "execrpts": execrpts,
            }

    def __setstate__(self, state: Dict[str, Any]) -> "VXAccount":
        self.account_id = state["account_id"]
        self.cash_info = VXCashInfo(**state["cash_info"])
        self.positions = {
            pos["symbol"]: VXPosition(**pos) for pos in state["positions"]
        }
        self.orders = {order["order_id"]: VXOrder(**order) for order in state["orders"]}
        self.execrpts = {}
        for execrpt in state["execrpts"]:
            if execrpt["order_id"] not in self.execrpts:
                self.execrpts[execrpt["order_id"]] = {}
            self.execrpts[execrpt["order_id"]][execrpt["execrpt_id"]] = VXExecRpt(
                **execrpt
            )
        self._lock = Lock()
        return self

    def __getstate__(self) -> Dict[str, Any]:
        return self.message()

    def __str__(self) -> str:
        return to_json(self.message())

    def __repr__(self) -> str:
        return self.__str__()


@singleton
class VXPortfolioManager:
    """组合管理器"""


if __name__ == "__main__":
    account = VXAccount(account_id="test", balance=10000)
    account.cash_info.balance += 10000
    print(account)

    # print(VXAccount(account_id="test"))
    print(id(VXAccount(account_id="test")))
    print(account)
