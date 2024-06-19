"""市场预设值清单"""

from typing import Any, Dict
from pydantic import PlainValidator, Field
from vxutils.datamodel.core import VXDataModel
from vxutils.convertors import to_enum
from vxquant.models.constants import SecType
from vxquant.models.nomalize import to_symbol

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

__all__ = ["vxMarketPreset"]

_DEFULAT_SYMBOL_MAP = {
    "SHSE.204": {
        "security_type": "REPO",
        "commission_coeff_peramount": 0.00,
        "commission_coeff_today_peramount": 0.0,
        "tax_coeff_peramount": 0.00,
        "price_tick": 0.0001,
        "volume_unit": 100,
        "upper_limit_ratio": 10000,
        "down_limit_ratio": 0.0,
        "allow_t0": False,
    },
    "SZSE.131": {
        "security_type": "REPO",
        "commission_coeff_peramount": 0.00,
        "commission_coeff_today_peramount": 0.0,
        "tax_coeff_peramount": 0.00,
        "price_tick": 0.0001,
        "volume_unit": 10,
        "upper_limit_ratio": 10000,
        "down_limit_ratio": 0.0,
        "allow_t0": False,
    },
    "SHSE.60": {
        "security_type": "STOCK",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SHSE.68": {
        "security_type": "STOCK",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 100,
        "upper_limit_ratio": 1.2,
        "down_limit_ratio": 0.8,
        "allow_t0": False,
    },
    "SHSE.00": {
        "security_type": "INDEX",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 1,
        "upper_limit_ratio": 100,
        "down_limit_ratio": 0,
        "allow_t0": True,
    },
    "SZSE.39": {
        "security_type": "INDEX",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 1,
        "upper_limit_ratio": 100,
        "down_limit_ratio": 0,
        "allow_t0": True,
    },
    "SHSE.50": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SHSE.51": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SHSE.58": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SHSE.56": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SHSE.10": {
        "security_type": "BOND",
        "commission_coeff_peramount": 0.0008,
        "commission_coeff_today_peramount": 0.0008,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.0001,
        "volume_unit": 10,
        "upper_limit_ratio": 1.3,
        "down_limit_ratio": 0.7,
        "allow_t0": True,
    },
    "SHSE.11": {
        "security_type": "BOND_CONVERTIBLE",
        "commission_coeff_peramount": 0.0008,
        "commission_coeff_today_peramount": 0.0008,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.01,
        "volume_unit": 10,
        "upper_limit_ratio": 1.3,
        "down_limit_ratio": 0.7,
        "allow_t0": True,
    },
    "SZSE.00": {
        "security_type": "STOCK",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SZSE.30": {
        "security_type": "STOCK",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.001,
        "price_tick": 0.01,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SZSE.12": {
        "security_type": "BOND_CONVERTIBLE",
        "commission_coeff_peramount": 0.0008,
        "commission_coeff_today_peramount": 0.0008,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.01,
        "volume_unit": 10,
        "upper_limit_ratio": 1.3,
        "down_limit_ratio": 0.7,
        "allow_t0": True,
    },
    "SZSE.15": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SZSE.16": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
    "SZSE.18": {
        "security_type": "ETFLOF",
        "commission_coeff_peramount": 0.001,
        "commission_coeff_today_peramount": 0.001,
        "tax_coeff_peramount": 0.0,
        "price_tick": 0.001,
        "volume_unit": 100,
        "upper_limit_ratio": 1.1,
        "down_limit_ratio": 0.9,
        "allow_t0": False,
    },
}

# T0的ETF产品
_T0_ETFLOF = [
    "SZSE.161129",
    "SZSE.160723",
    "SZSE.160216",
    "SHSE.501018",
    "SZSE.165513",
    "SZSE.161116",
    "SZSE.161815",
    "SZSE.162719",
    "SZSE.163208",
    "SZSE.164701",
    "SZSE.160416",
    "SZSE.162411",
    "SZSE.160719",
    "SHSE.513500",
    "SHSE.513030",
    "SHSE.513080",
    "SHSE.513100",
    "SZSE.159941",
    "SHSE.513300",
    "SZSE.161128",
    "SZSE.161125",
    "SZSE.161130",
    "SZSE.161126",
    "SZSE.162415",
    "SZSE.161127",
    "SHSE.513050",
    "SZSE.159822",
    "SZSE.159607",
    "SZSE.159605",
    "SZSE.164906",
    "SZSE.164824",
    "SZSE.159740",
    "SZSE.159741",
    "SZSE.159742",
    "SZSE.159823",
    "SZSE.159850",
    "SZSE.159892",
    "SZSE.159920",
    "SZSE.159954",
    "SZSE.159960",
    "SZSE.160322",
    "SZSE.160717",
    "SZSE.160922",
    "SZSE.160924",
    "SZSE.161124",
    "SZSE.161831",
    "SZSE.162416",
    "SZSE.164705",
    "SHSE.501021",
    "SHSE.501025",
    "SHSE.501301",
    "SHSE.501302",
    "SHSE.501303",
    "SHSE.501305",
    "SHSE.501306",
    "SHSE.501307",
    "SHSE.501309",
    "SHSE.501310",
    "SHSE.501311",
    "SHSE.510900",
    "SHSE.513000",
    "SHSE.513010",
    "SHSE.513060",
    "SHSE.513090",
    "SHSE.513130",
    "SHSE.513180",
    "SHSE.513330",
    "SHSE.513520",
    "SHSE.513550",
    "SHSE.513580",
    "SHSE.513600",
    "SHSE.513660",
    "SHSE.513680",
    "SHSE.513880",
    "SHSE.513900",
    "SHSE.513990",
    "SHSE.518880",
    "SZSE.159934",
    "SHSE.518800",
    "SZSE.159937",
    "SHSE.518680",
    "SHSE.518850",
    "SHSE.518600",
    "SHSE.518660",
    "SHSE.518890",
    "SZSE.159812",
    "SHSE.518860",
]
# 现金管理产品
_CASH_SECURITIES = [
    "SHSE.511990",
    "SHSE.511880",
    "SHSE.511660",
    "SHSE.511850",
    "SHSE.511810",
    "SZSE.159001",
    "SHSE.511690",
    "SZSE.159003",
    "SHSE.511800",
    "SHSE.511700",
    "SHSE.511820",
    "SHSE.511650",
    "SHSE.511900",
    "SHSE.511860",
    "SHSE.511620",
    "SZSE.159005",
    "SHSE.511980",
    "SHSE.511600",
    "SHSE.511830",
    "SHSE.511950",
    "SHSE.511670",
    "SHSE.511920",
    "SHSE.511960",
    "SHSE.511970",
    "SHSE.511910",
    "SHSE.511770",
    "SHSE.511930",
]

_DEFAULT_RESET = {
    "security_type": "OTHER",
    "commission_coeff_peramount": 0.001,
    "commission_coeff_today_peramount": 0.001,
    "tax_coeff_peramount": 0.001,
    "price_tick": 0.01,
    "volume_unit": 100,
    "upper_limit_ratio": 100,
    "down_limit_ratio": 0.0,
    "allow_t0": False,
}


class VXMarketPreset(VXDataModel):
    """交易所预设"""

    symbol: str = Field(default="", title="证券代码", description="证券代码")
    security_type: Annotated[SecType, PlainValidator(to_enum)] = Field(
        default="OTHER", title="证券类别", description="证券类别"
    )
    commission_coeff_peramount: float = Field(
        default=0.001, title="佣金系数", description="佣金系数"
    )
    commission_coeff_today_peramount: float = Field(
        default=0.001, title="当日佣金系数", description="当日佣金系数"
    )
    tax_coeff_peramount: float = Field(
        default=0.001, title="印花税系数", description="印花税系数"
    )
    price_tick: float = Field(default=0.01, title="价格跳动", description="价格跳动")
    volume_unit: int = Field(default=100, title="成交单位", description="成交单位")
    upper_limit_ratio: float = Field(
        default=100, title="涨停比例", description="涨停比例"
    )
    down_limit_ratio: float = Field(
        default=0.0, title="跌停比例", description="跌停比例"
    )
    allow_t0: bool = Field(
        default=False, title="是否允许T+0", description="是否允许T+0"
    )

    def model_post_init(self, _: Any) -> None:
        data: Dict[str, Any] = {}
        symbol = to_symbol(
            self.symbol, formatter=lambda exchange, code: f"{exchange[:2]}SE.{code}"
        )
        if symbol[:8] in _DEFULAT_SYMBOL_MAP:
            data.update(**_DEFULAT_SYMBOL_MAP[symbol[:8]])
        elif symbol[:7] in _DEFULAT_SYMBOL_MAP:
            data.update(**_DEFULAT_SYMBOL_MAP[symbol[:7]])

        if symbol in _CASH_SECURITIES:
            data["allow_t0"] = True
            data["security_type"] = "CASH"
            data["commission_coeff_peramount"] = 0.0
            data["commission_coeff_today_peramount"] = 0.0
            data["tax_coeff_peramount"] = 0.0
        elif symbol in _T0_ETFLOF:
            data["allow_t0"] = True

        for key, value in data.items():
            setattr(self, key, value)


# *class vxMarketPreset:
# *    """交易所预设"""
# *
# *    def __init__(self, symbol) -> None:
# *        preset = _DEFAULT_RESET.copy()
# *        if symbol[:8] in _DEFULAT_SYMBOL_MAP:
# *            self.__dict__.update(**_DEFULAT_SYMBOL_MAP[symbol[:8]])
# *
# *        elif symbol[:7] in _DEFULAT_SYMBOL_MAP:
# *            self.__dict__.update(**_DEFULAT_SYMBOL_MAP[symbol[:7]])
# *        else:
# *            self.__dict__.update(**preset)
# *
# *        if symbol in _CASH_SECURITIES:
# *            self.allow_t0 = True
# *            self.security_type = SecType.CASH
# *            self.commission_coeff_peramount = 0.0
# *            self.commission_coeff_today_peramount = 0.0
# *            self.tax_coeff_peramount = 0.0
# *        elif symbol in _T0_ETFLOF:
# *            self.allow_t0 = True
# *
# *    def __getitem__(self, key):
# *        try:
# *            return self.__dict__[key]
# *        except KeyError as e:
# *            raise AttributeError from e


if __name__ == "__main__":
    preset = VXMarketPreset(symbol="513550.SH")
    print(preset.allow_t0)
    print(preset.security_type)
    print(preset.commission_coeff_peramount)
    print(preset.commission_coeff_today_peramount)
    print(preset.tax_coeff_peramount)
    print(preset.price_tick)
    print(preset.volume_unit)
    print(preset)
