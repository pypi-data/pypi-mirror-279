"""miniQMT adapter for VXQuant API"""

import polars as pl
import logging
import time
from datetime import datetime, date
from pathlib import Path
from typing import Union, Optional, Dict, Any, List, Literal
from multiprocessing import Lock
from xtquant import xtdata
from xtquant import xtconstant
from xtquant.xttype import (
    StockAccount,
    XtAsset,
    XtAccountStatus,
    XtPosition,
    XtOrder,
    XtTrade,
    XtOrderError,
    XtCancelError,
)
from xtquant.xttrader import XtQuantTrader, XtQuantTraderCallback
from miniqmt.adapters import (
    miniqmt_order_adapter,
    miniqmt_execrpt_adapter,
    miniqmt_position_adapter,
    miniqmt_tick_adapter,
    miniqmt_cashinfo_adapter,
)
from vxquant.models.preset import VXMarketPreset
from vxquant.models.nomalize import to_symbol
from vxquant.models.base import VXTick, VXOrder, VXPosition, VXExecRpt, VXCashInfo
from vxutils.datamodel.dborm import VXDataBase, VXDBSession
from vxutils import retry, to_datetime, to_timestring
from vxsched import VXPublisher

xtdata.enable_hello = False


class VXMiniQMTTDAPI(XtQuantTraderCallback):

    def __init__(
        self,
        path: Union[str, Path],
        account_id: str,
        account_type: str = "STOCK",
    ) -> None:
        self._xt_trader: Optional[XtQuantTrader] = None
        self._path = path
        self._account = StockAccount(
            account_id=account_id, account_type=account_type.upper()
        )
        self._publisher = VXPublisher()
        self._lock = Lock()

    def set_publisher(self, publisher: VXPublisher) -> VXPublisher:
        """设置事件发布器

        Arguments:
            publisher {VXPublisher} -- 发布器对象

        Returns:
            VXPublisher -- 内部发布器对象
        """
        self._publisher = publisher
        return self._publisher

    @property
    @retry(
        3,
        cache_exceptions=(RuntimeError, ConnectionError, TimeoutError),
        delay=0.3,
        backoff=2,
    )
    def trader(self) -> XtQuantTrader:
        with self._lock:
            if self._xt_trader:
                return self._xt_trader

            self._xt_trader = XtQuantTrader(self._path, int(time.time()), callback=self)
            # 不要阻塞下单通道
            self._xt_trader.set_relaxed_response_order_enabled(True)
            self._xt_trader.start()
            connect_result = self._xt_trader.connect()
            if connect_result != 0:
                raise ConnectionError(
                    f"Failed to start XtQuantTrader, connect error_code: {connect_result}"
                )
            logging.info("XtQuantTrader started successfully...")

            subscribe_result = self._xt_trader.subscribe(self._account)
            if subscribe_result != 0:
                raise RuntimeError(
                    f"Failed to subscribe account, subscribe error_code: {subscribe_result}"
                )
            logging.info(
                f"Account[{self._account.account_id}] subscribed successfully..."
            )
            return self._xt_trader

    def close(self) -> None:
        with self._lock:
            try:
                if self._xt_trader:
                    self._xt_trader.stop()
            except Exception as e:
                logging.error(f"Failed to stop XtQuantTrader: {e}")
            finally:
                self._xt_trader = None

    def current(self, *symbols: str) -> Dict[str, VXTick]:
        ticks = xtdata.get_full_tick(symbols)
        datas = {}
        for stock_code, tick in ticks.items():
            tick["stock_code"] = stock_code
            datas[stock_code] = miniqmt_tick_adapter(tick)
        return datas

    def get_positions(self, symbol: str = "") -> Dict[str, VXPosition]:

        positions = self.trader.query_stock_positions(self._account)
        return dict(
            miniqmt_position_adapter(pos, key="symbol")
            for pos in positions
            if pos.volume > 0
        )

    def get_orders(
        self, order_id: str = "", is_open: bool = True
    ) -> Dict[str, VXOrder]:

        orders = self.trader.query_stock_orders(
            self._account, cancelable_only=(not is_open)
        )
        return (
            dict(miniqmt_order_adapter(order, key="order_id") for order in orders)
            if order_id == ""
            else {
                order.order_id: miniqmt_order_adapter(order)
                for order in orders
                if order.order_id == order_id
            }
        )

    def get_trades(self, trade_id: str = "") -> Dict[str, VXExecRpt]:
        trades = self.trader.query_stock_trades(self._account)
        return dict(
            miniqmt_execrpt_adapter(trade, key="execrpt_id") for trade in trades
        )

    def get_cash(self) -> VXCashInfo:
        cash = self.trader.query_stock_asset(self._account)
        return miniqmt_cashinfo_adapter(cash)

    def order_batch(self, *orders: VXOrder) -> List[VXOrder]:

        for order in orders:

            order_id = self.trader.order_stock(
                self._account,
                order.symbol,
                order_type=(
                    xtconstant.STOCK_BUY
                    if order.order_side.name == "Buy"
                    else xtconstant.STOCK_SELL
                ),
                order_volume=order.volume,
                price_type=(
                    xtconstant.FIX_PRICE
                    if order.order_type.name == "Limit"
                    else xtconstant.MARKET_PEER_PRICE_FIRST
                ),
                price=order.price,
                strategy_name=order.strategy_id,
                order_remark=order.order_remark,
            )
            order.order_id = str(order_id)
            logging.debug(f"Order placed: {order}")

        return list(orders)

    def order_volume(
        self,
        symbol: str,
        volume: int,
        price: Optional[float] = None,
        order_remark: str = "",
        strategy_id: str = "",
    ) -> VXOrder:
        """下单函数

        Arguments:
            symbol {str} -- 证券代码
            volume {int} -- 下单数量，正数为买，负数为卖
            price {Optional[float]} -- 委托价格 (default: {None})
            order_remark {str} -- 下单备注 (default: {""})
            strategy_id {str} -- 策略ID (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        symbol = to_symbol(symbol)
        order_side = "Buy" if volume > 0 else "Sell"
        order_type = (
            "Market"
            if price is None
            and VXMarketPreset(symbol=symbol).security_type.name != "BOND_CONVERTIBLE"
            else "Limit"
        )
        if price is None:
            ticks = xtdata.get_full_tick([symbol])
            price = (
                ticks[symbol]["askPrice"][0]
                if order_side == "Buy"
                else ticks[symbol]["bidPrice"][0]
            )

        order = VXOrder(
            account_id=self._account.account_id,
            symbol=symbol,
            volume=abs(volume),
            price=price,
            order_side=order_side,
            order_type=order_type,
            position_effect="Open" if volume > 0 else "Close",
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

        return self.order_batch(order)[0]

    def order_cancel(self, order: Union[str, VXOrder]) -> None:
        """撤单函数

        Arguments:
            order_id {str} -- 委托订单号
        """

        order_id = int(order.order_id if isinstance(order, VXOrder) else order)
        cancel_result = self.trader.cancel_order_stock(self._account, order_id)
        if cancel_result != 0:
            raise RuntimeError(f"Failed to cancel order: {order_id}")

    def auto_repo(
        self,
        reversed_balance: float = 0.0,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> Optional[VXOrder]:
        """自动回购函数

        Arguments:
            reversed_balance {float} -- 回购金额
            symbols {List[str]} -- 证券代码列表

        Keyword Arguments:
            strategy_id {str} -- 策略ID (default: {""})
            order_remark {str} -- 下单备注 (default: {""})

        Returns:
            VXOrder -- 返回下单订单信息
        """
        cash = self.get_cash()
        if cash.available < reversed_balance:
            raise ValueError("Available cash is not enough for repo...")

        target_repo_balance = cash.available - reversed_balance
        target_repo_volume = int(target_repo_balance // 100 // 10 * 10)
        if target_repo_volume <= 0:
            return None

        if not symbols:
            symbols = ["131810.SZ", "204001.SH"]

        ticks = self.current(*symbols)
        target_repo_symbol = ""
        for symbol in symbols:
            tick = ticks.get(symbol, None)
            if not tick:
                logging.warning(f"Tick data for {symbol} is not available...")
                continue
            if (
                target_repo_symbol == ""
                or tick.ask1_p > ticks[target_repo_symbol].ask1_p
            ):
                target_repo_symbol = symbol
        if target_repo_symbol == "":
            logging.warning("No available tick data for repo...")
            return None

        logging.info(f"Auto repo: {target_repo_symbol} {target_repo_volume}")
        return self.order_volume(
            symbol=symbols[0],
            volume=-target_repo_volume,
            price=ticks[target_repo_symbol].bid1_p,
            order_remark=order_remark,
            strategy_id=strategy_id,
        )

    def auto_ipo_bond_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        """自动新债申购函数

        Arguments:
            symbols {List[str]} -- 申购证券代码列表，若为空则根据策略自动选择，否则按照列表顺序申购
            strategy_id {str} -- 策略ID
            order_remark {str} -- 交易备注

        Returns:
            List[VXOrder] -- _description_
        """

        ipos = self.trader.query_ipo_data()
        orders = []
        for symbol, info in ipos.items():
            if info["type"] != "BOND":
                continue

            if symbols is None or symbol in symbols:
                order = self.order_volume(
                    symbol=symbol,
                    volume=info["maxPurchaseNum"],
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO BOND: {symbol} {info}")
        return orders

    def auto_ipo_stock_purchase(
        self,
        symbols: Optional[List[str]] = None,
        strategy_id: str = "",
        order_remark: str = "",
    ) -> List[VXOrder]:
        orders = []

        ipo_limits = self.trader.query_ipo_data(self._account)
        ipos = self.trader.query_ipo_data()

        for symbol, info in ipos.items():
            if info["type"] != "STOCK":
                continue

            if symbols is None or symbol in symbols:
                if symbol.startswith("0"):
                    ipo_limit = ipo_limits["SZ"]
                elif symbol.startswith("787"):
                    ipo_limit = ipo_limits["SH"]
                else:
                    ipo_limit = ipo_limits["KCB"]

                order = self.order_volume(
                    symbol=symbol,
                    volume=min(info["maxPurchaseNum"], ipo_limit),
                    price=info["issuePrice"],
                    order_remark=order_remark,
                    strategy_id=strategy_id,
                )
                orders.append(order)
                logging.info(f"Auto IPO STOCK: {symbol} {info}")
        return orders

    def on_account_status(self, account_status: XtAccountStatus) -> None:
        if account_status.status == xtconstant.ACCOUNT_STATUS_OK:
            logging.debug(f"Account status: {account_status.status}")
        else:
            logging.error(f"Account status error: {account_status.status}")

    def on_disconnected(self) -> None:
        """掉线通知回调函数"""
        try:
            logging.error("Disconnected from server... waiting for reconnect...")
            with self._lock:
                if self._xt_trader:
                    self._xt_trader.stop()
                    self._xt_trader = None
        except Exception as e:
            logging.error(f"Failed to process disconnected event: {e}")

    def on_stock_asset(self, data: XtAsset) -> None:
        logging.info(f"Stock asset: {data}")

    def on_stock_order(self, data: XtOrder) -> None:
        """委托更新回调函数

        Arguments:
            data {XtOrder} -- 交易订单信息
        """
        try:
            logging.info(f"Order updated: {data}")
            order = miniqmt_order_adapter(data)
            logging.debug(f"Receive order status updated: {order}")
            logging.debug(id(self._publisher))
            self._publisher(
                "on_order_status",
                data={"order": order},
                channel=self._account.account_id,
            )
        except Exception as e:
            logging.error(f"Failed to process order status: {e}")

    def on_stock_position(self, data: XtPosition) -> None:
        logging.error(f"Stock position: {data}")

    def on_stock_trade(self, data: XtTrade) -> None:
        """成交回报回调函数

        Arguments:
            data {XtTrade} -- 成交信息
        """
        try:
            logging.info(f"Trade report: {data}")
            execrpt = miniqmt_execrpt_adapter(data)
            logging.debug(f"Receive trade report: {execrpt}")
            self._publisher(
                "on_execution_report",
                data={"execrpt": execrpt},
                channel=self._account.account_id,
            )
        except Exception as e:
            logging.error(f"Failed to process trade report: {e}")

    def on_order_error(self, data: XtOrderError) -> None:
        """委托错误回调函数

        Arguments:
            data {XtOrderError} -- 报错信息
        """
        try:

            qmt_orders = self.trader.query_stock_orders(self._account)
            for qmt_order in qmt_orders:
                if qmt_order.order_id == data.order_id:
                    order = miniqmt_order_adapter(qmt_order)
                    order.reject_reason = f"{data.error_id}--{data.error_msg}"
                    order.status = "Rejected"
                    logging.warning(
                        f"Order {data.order_id} error: {order.error_id}--{order.error_msg}"
                    )
                    self._publisher(
                        "on_order_status",
                        data={"order": order},
                        channel=self._account.account_id,
                    )
                    break
        except Exception as e:
            logging.error(f"Failed to process order error: {e}")

    def on_cancel_error(self, data: XtCancelError) -> None:
        logging.warning(
            f"Order {data.order_id} Cancel error: {data.error_id}--{data.error_msg}"
        )


class VXMiniQMTMDAPI:
    def __init__(self) -> None:
        pass

    def current(self, *symbols) -> Dict[str, VXTick]:
        """最新实时行情查询接口

        Returns:
            Dict[str, VXTick] -- 行情数据
        """

        ticks = xtdata.get_full_tick(symbols)
        datas = {}
        for stock_code, tick in ticks.items():
            tick["stock_code"] = stock_code
            datas[stock_code] = miniqmt_tick_adapter(tick)
        return datas

    def calendar(
        self,
        start_date: Union[str, datetime, date] = "",
        end_date: Union[str, datetime, date] = "",
    ) -> List[datetime]:
        """交易日历查询接口

        Args:
            start_date (str): 开始日期
            end_date (str): 结束日期

        Returns:
            List[datetime] -- 交易日历
        """
        # xtdata.download_holiday_data()
        start_date = (
            to_timestring(start_date, fmt="%Y%m%d") if start_date else "20050101"
        )
        end_date = (
            to_timestring(end_date, fmt="%Y%m%d")
            if end_date
            else datetime.today().replace(day=31, month=12).strftime("%Y%m%d")
        )
        trade_dates = xtdata.get_trading_dates("SH", start_date, end_date)
        return list(map(lambda x: to_datetime(x / 1000), trade_dates))

    def history(
        self,
        symbols: List[str],
        freq: Literal["1d", "1m", "tick"] = "1d",
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
        stock_list = xtdata.get_stock_list_in_sector("沪深A股")
        xtdata.download_history_data2(stock_list, period=freq, callback=on_process)

        start_dt = to_timestring(start_dt, fmt="%Y%m%d")
        end_dt = to_timestring(end_dt, fmt="%Y%m%d") if end_dt else ""
        datas = xtdata.get_market_data(
            field_list=[
                "close",
                "open",
                "high",
                "low",
                "volume",
                "amount",
                "suspendFlag",
            ],
            stock_list=symbols,
            period=freq,
            start_time=start_dt,
            end_time=end_dt,
            dividend_type="front",
        )
        ret = pl.DataFrame(
            {
                "symbol": [],
                "tradedate": [],
                "open": [],
                "high": [],
                "low": [],
                "close": [],
                "volume": [],
                "amount": [],
                "suspendFlag": [],
            }
        )
        for field, value in datas.items():
            df = value.stack()
            if ret.shape[0] == 0:
                ret = pl.DataFrame(
                    {
                        "symbol": df.index.get_level_values(0),
                        "tradedate": df.index.get_level_values(1),
                        field: df,
                    }
                )
            else:
                ret = ret.join(
                    pl.DataFrame(
                        {
                            "symbol": df.index.get_level_values(0),
                            "tradedate": df.index.get_level_values(1),
                            field: df,
                        }
                    ),
                    on=["symbol", "tradedate"],
                    how="inner",
                )

        return ret.sort(["tradedate", "symbol"])


def on_process(data: Dict[str, Any]) -> None:
    print(data)


if __name__ == "__main__":
    import polars as pl

    pl.Config.set_tbl_rows(50)

    tdapi = VXMiniQMTTDAPI("D:\\兴业证券SMT-Q实盘交易\\userdata_mini", "2660007522")
    positions = pl.DataFrame(
        position.model_dump() for symbol, position in tdapi.get_positions().items()
    )
    print(
        positions.sort("market_value")["symbol", "market_value", "available", "volume"]
    )
