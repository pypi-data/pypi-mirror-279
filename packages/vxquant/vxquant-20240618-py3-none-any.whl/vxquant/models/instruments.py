"""股票池"""

import logging
import datetime
import polars as pl
from pathlib import Path
from typing import List, Union, Dict, Tuple, Optional, Any, Literal
from vxquant.models.nomalize import to_symbol as normalize_symbol
from vxutils import Datetime, to_datetime


__all__ = ["VXInstruments"]


def is_in_periods(
    dt: Datetime, periods: List[Tuple[datetime.datetime, datetime.datetime]]
) -> bool:
    """判断日期是否在时间段内"""
    dt = to_datetime(dt)
    return any(period[0] <= dt <= period[1] for period in periods)


class VXInstruments:
    """股票池类"""

    def __init__(self, name: str, registrations: Optional[pl.DataFrame] = None) -> None:
        self._name = name
        self._registrations = (
            registrations.with_columns(
                [
                    pl.col("start_date").cast(pl.Datetime),
                    pl.col("end_date").cast(pl.Datetime),
                ]
            )
            if registrations is not None
            else pl.DataFrame(
                # {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                {"symbol": [], "start_date": [], "end_date": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            )
        )
        self._last_updated_dt = (
            datetime.datetime.today()
            if self._registrations.height == 0
            else to_datetime(self._registrations["end_date"].max())
        )

    @property
    def name(self) -> str:
        """股票池名称"""
        return self._name

    def __str__(self) -> str:
        return f"< 证券池({self._name}) " f" 最新证券:\n {self.list_instruments()} >"

    @property
    def registrations(self) -> pl.DataFrame:
        """股票池出入注册表

        Returns:
            pl.DataFrame -- 注册表
        """
        return self._registrations

    def list_instruments(
        self, trade_date: Optional[Datetime] = None
    ) -> List[datetime.datetime]:
        """列出股票池中的证券

        Keyword Arguments:
            trade_date {Datetime} -- 交易日，若为空，则为当前日期 (default: {None})

        Returns:
            List[InstrumentType] -- 股票列表
        """
        trade_date = (
            to_datetime(trade_date)
            if trade_date is not None
            else datetime.datetime.today()
        )

        inst = self._registrations.filter(
            [(pl.col("start_date") <= trade_date), (pl.col("end_date") >= trade_date)]
        )

        return inst["symbol"].to_list()

    def add_instrument(
        self,
        symbol: str,
        start_date: Datetime,
        end_date: Optional[Datetime] = None,
        #
    ) -> "VXInstruments":
        try:
            symbol = normalize_symbol(symbol)
            start_date = to_datetime(start_date)
            end_date = to_datetime(end_date) if end_date else start_date
        except Exception as e:
            raise ValueError(f"参数错误: {e}")

        self._registrations.vstack(
            pl.DataFrame(
                [
                    {
                        "symbol": symbol,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                ],
                schema={
                    "symbol": str,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                },
            ),
            in_place=True,
        )
        return self

    def update_components(
        self,
        instruments: List[str],
        start_date: Datetime,
        end_date: Datetime,
    ) -> "VXInstruments":
        """按增量更新股票池"""

        end_date = to_datetime(end_date)
        start_date = to_datetime(start_date)

        new_instruments = pl.DataFrame(
            [
                {
                    "symbol": normalize_symbol(symbol),
                    "start_date": start_date,
                    "end_date": end_date,
                }
                for symbol in instruments
            ],
            schema={
                "symbol": pl.Utf8,
                "start_date": pl.Datetime,
                "end_date": pl.Datetime,
            },
        )

        self._registrations = pl.concat([self._registrations, new_instruments])
        self.rebuild()
        return self

    @classmethod
    def load(cls, name: str, instruments_file: Union[str, Path]) -> "VXInstruments":
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if not instruments_file.exists():
            raise FileNotFoundError(f"{instruments_file} 不存在。")
        if instruments_file.suffix in {".csv"}:
            registrations = pl.read_csv(instruments_file)
        elif instruments_file.suffix in {".parquet"}:
            registrations = pl.read_parquet(instruments_file)
        else:
            raise ValueError(f"{instruments_file} 文件格式不支持。")

        return VXInstruments(name, registrations)

    def dump(
        self,
        instruments_file: Union[str, Path],
        *,
        file_suffix: Literal["csv", "parquet"] = "csv",
    ) -> "VXInstruments":
        """保存相关信息"""
        if isinstance(instruments_file, str):
            instruments_file = Path(instruments_file)

        if Path(instruments_file).is_dir():
            instruments_file = Path(instruments_file, f"{self._name}.{file_suffix}")

        if file_suffix == "csv":
            self._registrations.write_csv(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        elif file_suffix == "parquet":
            self._registrations.write_parquet(instruments_file)
            logging.info(f"股票池:{self._name} 保存{instruments_file} 完成。")
        else:
            raise ValueError(f"{file_suffix} 文件格式不支持。")
        return self

    def rebuild(self) -> "VXInstruments":
        """重建登记表"""

        new_registrations = []
        temp_registrations = {}

        for rows in self._registrations.sort(by=["symbol", "start_date"]).iter_rows(
            named=True
        ):
            symbol = rows["symbol"]

            if symbol not in temp_registrations:
                temp_registrations[symbol] = rows
            elif (
                temp_registrations[symbol]["end_date"] + datetime.timedelta(days=1)
                >= rows["start_date"]
                and temp_registrations[symbol]["end_date"] < rows["end_date"]
            ):
                temp_registrations[symbol]["end_date"] = rows["end_date"]

            elif (temp_registrations[symbol]["end_date"]) < rows["start_date"]:
                new_registrations.append(temp_registrations[symbol])
                temp_registrations[symbol] = rows

        new_registrations.extend(temp_registrations.values())
        self._registrations = pl.DataFrame(new_registrations)

        return self

    def all_instruments(self) -> List[str]:
        return self._registrations["symbol"].unique().to_list()

    def union(self, *others: "VXInstruments") -> "VXInstruments":
        """合并另外一个股票池"""
        if len(others) == 1 and isinstance(others[0], (list, tuple)):
            others = others[0]

        registrations = [self._registrations] + [
            other._registrations for other in others
        ]
        self._registrations = pl.concat(registrations)
        self.rebuild()
        return self

    def intersect(self, other: "VXInstruments") -> "VXInstruments":
        """交集"""

        new_registrations: List[Dict[str, Any]] = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            new_registrations.extend(
                {
                    "symbol": rows["symbol"],
                    "start_date": max(rows["start_date"], other_rows["start_date"]),
                    "end_date": min(rows["end_date"], other_rows["end_date"]),
                    # "weight": rows["weight"],
                }
                for other_rows in other.registrations.filter(
                    (pl.col("start_date") < rows["end_date"])
                    & (pl.col("end_date") > rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                ).iter_rows(named=True)
            )

        self._registrations = (
            pl.DataFrame(new_registrations)
            if new_registrations
            else pl.DataFrame(
                # {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                {"symbol": [], "start_date": [], "end_date": [], "weight": []},
                schema={
                    "symbol": pl.Utf8,
                    "start_date": pl.Datetime,
                    "end_date": pl.Datetime,
                    # "weight": pl.Float64,
                },
            )
        )

        self.rebuild()
        return self

    def difference(self, other: "VXInstruments") -> "VXInstruments":
        """差集"""
        new_registrations = []
        for rows in self.registrations.sort(["symbol", "start_date"]).iter_rows(
            named=True
        ):
            for other_rows in (
                other.registrations.filter(
                    (pl.col("start_date") <= rows["end_date"])
                    & (pl.col("end_date") >= rows["start_date"])
                    & (pl.col("symbol") == rows["symbol"])
                )
                .sort("start_date")
                .iter_rows(named=True)
            ):
                if rows["start_date"] < other_rows["start_date"]:
                    new_registrations.append(
                        {
                            "symbol": rows["symbol"],
                            "start_date": rows["start_date"],
                            "end_date": other_rows["start_date"]
                            - datetime.timedelta(days=1),
                            # "weight": rows["weight"],
                        }
                    )

                rows["start_date"] = other_rows["end_date"] + datetime.timedelta(days=1)

                if rows["start_date"] > rows["end_date"]:
                    break

            if rows["start_date"] <= rows["end_date"]:
                new_registrations.append(rows)

        self._registrations = pl.DataFrame(new_registrations)
        self.rebuild()
        return self


if __name__ == "__main__":
    a = VXInstruments("test")
    print(a.registrations)
    a.add_instrument("SHSE.600000", "2022-01-01", "2022-02-28")
    a.add_instrument("SHSE.600000", "2022-03-6", "2022-04-30")
    a.add_instrument("SHSE.600000", "2022-02-01", "2022-03-05")
    a.add_instrument("SHSE.600001", "2022-01-01", "2022-02-28")
    a.add_instrument("SHSE.600001", "2022-03-12", "2022-04-30")
    a.update_components(
        ["SHSE.600000", "SHSE.600001", "SHSE.600002"],
        start_date="2022-05-01",
        end_date="2023-05-01",
    )
    print(a.registrations)
    a.rebuild()
    print(a.registrations)
    print("=" * 60)
    b = VXInstruments("b")

    b.add_instrument("SHSE.600000", "2022-02-14", "2022-03-12")
    b.add_instrument("SHSE.600000", "2021-01-01", "2022-01-12")

    print("-" * 60)
    print(b.registrations)
    print("-" * 60)

    # print(b.registrations)
    # with vxtime.timeit(1):
    #    a.union(b)
    # print(a.registrations)
    a.difference(b)
    # a.union(b)
    print(a.registrations)
