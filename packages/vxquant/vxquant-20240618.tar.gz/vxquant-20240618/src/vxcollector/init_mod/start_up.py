"""初始化模块"""

import logging
import calendar
from pathlib import Path
from datetime import date
from itertools import product
from tqdm import tqdm
import polars as pl
import baostock as bs
from baostock.data.resultset import ResultData
from typing import Generator, Any
from vxsched.core import ON_INIT_EVENT
from vxsched import vxsched, VXEvent
from vxutils import VXContext, Datetime, to_vxdatetime
from vxquant.models.nomalize import to_symbol
from vxquant.models.instruments import VXInstruments
from vxquant.models.industry import SW_INDUSTRY_CLASSICFILY


bs.login()


def to_lastday_of_month(dt: Datetime) -> date:
    """获取指定年月的最后一天"""
    dt = to_vxdatetime(dt).replace(tzinfo=None)
    return date(dt.year, dt.month, calendar.monthrange(dt.year, dt.month)[1])


def gen(rs: ResultData) -> Generator[Any, Any, Any]:
    while rs.error_code == "0" and rs.next():
        yield dict(zip(rs.fields, rs.get_row_data()))


@vxsched.register(ON_INIT_EVENT)
def init(context: VXContext, _: VXEvent) -> None:
    """初始化"""
    download_calendar(context)
    download_industry(context)
    download_instruments(context)


def download_calendar(context: VXContext) -> None:
    """下载交易日历数据"""
    calendar_db = Path.home() / ".data/" / "calendar.csv"
    rs = bs.query_trade_dates(
        start_date="2005-01-01", end_date=f"{date.today().year}-12-31"
    )
    calendar_df = (
        pl.DataFrame(list(gen(rs)))
        .with_columns(
            [
                pl.col("calendar_date").cast(pl.Date).alias("date"),
            ]
        )
        .select(["date", "is_trading_day"])
        .sort("date")
    )
    calendar_df.write_csv(calendar_db)
    logging.info(
        "baostock calendar data saved to %s,%s --> %s ",
        calendar_db,
        calendar_df["date"].min(),
        calendar_df["date"].max(),
    )
    logging.info("===> 日历更新完成 <===")


def download_industry(context: VXContext) -> None:
    """下载行业数据"""
    industry_db = Path.home() / ".data" / "industry"
    industry_db.mkdir(parents=True, exist_ok=True)

    dt = to_lastday_of_month(date.today())
    pbar = tqdm(product(range(2005, dt.year + 1), range(1, 13)))
    data = []
    for year, month in pbar:
        working_date = to_lastday_of_month(date(year, month, 1)).strftime("%Y-%m-%d")
        pbar.set_description(f"Downloading {working_date} industry data")
        if year == dt.year and month > dt.month:
            break
        rs = bs.query_stock_industry(date=working_date)
        df = pl.DataFrame(list(gen(rs)))
        if df.shape[0] == 0:
            continue
        data.append(df)
    if not data:
        logging.warning("---> 行业数据下载失败 <---")
        return
    industry_mapping = {
        ind_info["industry_name"]: ind_info["industry_code"]
        for ind_info in SW_INDUSTRY_CLASSICFILY
    }
    industry_df = pl.concat(data)
    rows = (
        industry_df.with_columns(
            [
                pl.col("code").alias("symbol"),
                pl.col("industry")
                .map_elements(lambda x: industry_mapping.get(x, "sw2021_000000"))
                .alias("industry_code"),
                pl.col("updateDate").cast(pl.Date).alias("updated_dt"),
            ]
        )
        .group_by(["industry_code", "updated_dt"])
        .agg(pl.col("symbol").unique().alias("symbols"))
    ).rows(named=True)

    instruments_industry = {}
    for row in tqdm(rows, desc="Saving industry data"):
        if row["industry_code"] not in instruments_industry:
            instruments_industry[row["industry_code"]] = VXInstruments(
                row["industry_code"]
            )
        instruments_industry[row["industry_code"]].update_components(
            row["symbols"],
            start_date=row["updated_dt"].replace(day=1),
            end_date=to_lastday_of_month(row["updated_dt"]),
        )
    for industry_code, instruments in instruments_industry.items():
        instruments.rebuild()
        instruments.dump(industry_db / f"{industry_code}.csv")

    logging.info("===> 行业数据更新完成 <===")
    return


def download_instruments(context: VXContext) -> None:
    """下载证券列表"""
    instruments_db = Path.home() / ".data" / "instruments"
    instruments_db.mkdir(parents=True, exist_ok=True)

    rs = bs.query_stock_basic()
    instruments_df = (
        pl.DataFrame(list(gen(rs)))
        .with_columns(
            [
                pl.col("code").map_elements(to_symbol).alias("symbol"),
                pl.col("ipoDate").cast(pl.Datetime).alias("start_date"),
                pl.col("outDate")
                .map_elements(lambda x: "2099-12-31" if x == "" else x)
                .cast(pl.Datetime)
                .alias("end_date"),
            ]
        )
        .select(["symbol", "start_date", "end_date", "type"])
    )

    instruments_df.filter(pl.col("type") == "1").select(
        ["symbol", "start_date", "end_date"]
    ).write_csv(instruments_db / "all_stocks.csv")
    logging.info(
        "baostock instruments data saved to %s,%s stocks ",
        instruments_db,
        instruments_df.filter(pl.col("type") == "1").shape[0],
    )

    instruments_df.filter(pl.col("type") == "2").select(
        ["symbol", "start_date", "end_date"]
    ).write_csv(instruments_db / "all_indexes.csv")
    logging.info(
        "baostock instruments data saved to %s,%s indexes ",
        instruments_db,
        instruments_df.filter(pl.col("type") == "2").shape[0],
    )

    instruments_df.filter(pl.col("type") == "4").select(
        ["symbol", "start_date", "end_date"]
    ).write_csv(instruments_db / "all_cbonds.csv")
    logging.info(
        "baostock instruments data saved to %s,%s bond_convertable ",
        instruments_db,
        instruments_df.filter(pl.col("type") == "4").shape[0],
    )

    instruments_df.filter(pl.col("type") == "5").select(
        ["symbol", "start_date", "end_date"]
    ).write_csv(instruments_db / "all_ofunds.csv")
    logging.info(
        "baostock instruments data saved to %s,%s etf/lofs ",
        instruments_db,
        instruments_df.filter(pl.col("type") == "5").shape[0],
    )
    logging.info("===> 证券列表更新完成 <===")
    return


def download_history_bars(context: VXContext) -> None:
    """下载行情数据"""
    logging.info("===> 开始下载股票历史行情数据 <===")
    trade_dates = pl.read_csv(Path.home() / ".data" / "calendar.csv")
    trade_dates = trade_dates.filter(
        [
            pl.col("is_trading_day") == 1,
            pl.col("date") >= date(2005, 1, 1),
            pl.col("date") <= date.today(),
        ]
    )
    all_stock = VXInstruments.load(
        "all_stocks", Path.home() / ".data" / "instruments" / "all_stocks.csv"
    )
