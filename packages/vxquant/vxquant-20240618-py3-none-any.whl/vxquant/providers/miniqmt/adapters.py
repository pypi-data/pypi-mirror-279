"""类型转换器"""

from enum import Enum
from xtquant import xtconstant
from xtquant.xttype import XtPosition
from vxutils import to_datetime
from vxutils.datamodel.adapter import VXDataAdapter
from vxquant.models.base import VXOrder, VXTick, VXExecRpt, VXPosition, VXCashInfo
from vxquant.models.preset import VXMarketPreset


qmt_orderstatus_map = {
    xtconstant.ORDER_UNREPORTED: "PendingNew",
    xtconstant.ORDER_WAIT_REPORTING: "PendingNew",
    xtconstant.ORDER_REPORTED: "New",
    xtconstant.ORDER_REPORTED_CANCEL: "New",
    xtconstant.ORDER_PARTSUCC_CANCEL: "PartiallyFilled",
    xtconstant.ORDER_PART_CANCEL: "Canceled",
    xtconstant.ORDER_CANCELED: "Canceled",
    xtconstant.ORDER_PART_SUCC: "PartiallyFilled",
    xtconstant.ORDER_SUCCEEDED: "Filled",
    xtconstant.ORDER_JUNK: "Rejected",
    xtconstant.ORDER_UNKNOWN: "Unknown",
}

order_sides = [
    xtconstant.STOCK_BUY,
    xtconstant.CREDIT_BUY,
    xtconstant.CREDIT_FIN_BUY,
    xtconstant.CREDIT_BUY_SECU_REPAY,
    xtconstant.CREDIT_FIN_BUY_SPECIAL,
    xtconstant.CREDIT_BUY_SECU_REPAY_SPECIAL,
]

market_price_types = [
    xtconstant.MARKET_SH_CONVERT_5_CANCEL,
    xtconstant.MARKET_SH_CONVERT_5_LIMIT,
    xtconstant.MARKET_PEER_PRICE_FIRST,
    xtconstant.MARKET_MINE_PRICE_FIRST,
    xtconstant.MARKET_PEER_PRICE_FIRST,
    xtconstant.MARKET_MINE_PRICE_FIRST,
    xtconstant.MARKET_SZ_INSTBUSI_RESTCANCEL,
    xtconstant.MARKET_SZ_CONVERT_5_CANCEL,
    xtconstant.MARKET_SZ_FULL_OR_CANCEL,
    84,
    85,
    86,
    87,
    88,
    89,
]


miniqmt_tick_adapter = VXDataAdapter(
    VXTick,
    {
        "tick_id": lambda x: str(
            f"{x['stock_code']}@{x['timetag'] if 'timetag' in x else x['time']}"
        ),
        "symbol": "stock_code",
        "open": "open",
        "high": "high",
        "low": "low",
        "lasttrade": "lastPrice",
        "yclose": "lastClose",
        "ysettle": "lastSettlementPrice",
        "amount": "amount",
        "volume": "volume",
        "ask1_p": lambda x: x["askPrice"][0],
        "ask1_v": lambda x: x["askVol"][0],
        "bid1_p": lambda x: x["bidPrice"][0],
        "bid1_v": lambda x: x["bidVol"][0],
        "ask2_p": lambda x: x["askPrice"][1],
        "ask2_v": lambda x: x["askVol"][1],
        "bid2_p": lambda x: x["bidPrice"][1],
        "bid2_v": lambda x: x["bidVol"][1],
        "ask3_p": lambda x: x["askPrice"][2],
        "ask3_v": lambda x: x["askVol"][2],
        "bid3_p": lambda x: x["bidPrice"][2],
        "bid3_v": lambda x: x["bidVol"][2],
        "ask4_p": lambda x: x["askPrice"][3],
        "ask4_v": lambda x: x["askVol"][3],
        "bid4_p": lambda x: x["bidPrice"][3],
        "bid4_v": lambda x: x["bidVol"][3],
        "ask5_p": lambda x: x["askPrice"][4],
        "ask5_v": lambda x: x["askVol"][4],
        "bid5_p": lambda x: x["bidPrice"][4],
        "bid5_v": lambda x: x["bidVol"][4],
        "created_dt": lambda x: to_datetime(
            x["timetag"] if "timetag" in x else x["time"] / 1000
        ),
    },
)

miniqmt_order_adapter = VXDataAdapter(
    VXOrder,
    {
        "order_id": lambda x: str(x.order_id),
        "account_id": "account_id",
        "symbol": "stock_code",
        "order_side": lambda x: ("Buy" if x.order_type in order_sides else "Sell"),
        "position_effect": lambda x: (
            "Open" if x.order_type in order_sides else "Close"
        ),
        "order_type": lambda x: (
            "Market" if x.price_type in market_price_types else "Limit"
        ),
        "price": "price",
        "volume": "order_volume",
        "filled_volume": "traded_volume",
        "filled_vwap": "traded_price",
        "filled_amount": lambda x: x.traded_volume * x.traded_price,
        "status": lambda x: qmt_orderstatus_map.get(x.order_status, "Unknown"),
        "reject_reason": "status_msg",
        "created_dt": lambda x: to_datetime(x.order_time),
    },
)


miniqmt_execrpt_adapter = VXDataAdapter(
    VXExecRpt,
    {
        "execrpt_id": lambda x: str(x.traded_id),
        "account_id": "account_id",
        "order_id": lambda x: str(x.order_id),
        "symbol": "stock_code",
        "order_side": lambda x: ("Buy" if x.order_type in order_sides else "Sell"),
        "position_effect": lambda x: (
            "Open" if x.order_type in order_sides else "Close"
        ),
        "price": "traded_price",
        "volume": "traded_volume",
        "created_dt": lambda x: to_datetime(x.traded_time),
    },
)


miniqmt_position_adapter = VXDataAdapter(
    VXPosition,
    {
        "account_id": "account_id",
        "symbol": "stock_code",
        "volume_today": lambda x: (
            x.volume - x.yesterday_volume if x.volume > x.yesterday_volume else 0
        ),
        "volume_his": lambda x: x.yesterday_volume,
        "frozen": "frozen_volume",
        "lasttrade": lambda x: (
            round(x.market_value / x.volume, 4) if x.volume > 0 else 0.0
        ),
        "cost": lambda x: x.volume * (x.avg_price if x.avg_price > 0 else x.open_price),
    },
)

miniqmt_cashinfo_adapter = VXDataAdapter(
    VXCashInfo,
    {
        "account_id": "account_id",
        "balance": lambda x: x.cash + x.frozen_cash,
        "order_frozen": "frozen_cash",
        "market_value": "market_value",
    },
)

if __name__ == "__main__":

    import time
    from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
    from xtquant.xttype import StockAccount
    from xtquant import xtconstant

    path = """D:\\兴业证券SMT-Q实盘交易\\userdata_mini"""
    session_id = int(time.time())
    xt_trader = XtQuantTrader(path, session_id)
    acc = StockAccount("20061359")
    xt_trader.start()
    connect_result = xt_trader.connect()
    print(connect_result)
    subscribe_result = xt_trader.subscribe(acc)
    print(subscribe_result)
    xt_trader.order_stock(
        acc,
        "600000.SH",
        xtconstant.STOCK_BUY,
        1000,
        xtconstant.MARKET_SH_CONVERT_5_CANCEL,
        price=0,
    )
    xt_trader.order_stock(
        acc,
        "600000.SH",
        xtconstant.STOCK_BUY,
        1000,
        xtconstant.MARKET_SH_CONVERT_5_LIMIT,
        price=0,
    )
    xt_trader.order_stock(
        acc,
        "600000.SH",
        xtconstant.STOCK_BUY,
        1000,
        xtconstant.MARKET_MINE_PRICE_FIRST,
        price=0,
    )
    orders = xt_trader.query_stock_orders(acc)
    for order in orders:
        print(miniqmt_order_adapter(order), order.price_type)
    print(market_price_types)

    execrpts = xt_trader.query_stock_trades(acc)
    for execrpt in execrpts:
        print(miniqmt_execrpt_adapter(execrpt))

    positions = xt_trader.query_stock_positions(acc)
    for position in positions:
        print(
            miniqmt_position_adapter(position),
            position.on_road_volume,
            position.yesterday_volume,
            position.market_value,
            position.volume,
            "avg_price:",
            position.avg_price,
            position.open_price,
        )
    asset = xt_trader.query_stock_asset(acc)

    print(miniqmt_cashinfo_adapter(asset))
