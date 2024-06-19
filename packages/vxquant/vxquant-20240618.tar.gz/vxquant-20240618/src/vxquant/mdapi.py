"""行情接口基类"""

import logging
import polars as pl
from pathlib import Path
import calendar
from datetime import date, timedelta
from itertools import product
from typing import Dict, Any, List, Literal, Optional
from tqdm import tqdm
from vxutils.provider import AbstractProvider, AbstractProviderCollection
from vxutils import Datetime, VXContext, VXDatetime, to_vxdatetime
from vxquant.models.base import VXTick
from vxquant.models.industry import SW_INDUSTRY_CLASSICFILY
from vxquant.models.instruments import VXInstruments


class VXCalendarProvider(AbstractProvider):
    """交易日历接口基类"""

    def __init__(self) -> None:
        self._context = VXContext()

    def start_up(self, context: VXContext) -> None:
        super().start_up(context)
        calendar_db = Path.home() / ".data/" / "calendar.csv"
        if not calendar_db.exists():
            self.context.calendar = self._fetch_calendar(
                date(2005, 1, 1), date.today().replace(month=12, day=31)
            )
            calendar_db.parent.mkdir(parents=True, exist_ok=True)
            self.context.calendar.write_csv(Path.home() / ".data/" / "calendar.csv")
            logging.info("calendar data saved to %s", calendar_db)
        else:
            self.context.calendar = pl.read_csv(calendar_db, dtypes={"date": pl.Date})

    def __call__(
        self, start_date: Optional[Datetime] = None, end_date: Optional[Datetime] = None
    ) -> pl.DataFrame:

        start_date = (
            VXDatetime(2005, 1, 1)
            if start_date is None
            else to_vxdatetime(start_date).replace(tzinfo=None)
        ).date()
        end_date = (
            VXDatetime.today().replace(month=12, day=31, tzinfo=None)
            if end_date is None
            else to_vxdatetime(end_date).replace(tzinfo=None)
        ).date()
        if start_date > end_date:
            raise ValueError("start_date should be less than end_date")

        if start_date < self.context.calendar["date"].min():
            self.context.calendar = pl.concat(
                [
                    self.context.calendar,
                    self._fetch_calendar(
                        start_date, self.context.calendar["date"].min()
                    ),
                ]
            )
            self.context.calendar.write_csv(Path.home() / ".data/" / "calendar.csv")

        if end_date > self.context.calendar["date"].max():
            self.context.calendar = pl.concat(
                [
                    self.context.calendar,
                    self._fetch_calendar(self.context.calendar["date"].max(), end_date),
                ]
            )
            self.context.calendar.write_csv(Path.home() / ".data/" / "calendar.csv")

        return self.context.calendar.filter(
            [pl.col("date") >= start_date, pl.col("date") <= end_date]
        )

    def _fetch_calendar(self, start_date: date, end_date: date) -> pl.DataFrame:
        raise NotImplementedError


class VXHQProvider(AbstractProvider):
    """实时行情接口基类"""

    def __call__(self, *symbols: str) -> pl.DataFrame:
        raise NotImplementedError


class VXInstrumentsProvider(AbstractProvider):
    """获取合约信息接口基类"""

    def start_up(self, context: VXContext) -> None:
        super().start_up(context)
        self.context.instrument_dir = Path.home() / ".data/instruments"
        if not self.context.instrument_dir.exists():
            self.contet.instrument_dir.mkdir(parents=True, exist_ok=True)

    def __call__(self, instruments_name: str = "all_stocks") -> VXInstruments:
        if Path(self.context.instrument_dir / f"{instruments_name}.csv").exists():
            return VXInstruments.load(
                instruments_name,
                self.context.instrument_dir / f"{instruments_name}.csv",
            )
        elif Path(self.context.instrument_dir / f"{instruments_name}.parquet").exists():
            return VXInstruments.load(
                instruments_name,
                self.context.instrument_dir / f"{instruments_name}.parquet",
            )
        raise FileNotFoundError(f"{instruments_name} not found.")


class VXHistoryProvider(AbstractProvider):
    """历史行情接口基类"""

    def __call__(
        self,
        *symbols: str,
        start: Optional[Datetime] = None,
        end: Optional[Datetime] = None,
        freq: Literal["1d"] = "1d",
        adjustflag: Literal["forward", "backward", "none"] = "forward",
        asset: Literal["E", "I", "C", "F", "O"] = "E",
    ) -> pl.DataFrame:
        if asset not in ["E", "I", "C", "F", "O"]:
            raise ValueError("asset should be in ['E', 'I', 'C', 'F', 'O']")
        if adjustflag not in ["forward", "backward", "none"]:
            raise ValueError("adjustflag should be in ['forward', 'backward', 'none']")
        if freq not in ["1d"]:
            raise ValueError("freq should be '1d'")
        if not symbols:
            pass
        raise NotImplementedError

    def _fetch_history(self, *symbols: str, freq: Literal["1d"] = "1d") -> pl.DataFrame:
        raise NotImplementedError

    def _fetch_deviend(
        self, start: Optional[Datetime] = None, end: Optional[Datetime] = None
    ) -> pl.DataFrame:
        raise NotImplementedError


def to_lastday_of_month(dt: Datetime) -> date:
    """获取指定年月的最后一天"""
    dt = to_vxdatetime(dt).replace(tzinfo=None)
    return date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])


def get_n_of_month(dt: Datetime, n: int = -1) -> date:
    """获取指定年月的第n天"""
    vxdt = to_vxdatetime(dt).replace(tzinfo=None)
    max_days = calendar.monthrange(vxdt.year, vxdt.month)[1]
    if n > max_days:
        n = max_days
    elif -max_days <= n < 0:
        n = max_days + n + 1
    else:
        raise ValueError(
            f"{vxdt} has only {max_days} days. n should be in [-{max_days}, {max_days}]"
        )

    return date(vxdt.year, vxdt.month, n)


class VXIndustryProvider(AbstractProvider):
    """行业分类接口"""

    def start_up(self, context: VXContext) -> None:
        super().start_up(context)
        self.context.industry_dir = Path.home() / ".data/industry/"
        if not self.context.industry_dir.exists():
            self.context.industry_dir.mkdir(parents=True, exist_ok=True)

    def __call__(
        self,
        industry_code: str,
    ) -> VXInstruments:
        if (self.context.industry_dir / f"{industry_code}.csv").exists():
            return VXInstruments.load(
                industry_code,
                self.context.industry_dir / f"{industry_code}.csv",
            )
        elif (self.context.industry_dir / f"{industry_code}.parquet").exists():
            return VXInstruments.load(
                industry_code, self.context.industry_dir / f"{industry_code}.parquet"
            )

        raise ValueError(f"{industry_code} not in industry list.")


class VXMdAPI(AbstractProviderCollection):
    """行情接口集合"""

    __defaults__ = {
        "current": {},
        "calendar": {},
        "hisotry": {},
        "instruments": {
            "mod_path": "vxquant.mdapi.VXInstrumentsProvider",
            "params": {},
        },
        "industry": {"mod_path": "vxquant.mdapi.VXIndustryProvider", "params": {}},
    }
    current: "VXHQProvider"
    calendar: "VXCalendarProvider"
    history: "VXHistoryProvider"
    instruments: "VXInstrumentsProvider"
    industry: "VXIndustryProvider"


if __name__ == "__main__":
    df = pl.DataFrame(
        {"date": ["2004-12-31"], "is_trading_date": ["1"]},
        schema={"date": pl.Date, "is_trading_date": pl.Utf8},
    )
    print(df["date"].max(), df["date"].min())
