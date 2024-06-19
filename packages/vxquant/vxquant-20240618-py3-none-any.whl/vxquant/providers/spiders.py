"""网络爬虫模块"""

import time
from datetime import date, timedelta
import httpx
import polars as pl
from itertools import product
from vxquant.mdapi import VXCalendarProvider, VXHQProvider
from vxutils import to_datetime, VXContext

SSE_CALENDAR_LIST = "http://www.szse.cn/api/report/exchange/onepersistenthour/monthList?month={year}-{month}&random={timestamp}"


class VXSSECalendarProvider(VXCalendarProvider):

    def _fetch_calendar(self, start_date: date, end_date: date) -> pl.DataFrame:
        working_date = start_date
        replay = []

        for year, month in product(
            range(working_date.year, end_date.year + 1), range(1, 13)
        ):

            url = SSE_CALENDAR_LIST.format(
                year=year,
                month=month,
                timestamp=int(time.time()),
            )
            response = httpx.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                },
            )

            response.raise_for_status()
            data = response.json()
            replay.extend(
                [
                    {
                        "date": to_datetime(trade_date["jyrq"]).date(),
                        "is_trading_day": int(trade_date["jybz"]),
                    }
                    for trade_date in data["data"]
                ]
                if "data" in data and data["data"]
                else []
            )

        return pl.DataFrame(replay).filter(
            [pl.col("date") >= start_date, pl.col("date") <= end_date]
        )


class VXTencentHQProvider(VXHQProvider):
    pass


if __name__ == "__main__":
    cal = VXSSECalendarProvider()
    cal.start_up(VXContext())
    print(cal(date(2020, 1, 1), date(2021, 11, 21)))
