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


class ichiV2(IStrategy):

    INTERFACE_VERSION = 3

    # NOTE: settings as of the 25th july 21
    # Buy hyperspace params:
    buy_params = {
        "buy_trend_above_senkou_level": 1,
        "buy_trend_bullish_level": 6,
        "buy_fan_magnitude_shift_value": 3,
        "buy_min_fan_magnitude_gain": 1.002 # NOTE: Good value (Win% ~70%), alot of trades
        #"buy_min_fan_magnitude_gain": 1.008 # NOTE: Very save value (Win% ~90%), only the biggest moves 1.008,
    }

    sell_trend_indicator = CategoricalParameter(
        ["trend_close_1h", "trend_close_2h", "trend_close_4h"],
        default="trend_close_2h",
        space="sell",
    )
    sell_fan_magnitude_gain = DecimalParameter(
        0.996,
        1.002,
        default=0.999,
        decimals=3,
        space="sell",
    )
    sell_min_profit_protect = DecimalParameter(
        0.002,
        0.010,
        default=0.004,
        decimals=3,
        space="sell",
    )
    sell_max_trade_minutes = IntParameter(90, 300, default=150, space="sell")
    sell_hard_stop_loss = DecimalParameter(
        -0.040,
        -0.010,
        default=-0.018,
        decimals=3,
        space="sell",
    )
    sell_hard_loss_atr_mult = DecimalParameter(
        1.0,
        3.0,
        default=1.8,
        decimals=1,
        space="sell",
    )
    sell_min_hard_loss_minutes = IntParameter(20, 120, default=45, space="sell")
    sell_timeout_loss = DecimalParameter(
        -0.020,
        -0.002,
        default=-0.005,
        decimals=3,
        space="sell",
    )
    sell_timeout_profit = DecimalParameter(
        0.001,
        0.006,
        default=0.002,
        decimals=3,
        space="sell",
    )

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

    startup_candle_count = 96
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

        return dataframe


    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        conditions = []

        # Trending market
        if self.buy_params['buy_trend_above_senkou_level'] >= 1:
            conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_5m'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 2:
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_15m'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 3:
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_30m'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 4:
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_1h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 5:
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_2h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 6:
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_4h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 7:
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_6h'] > dataframe['senkou_b'])

        if self.buy_params['buy_trend_above_senkou_level'] >= 8:
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_a'])
            conditions.append(dataframe['trend_close_8h'] > dataframe['senkou_b'])

        # Trends bullish
        if self.buy_params['buy_trend_bullish_level'] >= 1:
            conditions.append(dataframe['trend_close_5m'] > dataframe['trend_open_5m'])

        if self.buy_params['buy_trend_bullish_level'] >= 2:
            conditions.append(dataframe['trend_close_15m'] > dataframe['trend_open_15m'])

        if self.buy_params['buy_trend_bullish_level'] >= 3:
            conditions.append(dataframe['trend_close_30m'] > dataframe['trend_open_30m'])

        if self.buy_params['buy_trend_bullish_level'] >= 4:
            conditions.append(dataframe['trend_close_1h'] > dataframe['trend_open_1h'])

        if self.buy_params['buy_trend_bullish_level'] >= 5:
            conditions.append(dataframe['trend_close_2h'] > dataframe['trend_open_2h'])

        if self.buy_params['buy_trend_bullish_level'] >= 6:
            conditions.append(dataframe['trend_close_4h'] > dataframe['trend_open_4h'])

        if self.buy_params['buy_trend_bullish_level'] >= 7:
            conditions.append(dataframe['trend_close_6h'] > dataframe['trend_open_6h'])

        if self.buy_params['buy_trend_bullish_level'] >= 8:
            conditions.append(dataframe['trend_close_8h'] > dataframe['trend_open_8h'])

        # Trends magnitude
        conditions.append(dataframe['fan_magnitude_gain'] >= self.buy_params['buy_min_fan_magnitude_gain'])
        conditions.append(dataframe['fan_magnitude'] > 1)

        for x in range(self.buy_params['buy_fan_magnitude_shift_value']):
            conditions.append(dataframe['fan_magnitude'].shift(x+1) < dataframe['fan_magnitude'])

        if conditions:
            dataframe.loc[
                reduce(lambda x, y: x & y, conditions),
                'buy'] = 1

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

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.populate_buy_trend(dataframe, metadata)
        if 'buy' in dataframe.columns:
            dataframe.loc[dataframe['buy'] == 1, 'enter_long'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe = self.populate_sell_trend(dataframe, metadata)
        if 'sell' in dataframe.columns:
            dataframe.loc[dataframe['sell'] == 1, 'exit_long'] = 1
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

        # Lock in profits only when momentum cools down.
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
