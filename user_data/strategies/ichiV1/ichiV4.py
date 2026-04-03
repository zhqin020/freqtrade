# --- Do not remove these libs ---
from freqtrade.strategy.interface import IStrategy
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib
import pandas as pd  # noqa
pd.options.mode.chained_assignment = None  # default='warn'
import technical.indicators as ftt
from functools import reduce
from datetime import datetime, timedelta
from freqtrade.strategy import (
    merge_informative_pair,
    CategoricalParameter,
    DecimalParameter,
    IntParameter,
)
import numpy as np
from freqtrade.strategy import stoploss_from_open
from freqtrade.persistence import Trade


class ichiV4(IStrategy):

    INTERFACE_VERSION = 3
    can_short = True

    # Buy hyperspace params
    buy_trend_above_senkou_level = IntParameter(1, 8, default=1, space="buy")
    buy_trend_bullish_level = IntParameter(1, 8, default=6, space="buy")
    buy_fan_magnitude_shift_value = IntParameter(1, 5, default=3, space="buy")
    buy_min_fan_magnitude_gain = DecimalParameter(
        1.0,
        1.01,
        default=1.002,
        decimals=3,
        space="buy",
    )

    sell_trend_indicator = CategoricalParameter(
        ["trend_close_1h", "trend_close_2h", "trend_close_4h"],
        default="trend_close_2h",
        space="sell",
    )
    sell_fan_magnitude_gain = DecimalParameter(
        0.999,
        1.002,
        default=1.002,
        decimals=3,
        space="sell",
    )
    sell_min_profit_protect = DecimalParameter(
        0.002,
        0.006,
        default=0.002,
        decimals=3,
        space="sell",
    )
    sell_max_trade_minutes = IntParameter(180, 320, default=252, space="sell")
    sell_hard_stop_loss = DecimalParameter(
        -0.025,
        -0.012,
        default=-0.019,
        decimals=3,
        space="sell",
    )
    sell_hard_loss_atr_mult = DecimalParameter(
        1.2,
        2.0,
        default=1.5,
        decimals=1,
        space="sell",
    )
    sell_min_hard_loss_minutes = IntParameter(50, 100, default=71, space="sell")
    sell_timeout_loss = DecimalParameter(
        -0.016,
        -0.006,
        default=-0.014,
        decimals=3,
        space="sell",
    )
    sell_timeout_profit = DecimalParameter(
        0.002,
        0.006,
        default=0.003,
        decimals=3,
        space="sell",
    )

    # Leverage hyperspace params (1-5x, long and short separately)
    leverage_long_value = IntParameter(1, 5, default=1, space="buy")
    leverage_short_value = IntParameter(1, 5, default=1, space="sell")

    # ROI table:
    minimal_roi = {
        "0": 0.059,
        "10": 0.037,
        "41": 0.012,
        "114": 0
    }

    # Stoploss:
    stoploss = -0.275

    # Optimal timeframe for the strategy
    timeframe = '5m'

    startup_candle_count = 300
    process_only_new_candles = False

    trailing_stop = False
    #trailing_stop_positive = 0.002
    #trailing_stop_positive_offset = 0.025
    #trailing_only_offset_is_reached = True

    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    plot_config = {
        'main_plot': {
            # fill area between senkou_a and senkou_b
            'senkou_a': {
                'color': 'green', #optional
                'fill_to': 'senkou_b',
                'fill_label': 'Ichimoku Cloud', #optional
                'fill_color': 'rgba(255,76,46,0.2)', #optional
            },
            # plot senkou_b, too. Not only the area to it.
            'senkou_b': {},
            'trend_close_5m': {'color': '#FF5733'},
            'trend_close_15m': {'color': '#FF8333'},
            'trend_close_30m': {'color': '#FFB533'},
            'trend_close_1h': {'color': '#FFE633'},
            'trend_close_2h': {'color': '#E3FF33'},
            'trend_close_4h': {'color': '#C4FF33'},
            'trend_close_6h': {'color': '#61FF33'},
            'trend_close_8h': {'color': '#33FF7D'}
        },
        'subplots': {
            'fan_magnitude': {
                'fan_magnitude': {}
            },
            'fan_magnitude_gain': {
                'fan_magnitude_gain': {}
            }
        }
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        heikinashi = qtpylib.heikinashi(dataframe)
        dataframe['open'] = heikinashi['open']
        #dataframe['close'] = heikinashi['close']
        dataframe['high'] = heikinashi['high']
        dataframe['low'] = heikinashi['low']

        dataframe['trend_close_5m'] = dataframe['close']
        dataframe['trend_close_15m'] = ta.EMA(dataframe['close'], timeperiod=3)
        dataframe['trend_close_30m'] = ta.EMA(dataframe['close'], timeperiod=6)
        dataframe['trend_close_1h'] = ta.EMA(dataframe['close'], timeperiod=12)
        dataframe['trend_close_2h'] = ta.EMA(dataframe['close'], timeperiod=24)
        dataframe['trend_close_4h'] = ta.EMA(dataframe['close'], timeperiod=48)
        dataframe['trend_close_6h'] = ta.EMA(dataframe['close'], timeperiod=72)
        dataframe['trend_close_8h'] = ta.EMA(dataframe['close'], timeperiod=96)

        dataframe['trend_open_5m'] = dataframe['open']
        dataframe['trend_open_15m'] = ta.EMA(dataframe['open'], timeperiod=3)
        dataframe['trend_open_30m'] = ta.EMA(dataframe['open'], timeperiod=6)
        dataframe['trend_open_1h'] = ta.EMA(dataframe['open'], timeperiod=12)
        dataframe['trend_open_2h'] = ta.EMA(dataframe['open'], timeperiod=24)
        dataframe['trend_open_4h'] = ta.EMA(dataframe['open'], timeperiod=48)
        dataframe['trend_open_6h'] = ta.EMA(dataframe['open'], timeperiod=72)
        dataframe['trend_open_8h'] = ta.EMA(dataframe['open'], timeperiod=96)

        dataframe['fan_magnitude'] = (dataframe['trend_close_1h'] / dataframe['trend_close_8h'])
        dataframe['fan_magnitude_gain'] = dataframe['fan_magnitude'] / dataframe['fan_magnitude'].shift(1)

        ichimoku = ftt.ichimoku(dataframe, conversion_line_period=20, base_line_periods=60, laggin_span=120, displacement=30)
        dataframe['tenkan_sen'] = ichimoku['tenkan_sen']
        dataframe['kijun_sen'] = ichimoku['kijun_sen']
        dataframe['senkou_a'] = ichimoku['senkou_span_a']
        dataframe['senkou_b'] = ichimoku['senkou_span_b']
        dataframe['leading_senkou_span_a'] = ichimoku['leading_senkou_span_a']
        dataframe['leading_senkou_span_b'] = ichimoku['leading_senkou_span_b']
        dataframe['cloud_green'] = ichimoku['cloud_green']
        dataframe['cloud_red'] = ichimoku['cloud_red']

        dataframe['atr'] = ta.ATR(dataframe)

        # ==================== 调试用 ====================
        dataframe['debug_cloud_ok'] = (
            (dataframe['trend_close_5m'] > dataframe['senkou_a']) &
            (dataframe['trend_close_5m'] > dataframe['senkou_b'])
        ).astype(int)
        
        # 调试 EMA 趋势：检查到 4h 级别 (trend_close_4h > trend_open_4h)
        dataframe['debug_bullish_level'] = (dataframe['trend_close_4h'] > dataframe['trend_open_4h']).astype(int)
        
        dataframe['debug_fan_gain_ok'] = (dataframe['fan_magnitude_gain'] >= self.buy_min_fan_magnitude_gain.value).astype(int)
        
        dataframe['debug_fan_rising'] = (
            (dataframe['fan_magnitude'] > dataframe['fan_magnitude'].shift(1)) & 
            (dataframe['fan_magnitude'].shift(1) > dataframe['fan_magnitude'].shift(2))
        ).astype(int)
        
        dataframe['debug_all_buy'] = (
            dataframe['debug_cloud_ok'] & 
            dataframe['debug_bullish_level'] & 
            dataframe['debug_fan_gain_ok'] & 
            dataframe['debug_fan_rising']
        ).astype(int)
        # ================================================

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Trending market
        if self.buy_trend_above_senkou_level.value >= 1:
            conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 2:
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 3:
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 4:
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 5:
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 6:
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 7:
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 8:
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_b'])

        # Trends bullish
        if self.buy_trend_bullish_level.value >= 1:
            conditions.append(dataframe['trend_close_5m'] > dataframe['trend_open_5m'])

        if self.buy_trend_bullish_level.value >= 2:
            conditions.append(dataframe['trend_close_15m'] > dataframe['trend_open_15m'])

        if self.buy_trend_bullish_level.value >= 3:
            conditions.append(dataframe['trend_close_30m'] > dataframe['trend_open_30m'])

        if self.buy_trend_bullish_level.value >= 4:
            conditions.append(dataframe['trend_close_1h'] > dataframe['trend_open_1h'])

        if self.buy_trend_bullish_level.value >= 5:
            conditions.append(dataframe['trend_close_2h'] > dataframe['trend_open_2h'])

        if self.buy_trend_bullish_level.value >= 6:
            conditions.append(dataframe['trend_close_4h'] > dataframe['trend_open_4h'])

        if self.buy_trend_bullish_level.value >= 7:
            conditions.append(dataframe['trend_close_6h'] > dataframe['trend_open_6h'])

        if self.buy_trend_bullish_level.value >= 8:
            conditions.append(dataframe['trend_close_8h'] > dataframe['trend_open_8h'])

        # Trends magnitude
        conditions.append(dataframe['fan_magnitude_gain'] >= self.buy_min_fan_magnitude_gain.value)
        conditions.append(dataframe['fan_magnitude'] > 1)

        for x in range(self.buy_fan_magnitude_shift_value.value):
            conditions.append(dataframe['fan_magnitude'].shift(x+1) < dataframe['fan_magnitude'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

        return dataframe

    def populate_short_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Trending market (bearish side)
        if self.buy_trend_above_senkou_level.value >= 1:
            conditions.append(dataframe['trend_close_5m'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_5m'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 2:
            conditions.append(dataframe['trend_close_15m'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_15m'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 3:
            conditions.append(dataframe['trend_close_30m'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_30m'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 4:
            conditions.append(dataframe['trend_close_1h'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_1h'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 5:
            conditions.append(dataframe['trend_close_2h'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_2h'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 6:
            conditions.append(dataframe['trend_close_4h'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_4h'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 7:
            conditions.append(dataframe['trend_close_6h'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_6h'] < dataframe['senkou_b'])

        if self.buy_trend_above_senkou_level.value >= 8:
            conditions.append(dataframe['trend_close_8h'] < dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_8h'] < dataframe['senkou_b'])

        # Trends bearish
        if self.buy_trend_bullish_level.value >= 1:
            conditions.append(dataframe['trend_close_5m'] < dataframe['trend_open_5m'])

        if self.buy_trend_bullish_level.value >= 2:
            conditions.append(dataframe['trend_close_15m'] < dataframe['trend_open_15m'])

        if self.buy_trend_bullish_level.value >= 3:
            conditions.append(dataframe['trend_close_30m'] < dataframe['trend_open_30m'])

        if self.buy_trend_bullish_level.value >= 4:
            conditions.append(dataframe['trend_close_1h'] < dataframe['trend_open_1h'])

        if self.buy_trend_bullish_level.value >= 5:
            conditions.append(dataframe['trend_close_2h'] < dataframe['trend_open_2h'])

        if self.buy_trend_bullish_level.value >= 6:
            conditions.append(dataframe['trend_close_4h'] < dataframe['trend_open_4h'])

        if self.buy_trend_bullish_level.value >= 7:
            conditions.append(dataframe['trend_close_6h'] < dataframe['trend_open_6h'])

        if self.buy_trend_bullish_level.value >= 8:
            conditions.append(dataframe['trend_close_8h'] < dataframe['trend_open_8h'])

        # Trends magnitude (downward acceleration)
        inv_fan_gain = 1 / self.buy_min_fan_magnitude_gain.value
        conditions.append(dataframe['fan_magnitude_gain'] <= inv_fan_gain)
        conditions.append(dataframe['fan_magnitude'] < 1)

        for x in range(self.buy_fan_magnitude_shift_value.value):
            conditions.append(dataframe['fan_magnitude'].shift(x+1) > dataframe['fan_magnitude'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'short'] = 1

        return dataframe


    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Reduce noisy exits by requiring both trend break and weakening momentum.
        conditions.append(
            qtpylib.crossed_below(
                dataframe['trend_close_5m'],
                dataframe[self.sell_trend_indicator.value],
            )
        )
        conditions.append(dataframe['fan_magnitude_gain'] < self.sell_fan_magnitude_gain.value)
        conditions.append(dataframe['trend_close_5m'] < dataframe['trend_close_15m'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'sell'] = 1

        return dataframe

    def populate_cover_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Reduce noisy short exits by requiring trend reversal and strengthening momentum.
        conditions.append(
            qtpylib.crossed_above(
                dataframe['trend_close_5m'],
                dataframe[self.sell_trend_indicator.value],
            )
        )
        conditions.append(dataframe['fan_magnitude_gain'] > (2 - self.sell_fan_magnitude_gain.value))
        conditions.append(dataframe['trend_close_5m'] > dataframe['trend_close_15m'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'cover'] = 1

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.populate_buy_trend(dataframe, metadata)
        dataframe = self.populate_short_trend(dataframe, metadata)
        if 'buy' in dataframe.columns:
            dataframe.loc[dataframe['buy'] == 1, 'enter_long'] = 1
        if 'short' in dataframe.columns:
            dataframe.loc[dataframe['short'] == 1, 'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.populate_sell_trend(dataframe, metadata)
        dataframe = self.populate_cover_trend(dataframe, metadata)
        if 'sell' in dataframe.columns:
            dataframe.loc[dataframe['sell'] == 1, 'exit_long'] = 1
        if 'cover' in dataframe.columns:
            dataframe.loc[dataframe['cover'] == 1, 'exit_short'] = 1
        return dataframe

    def custom_exit(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs,
    ):
        if not self.dp:
            return None

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if dataframe.empty:
            return None

        last = dataframe.iloc[-1]
        open_minutes = (current_time - trade.open_date_utc).total_seconds() / 60

        if trade.is_short:
            # Lock in short profits only when upward momentum starts to return.
            if current_profit >= self.sell_min_profit_protect.value:
                if (
                    last['fan_magnitude_gain'] > (2 - self.sell_fan_magnitude_gain.value)
                    and last['trend_close_5m'] > last['trend_close_15m']
                ):
                    return 'profit_protect_short'

            atr_pct = 0.0
            if pd.notna(last['atr']) and pd.notna(last['close']) and last['close'] > 0:
                atr_pct = float(last['atr'] / last['close'])

            dynamic_hard_stop = min(
                self.sell_hard_stop_loss.value,
                -atr_pct * self.sell_hard_loss_atr_mult.value,
            )

            # Cut deep short losses when higher timeframe trend flips upward.
            if (
                open_minutes >= self.sell_min_hard_loss_minutes.value
                and current_profit <= dynamic_hard_stop
                and last['trend_close_5m'] > last['trend_close_30m']
                and last['fan_magnitude_gain'] > (2 - self.sell_fan_magnitude_gain.value)
                and last['trend_close_15m'] > last['trend_close_1h']
            ):
                return 'hard_loss_cut_short'

            # Time stop for stale shorts that are not recovering.
            if (
                open_minutes >= self.sell_max_trade_minutes.value
                and current_profit < self.sell_timeout_loss.value
                and last['trend_close_5m'] > last['trend_close_1h']
                and last['fan_magnitude_gain'] > (2 - self.sell_fan_magnitude_gain.value)
            ):
                return 'stale_loss_cut_short'

            # Free capital from long stale shorts with tiny profits.
            if (
                open_minutes >= (self.sell_max_trade_minutes.value * 1.5)
                and current_profit > 0
                and current_profit <= self.sell_timeout_profit.value
                and last['trend_close_5m'] > last['trend_close_15m']
            ):
                return 'stale_profit_exit_short'

            return None

        # Lock in long profits only when momentum cools down.
        if current_profit >= self.sell_min_profit_protect.value:
            if (
                last['fan_magnitude_gain'] < self.sell_fan_magnitude_gain.value
                and last['trend_close_5m'] < last['trend_close_15m']
            ):
                return 'profit_protect'

        atr_pct = 0.0
        if pd.notna(last['atr']) and pd.notna(last['close']) and last['close'] > 0:
            atr_pct = float(last['atr'] / last['close'])

        # In high volatility, give more room before hard-cutting to reduce whipsaws.
        dynamic_hard_stop = min(
            self.sell_hard_stop_loss.value,
            -atr_pct * self.sell_hard_loss_atr_mult.value,
        )

        # Cut deep losses early when higher timeframe trend is also weak.
        if (
            open_minutes >= self.sell_min_hard_loss_minutes.value
            and current_profit <= dynamic_hard_stop
            and last['trend_close_5m'] < last['trend_close_30m']
            and last['fan_magnitude_gain'] < self.sell_fan_magnitude_gain.value
            and last['trend_close_15m'] < last['trend_close_1h']
        ):
            return 'hard_loss_cut'

        # Time stop for stale trades that are not recovering.
        if (
            open_minutes >= self.sell_max_trade_minutes.value
            and current_profit < self.sell_timeout_loss.value
            and last['trend_close_5m'] < last['trend_close_1h']
            and last['fan_magnitude_gain'] < self.sell_fan_magnitude_gain.value
        ):
            return 'stale_loss_cut'

        # Free capital from long stale trades with tiny profits.
        if (
            open_minutes >= (self.sell_max_trade_minutes.value * 1.5)
            and current_profit > 0
            and current_profit <= self.sell_timeout_profit.value
            and last['trend_close_5m'] < last['trend_close_15m']
        ):
            return 'stale_profit_exit'

        return None

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag,
        side: str,
        **kwargs,
    ) -> float:
        if side == 'long':
            return float(min(self.leverage_long_value.value, max_leverage))
        return float(min(self.leverage_short_value.value, max_leverage))
