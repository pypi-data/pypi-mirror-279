"""行情接口基类"""

from datetime import date
import polars as pl
import baostock as bs
from baostock.data import resultset
from functools import lru_cache
from typing import Dict, Any, List, Generator, Literal, Optional
from vxutils.provider import AbstractProvider, AbstractProviderCollection
from vxutils import async_task, Datetime
from vxquant.models.industry import SW_INDUSTRY_CLASSICFILY
from vxquant.mdapi import (
    VXCalendarProvider,
    VXHQProvider,
    VXInstrumentsProvider,
    VXHistoryProvider,
    VXIndustryProvider,
    to_lastday_of_month,
)


lg = bs.login()
if lg.error_code != "0":
    raise ConnectionError(f"baostock loggin error: {lg.error_msg}")


def gen(rs: resultset) -> Generator[Any, Any, Any]:
    while rs.error_code == "0" and rs.next():
        yield dict(zip(rs.fields, rs.get_row_data()))


class VXBaoStockCalendarProvider(VXCalendarProvider):
    """baostock交易日历接口"""

    @lru_cache(100)
    def _fetch_calendar(self, start_date: date, end_date: date) -> pl.DataFrame:
        print(f"fetching calendar from {start_date} to {end_date}")
        data = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        return pl.DataFrame(gen(data)).select(
            [
                pl.col("calendar_date").cast(pl.Date).alias("date"),
                pl.col("is_trading_day"),
            ]
        )


class VXBaostockHistoryProvider(VXHistoryProvider):

    @lru_cache(128)
    def __call__(
        self,
        *symbols: str,
        start: Datetime,
        end: Datetime,
        freq: Literal["1d"] = "1d",
        adjustflag: Literal["forward", "backward", "none"] = "forward",
    ) -> pl.DataFrame:
        return super().__call__(
            *symbols, start=start, end=end, freq=freq, adjustflag=adjustflag
        )


class VXBaostockIndustryProvider(VXIndustryProvider):

    def _fetch_industry(
        self, trade_date: Optional[Datetime] = None, *, industry_code: str = ""
    ) -> pl.DataFrame:

        dt = to_lastday_of_month(trade_date or date.today())

        df = pl.DataFrame(
            list(gen(bs.query_stock_industry(date=dt.strftime("%Y-%m-%d"))))
        )
        if df.shape[0] == 0:
            return df

        d = {
            ind_info["industry_name"]: ind_info["industry_code"]
            for ind_info in SW_INDUSTRY_CLASSICFILY
        }

        df = df.with_columns(
            [
                pl.col("code").alias("symbol"),
                pl.col("industry")
                .map_elements(lambda x: d.get(x, "sw2021_000000"))
                .alias("industry_code"),
                pl.col("updateDate").cast(pl.Date).alias("updated_dt"),
            ]
        ).select(["symbol", "industry_code", "updated_dt"])
        return df


if __name__ == "__main__":
    from vxutils import VXContext
    from vxquant.models.instruments import VXInstruments

    provider = VXBaostockIndustryProvider()
    provider.start_up(VXContext())
    print(provider(date(2021, 11, 1)))