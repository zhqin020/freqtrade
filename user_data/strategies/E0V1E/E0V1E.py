from datetime import datetime, timedelta
import talib.abstract as ta
import pandas_ta as pta
from freqtrade.persistence import Trade
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
from freqtrade.strategy import DecimalParameter, IntParameter, BooleanParameter
from functools import reduce
import warnings

warnings.simplefilter(action="ignore", category=RuntimeWarning)


class E0V1E(IStrategy):
    minimal_roi = {"0": 1}
    timeframe = "1h"

    custom_info: dict = {}
    can_short = True
    process_only_new_candles = True
    startup_candle_count = 240
    order_types = {
        "entry": "market",
        "exit": "market",
        "emergency_exit": "market",
        "force_entry": "market",
        "force_exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
        "stoploss_on_exchange_interval": 60,
        "stoploss_on_exchange_market_ratio": 0.99,
    }

    stoploss = -0.25
    trailing_stop = False
    trailing_stop_positive = 0.002
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    use_custom_stoploss = True

    is_optimize_32 = True
    buy_rsi_fast_32 = IntParameter(
        20, 70, default=57, space="buy", optimize=is_optimize_32
    )
    buy_rsi_32 = IntParameter(15, 60, default=49, space="buy", optimize=is_optimize_32)
    buy_sma15_32 = DecimalParameter(
        0.900, 1, default=0.975, decimals=3, space="buy", optimize=is_optimize_32
    )
    buy_cti_32 = DecimalParameter(
        -1, 1, default=-0.75, decimals=2, space="buy", optimize=is_optimize_32
    )
    
    # Short parameters
    short_rsi_fast_32 = IntParameter(
        20, 70, default=45, space="sell", optimize=is_optimize_32
    )
    short_rsi_32 = IntParameter(40, 85, default=55, space="sell", optimize=is_optimize_32)
    short_sma15_32 = DecimalParameter(
        1.000, 1.100, default=1.025, decimals=3, space="sell", optimize=is_optimize_32
    )
    short_cti_32 = DecimalParameter(
        -1, 1, default=0.75, decimals=2, space="sell", optimize=is_optimize_32
    )

    sell_fastx = IntParameter(50, 100, default=84, space="sell", optimize=True)

    cci_opt = False
    sell_loss_cci = IntParameter(
        low=0, high=600, default=120, space="sell", optimize=cci_opt
    )
    sell_loss_cci_profit = DecimalParameter(
        -0.15, 0, default=-0.05, decimals=2, space="sell", optimize=cci_opt
    )
    buy_rsi_period = IntParameter(10, 190, default=83, space="buy", optimize=True)
    buy_rsi_fast_period = IntParameter(10, 190, default=121, space="buy", optimize=True)
    buy_rsi_slow_period = IntParameter(10, 190, default=139, space="buy", optimize=True)
    buy_sma_period = IntParameter(10, 190, default=35, space="buy", optimize=True)

    @property
    def protections(self):

        return [{"method": "CooldownPeriod", "stop_duration_candles": 18}]

    def custom_stoploss(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs,
    ) -> float:

        if current_profit >= 0.05:
            return -0.002

        if (str(trade.enter_tag) == "buy_new" or str(trade.enter_tag) == "short_new") and current_profit >= 0.03:
            return -0.003

        return None

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # buy_1 indicators
        dataframe["sma_15"] = ta.SMA(
            dataframe, timeperiod=int(self.buy_sma_period.value)
        )
        dataframe["cti"] = pta.cti(dataframe["close"], length=20)
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=int(self.buy_rsi_period.value))
        dataframe["rsi_fast"] = ta.RSI(
            dataframe, timeperiod=int(self.buy_rsi_fast_period.value)
        )
        dataframe["rsi_slow"] = ta.RSI(
            dataframe, timeperiod=int(self.buy_rsi_slow_period.value)
        )

        # profit sell indicators
        stoch_fast = ta.STOCHF(dataframe, 5, 3, 0, 3, 0)
        dataframe["fastk"] = stoch_fast["fastk"]

        dataframe["cci"] = ta.CCI(dataframe, timeperiod=20)

        dataframe["ma120"] = ta.MA(dataframe, timeperiod=120)
        dataframe["ma240"] = ta.MA(dataframe, timeperiod=240)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        conditions = []
        dataframe.loc[:, "enter_tag"] = ""
        buy_1 = (
            (dataframe["rsi_slow"] < dataframe["rsi_slow"].shift(1))
            & (dataframe["rsi_fast"] < self.buy_rsi_fast_32.value)
            & (dataframe["rsi"] > self.buy_rsi_32.value)
            & (dataframe["close"] < dataframe["sma_15"] * self.buy_sma15_32.value)
            & (dataframe["cti"] < self.buy_cti_32.value)
        )

        buy_new = (
            (dataframe["rsi_slow"] < dataframe["rsi_slow"].shift(1))
            & (dataframe["rsi_fast"] < 34)
            & (dataframe["rsi"] > 28)
            & (dataframe["close"] < dataframe["sma_15"] * 0.96)
            & (dataframe["cti"] < self.buy_cti_32.value)
        )

        conditions.append(buy_1)
        dataframe.loc[buy_1, "enter_tag"] += "buy_1"

        conditions.append(buy_new)
        dataframe.loc[buy_new, "enter_tag"] += "buy_new"

        if conditions:
            dataframe.loc[reduce(lambda x, y: x | y, conditions), "enter_long"] = 1
            
        # Short conditions
        short_conditions = []
        short_1 = (
            (dataframe["rsi_slow"] > dataframe["rsi_slow"].shift(1))
            & (dataframe["rsi_fast"] > self.short_rsi_fast_32.value)
            & (dataframe["rsi"] < self.short_rsi_32.value)
            & (dataframe["close"] > dataframe["sma_15"] * self.short_sma15_32.value)
            & (dataframe["cti"] > self.short_cti_32.value)
        )
        
        short_new = (
            (dataframe["rsi_slow"] > dataframe["rsi_slow"].shift(1))
            & (dataframe["rsi_fast"] > 66)
            & (dataframe["rsi"] < 72)
            & (dataframe["close"] > dataframe["sma_15"] * 1.04)
            & (dataframe["cti"] > self.short_cti_32.value)
        )
        
        short_conditions.append(short_1)
        dataframe.loc[short_1, "enter_tag"] += "short_1"
        
        short_conditions.append(short_new)
        dataframe.loc[short_new, "enter_tag"] += "short_new"
        
        if short_conditions:
            dataframe.loc[reduce(lambda x, y: x | y, short_conditions), "enter_short"] = 1
            
        return dataframe

    def custom_exit(
        self,
        pair: str,
        trade: "Trade",
        current_time: "datetime",
        current_rate: float,
        current_profit: float,
        **kwargs,
    ):
        dataframe, _ = self.dp.get_analyzed_dataframe(
            pair=pair, timeframe=self.timeframe
        )
        current_candle = dataframe.iloc[-1].squeeze()

        min_profit = trade.calc_profit_ratio(trade.min_rate)

        ti = self.custom_info.setdefault(trade.id, {"hold": False, "hold1": False})

        if trade.is_short:
            if (
                current_candle["close"] < current_candle["ma120"]
                and current_candle["close"] < current_candle["ma240"]
            ):
                ti["hold"] = True

            if (current_candle["ma120"] - trade.open_rate) / trade.open_rate >= 0.1:
                ti["hold1"] = True

            if current_profit > 0:
                if current_candle["fastk"] < (100 - self.sell_fastx.value):
                    return "fastk_profit_sell_short"

            if min_profit <= -0.1:
                if current_profit > self.sell_loss_cci_profit.value:
                    if current_candle["cci"] < -self.sell_loss_cci.value:
                        return "cci_loss_sell_short"

            if ti["hold1"] and current_candle["close"] > current_candle["ma120"]:
                ti["hold1"] = False
                return "ma120_sell_fast_short"

            if (
                ti["hold"]
                and current_candle["close"] > current_candle["ma120"]
                and current_candle["close"] > current_candle["ma240"]
            ):
                if min_profit <= -0.1:
                    ti["hold"] = False
                    return "ma120_sell_short"
        else:
            if (
                current_candle["close"] > current_candle["ma120"]
                and current_candle["close"] > current_candle["ma240"]
            ):
                ti["hold"] = True

            if (trade.open_rate - current_candle["ma120"]) / trade.open_rate >= 0.1:
                ti["hold1"] = True

            if current_profit > 0:
                if current_candle["fastk"] > self.sell_fastx.value:
                    return "fastk_profit_sell"

            if min_profit <= -0.1:
                if current_profit > self.sell_loss_cci_profit.value:
                    if current_candle["cci"] > self.sell_loss_cci.value:
                        return "cci_loss_sell"

            if ti["hold1"] and current_candle["close"] < current_candle["ma120"]:
                ti["hold1"] = False
                return "ma120_sell_fast"

            if (
                ti["hold"]
                and current_candle["close"] < current_candle["ma120"]
                and current_candle["close"] < current_candle["ma240"]
            ):
                if min_profit <= -0.1:
                    ti["hold"] = False
                    return "ma120_sell"

        return None

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, ["exit_long", "exit_tag"]] = (0, "long_out")
        return dataframe
