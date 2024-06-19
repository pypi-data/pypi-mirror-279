"""symbol类定义"""

import re
from functools import lru_cache
from typing import Callable, Tuple


def default_formatter(exchange: str, code: str) -> str:
    # return f"{exchange.upper()[:2]}SE.{code}"
    return f"{code}.{exchange.upper()[:2]}"


def symbol_parser(symbol: str) -> Tuple[str, str]:
    # todo 用正则表达式进行进一步优化
    symbol = symbol.strip()

    match_obj = re.match(r"^(\d{6,10})$", symbol)
    if match_obj:
        code = match_obj[1]
        if code[0] in ["0", "1", "2", "3", "4"]:
            exchange = "SZSE"
        elif code[0] in ["5", "6", "7", "8", "9"]:
            exchange = "SHSE"
        else:
            exchange = "BJSE"
        return (exchange, code)

    symbol = symbol.upper()

    match_obj = re.match(r"^[A-Za-z]{2,4}.?([0-9]{6,10})$", symbol)

    if not match_obj:
        match_obj = re.match(r"^([0-9]{6,10}).?[A-Za-z]{2,4}$", symbol)

    if match_obj is None:
        raise ValueError(f"{symbol} format is not support.")

    code = match_obj[1]
    exchange = symbol.replace("SE", "").replace(".", "").replace(code, "")
    if exchange in {"OF", "ETF", "LOF", ""}:
        exchange = "SZSE" if code[0] in ["0", "1", "2", "3", "4"] else "SHSE"
    elif exchange in {"XSHG", "XSZG", "XBJG"}:
        exchange = exchange.replace("X", "").replace("G", "")
    exchange = exchange if len(exchange) > 2 else f"{exchange}SE"
    return (exchange.upper(), code)


@lru_cache(200)
def to_symbol(
    instrument: str, *, formatter: Callable[[str, str], str] = default_formatter
) -> str:
    """格式化symbol

    Arguments:
        instrument {str} -- 需要格式化的symbol

    Keyword Arguments:
        formatter {Callable[[str, str], str]} -- 格式化函数 (default: {default_formatter})

    Returns:
        str -- 格式化后的symbol
    """
    if instrument.upper() in {"CNY", "CACH"}:
        return "CNY"

    exchange, code = symbol_parser(instrument)
    return formatter(exchange=exchange, code=code)


if __name__ == "__main__":
    print(symbol_parser("sh600000"))
    print(symbol_parser("SH600000"))
    print(symbol_parser("SZ600000"))
    print(symbol_parser("600000.sh"))
    print(symbol_parser("600000"))
    print(symbol_parser("600000SH"))
    print(symbol_parser("600000SZ"))
    print(symbol_parser("600000.XSHG"))
    print(symbol_parser("600000.XSZG"))
    print(symbol_parser("600000.SHSE"))
    print(symbol_parser("600000.SZSE"))
    print(symbol_parser("600000.SH"))
    print(symbol_parser("600000.SZ"))
    print(symbol_parser("600000.BJ"))
    print(symbol_parser("600000OF"))
    print(symbol_parser("600000ETF"))
    print(symbol_parser("600000LOF"))
    print(symbol_parser("600000CNY"))
    print(symbol_parser("600000CACH"))
    print(symbol_parser("600000.XSHG"))

    print(to_symbol("600000"))
    print(to_symbol("600000SH"))
    print(to_symbol("600000SZ"))
    print(to_symbol("600000.XSHG"))
    print(to_symbol("600000.XSZG"))
    print(to_symbol("600000.SHSE"))
    print(to_symbol("600000.SZSE"))
    print(to_symbol("600000.SH"))
    print(to_symbol("600000.SZ"))
    print(to_symbol("600000.BJ"))
    print(to_symbol("600000OF"))
    print(to_symbol("600000ETF"))
    print(to_symbol("600000LOF"))
    print(to_symbol("SHSE.600000"))
    print(to_symbol("SZSE.600000"))
    print(to_symbol("CNY"))
    print(to_symbol("CACH"))
    print(to_symbol("SH600000"))
