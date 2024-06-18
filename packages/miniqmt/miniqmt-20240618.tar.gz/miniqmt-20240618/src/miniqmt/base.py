"""基础接口"""

import time
import polars as pl
import requests
from pathlib import Path
from datetime import datetime, date
from itertools import chain
from typing import Dict, List, Literal, Union, Optional
from vxquant.models.base import VXTick
from vxquant.models.nomalize import to_symbol
from vxquant.models.instruments import VXInstruments
from vxutils import async_map


TENCENT_HQ_URL = "http://qt.gtimg.cn/q={symbols}&random={timestamp}"


TENCENT_COLUMNS = [
    "symbol",
    "name",  # 1: 股票名字
    "code",  # 2: 股票代码
    "lasttrade",  # 3: 当前价格
    "yclose",  # 4: 昨收
    "open",  # 5: 今开
    "volume",  # 6: 成交量（手）
    "outter_vol",  # 7: 外盘
    "intter_vol",  # 8: 内盘
    "bid1_p",  # 9: 买一
    "bid1_v",  # 10: 买一量（手）
    "bid2_p",  # 11: 买二
    "bid2_v",  # 12：买二量（手）
    "bid3_p",  # 13: 买三
    "bid3_v",
    "bid4_p",  # 14：买三量（手）  # 15: 买四
    "bid4_v",  # 16：买四量（手）
    "bid5_p",  # 17: 买五
    "bid5_v",  # 18：卖五量（手）
    "ask1_p",  # 19: 卖一
    "ask1_v",  # 20: 卖一量（手）
    "ask2_p",  # 21: 卖二
    "ask2_v",  # 22：卖二量（手）
    "ask3_p",  # 23: 卖三
    "ask3_v",  # 24：卖三量（手）
    "ask4_p",  # 25: 卖四
    "ask4_v",  # 26：卖四量（手）
    "ask5_p",  # 27: 卖五
    "ask5_v",  # 28：卖五量（手）
    "last_volume",  # 29: 最近逐笔成交
    "created_dt",  # 30: 时间
    "change",  # 31: 涨跌
    "pct_change",  # 32: 涨跌%
    "high",  # 33: 最高
    "low",  # 34: 最低
    "combine",  # 35: 价格/成交量（手）/成交额
    "volume_backup",  # 36: 成交量（手）
    "amount",  # 37: 成交额（万）
    "turnover",  # 38: 换手率
    "pe",  # 39: 市盈率
    "unknow",  # 40:
    "high2",  # 41: 最高
    "low2",  # 42: 最低
    "amplitude",  # 43: 振幅
    "negotiablemv",  # 44: 流通市值
    "totmktcap",  # 45: 总市值
    "pb",  # 46: 市净率
    "uplimit",  # 47: 涨停价
    "downlimit",  # 48: 跌停价
]

VOLUME_COLUMNS = [
    "volume",
    "bid1_v",
    "ask1_v",
    "bid2_v",
    "ask2_v",
    "bid3_v",
    "ask3_v",
    "bid4_v",
    "ask4_v",
    "bid5_v",
    "ask5_v",
]

tencent_formatter = lambda exchange, code: f"{exchange[:2]}{code}".lower()


def get_tencent_hq(session: requests.Session, url) -> List[Dict[str, str]]:
    resp = session.get(url)
    resp.raise_for_status()
    content = resp.text
    ticks = []
    for line in content.split(";"):
        if not line.strip().startswith("v"):
            continue
        data = line.split("=")
        tick = dict(zip(TENCENT_COLUMNS, data[1].split("~")))
        tick["symbol"] = to_symbol(data[0].replace("v_", ""))
        ticks.append(tick)
    return ticks


class VXMdAPI:

    def current(self, *symbols) -> pl.DataFrame:
        """最新实时行情查询接口

        Returns:
            Dict[str, VXTick] -- 行情数据
        """
        urls = [
            TENCENT_HQ_URL.format(
                symbols=",".join(
                    [
                        to_symbol(symbol, formatter=tencent_formatter)
                        for symbol in symbols[start : start + 50]
                    ]
                ),
                timestamp=int(time.time() * 1000),
            )
            for start in range(0, len(symbols), 50)
        ]
        session = requests.Session()
        session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )

        return pl.DataFrame(
            list(chain(*async_map(lambda url: get_tencent_hq(session, url), urls)))
        )

    def calendar(
        self,
        start_date: Optional[Union[str, datetime, date]] = None,
        end_date: Optional[Union[str, datetime, date]] = None,
    ) -> List[datetime]:
        """交易日历查询接口

        Args:
            start_date (str): 开始日期
            end_date (str): 结束日期

        Returns:
            List[datetime] -- 交易日历
        """
        raise NotImplementedError

    def history(
        self,
        symbol: str,
        freq: Literal["1d", "1m", "tick"],
        start_dt: Union[str, datetime, date] = "2005-01-01",
        end_dt: Optional[Union[str, datetime, date]] = None,
    ) -> pl.DataFrame:
        """历史数据接口

        Arguments:
            symbol {str} -- 获取数据的标的代码
            freq {Literal[1d,1m,tick]} -- _description_
            start_dt {Union[str,datetime,date]} -- _description_

        Returns:
            pl.DataFrame -- _description_
        """
        raise NotImplementedError

    def instruments(self, name: str) -> VXInstruments:
        """证券池查询接口

        Args:
            name (str): 证券池名称

        Returns:
            VXInstruments: 证券池名称
        """
        raise NotImplementedError

    def industry(self, name: str) -> VXInstruments:
        """行业查询接口

        Args:
            name (str): 行业名称

        Returns:
            VXInstruments: 行业名称
        """
        raise NotImplementedError


class VXDatabuilder:
    def __init__(self, data_dir: Union[str, Path]) -> None:
        pass

    def get_history_data(
        self,
        symbol: str,
        freq: Literal["1d", "1m", "tick"],
        start_dt: Union[str, datetime, date],
        end_dt: Optional[Union[str, datetime, date]] = None,
    ) -> pl.DataFrame:
        raise NotImplementedError

    def get_instruments(self, name: str) -> VXInstruments:
        raise NotImplementedError

    def get_industry(self, name: str) -> VXInstruments:
        raise NotImplementedError

    def get_calendar(
        self,
        start_dt: Union[str, datetime, date],
        end_dt: Optional[Union[str, datetime, date]] = None,
    ) -> List[datetime]:
        raise NotImplementedError


if __name__ == "__main__":
    mdapi = VXMdAPI()

    ticks = mdapi.current("SZ.000001", "SH.600000")
    print(ticks)
