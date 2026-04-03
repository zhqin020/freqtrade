import logging
from datetime import datetime
from typing import Optional

import pandas as pd
import talib.abstract as ta

from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    merge_informative_pair,
)

"""
/freqtrade backtesting --strategy BoxTheoryStrat --timeframe 1h -c user_data/config.json -v --timerange 20240101-
"""
logger = logging.getLogger(__name__)


class BoxTheoryStrat(IStrategy):
    """
    BoxTheoryStrat - Optimized Box Theory (Darvas Box) with DCA.
    Supports Long and Short positions.
    Includes Trend filtering (EMA200), Volume Exhaustion, and HTF Reversal Safety Exits.
    """

    # Strategy Interface Version
    INTERFACE_VERSION = 3

    # Main timeframe: 15m
    timeframe = "15m"
    inf_1h = "1h"
    inf_4h = "4h"

    # Can this strategy go short?
    can_short = True

    # Optimized ROI from Hyperopt
    minimal_roi = {
        "0": 0.119,
        "60": 0.102,
        "127": 0.015,
        "344": 0
    }

    # Consolidated Stoploss (Prevent extreme DCA drawdowns)
    stoploss = -0.197

    # Trailing stoploss (To protect gains after multi-entry DCA recovery)
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.025
    trailing_only_offset_is_reached = True

    # DCA / Position Adjustment
    position_adjustment_enable = True
    max_dca_multiplier = 1.6  # Total stake multiplier limit

    # Hyperoptable Parameters
    box_window_15m = IntParameter(6, 40, default=23, space="buy")
    box_window_1h = IntParameter(6, 40, default=12, space="buy")
    box_window_4h = IntParameter(24, 100, default=54, space="buy")

    # Range Thresholds
    range_threshold = DecimalParameter(0.01, 0.15, default=0.078, space="buy")
    min_touches = IntParameter(2, 5, default=2, space="buy")

    # Volume Confirmation
    volume_exhaustion_threshold = DecimalParameter(0.5, 1.5, default=0.919, space="buy")
    breakout_volume_threshold = DecimalParameter(1.5, 4.0, default=2.996, space="buy")

    # DCA Parameters
    dca_min_pct = DecimalParameter(0.01, 0.05, default=0.015, space="buy")  # N% drop
    max_entry_count = IntParameter(1, 10, default=5, space="buy")

    # Leverage
    leverage_val = IntParameter(1, 5, default=1, space="buy")

    def informative_pairs(self):
        pairs = self.dp.current_whitelist()
        informative_pairs = [(pair, self.inf_4h) for pair in pairs]
        informative_pairs += [(pair, self.inf_1h) for pair in pairs]
        return informative_pairs

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: str | None,
        side: str,
        **kwargs,
    ) -> float:
        return float(self.leverage_val.value)

    def custom_stake_amount(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_stake: float,
        min_stake: float | None,
        max_stake: float,
        leverage: float,
        entry_tag: str | None,
        side: str,
        **kwargs,
    ) -> float:
        # Initial entry is smaller to allow more budget for DCA
        return proposed_stake / 4.0

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Get Informative Data
        inf_4h_df = self.dp.get_pair_dataframe(pair=metadata["pair"], timeframe=self.inf_4h)
        inf_1h_df = self.dp.get_pair_dataframe(pair=metadata["pair"], timeframe=self.inf_1h)

        # 4H Indicators (Big Zone & Trend)
        inf_4h_df["ema200"] = ta.EMA(inf_4h_df, timeperiod=200)
        inf_4h_df["box_top"] = inf_4h_df["high"].rolling(window=self.box_window_4h.value).max()
        inf_4h_df["box_bottom"] = inf_4h_df["low"].rolling(window=self.box_window_4h.value).min()

        # 1H Indicators (Middle Zone)
        inf_1h_df["box_top"] = inf_1h_df["high"].rolling(window=self.box_window_1h.value).max()
        inf_1h_df["box_bottom"] = inf_1h_df["low"].rolling(window=self.box_window_1h.value).min()
        inf_1h_df["touch_top"] = (
            (abs(inf_1h_df["high"] - inf_1h_df["box_top"]) / inf_1h_df["box_top"] < 0.002)
            .rolling(window=self.box_window_1h.value)
            .sum()
        )
        inf_1h_df["touch_bottom"] = (
            (abs(inf_1h_df["low"] - inf_1h_df["box_bottom"]) / inf_1h_df["box_bottom"] < 0.002)
            .rolling(window=self.box_window_1h.value)
            .sum()
        )
        inf_1h_df["is_valid"] = (
            (inf_1h_df["touch_top"] >= self.min_touches.value)
            & (inf_1h_df["touch_bottom"] >= self.min_touches.value)
            & (
                (inf_1h_df["box_top"] - inf_1h_df["box_bottom"]) / inf_1h_df["close"]
                < self.range_threshold.value
            )
        )

        # Merge informative data
        dataframe = merge_informative_pair(dataframe, inf_4h_df, self.timeframe, self.inf_4h, ffill=True)
        dataframe = merge_informative_pair(dataframe, inf_1h_df, self.timeframe, self.inf_1h, ffill=True)

        # 15M Indicators (Small Zone / Execution)
        dataframe["box_top"] = dataframe["high"].rolling(window=self.box_window_15m.value).max()
        dataframe["box_bottom"] = dataframe["low"].rolling(window=self.box_window_15m.value).min()

        # Volume Confirmation
        dataframe["volume_sma"] = ta.SMA(dataframe, timeperiod=20, price="volume")
        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        
        # Trend Filters (4H EMA 200)
        is_bullish = dataframe[f"close_{self.inf_4h}"] > dataframe[f"ema200_{self.inf_4h}"]
        is_bearish = dataframe[f"close_{self.inf_4h}"] < dataframe[f"ema200_{self.inf_4h}"]

        # Long Entry Conditions
        # 1. Breakout Long (Bullish Trend + 1H Box Breakout + Volume Spike)
        dataframe.loc[
            (
                is_bullish &
                dataframe[f"is_valid_{self.inf_1h}"].shift(1) &
                (dataframe["close"] > dataframe[f"box_top_{self.inf_1h}"].shift(1)) &
                (dataframe["volume"] > dataframe["volume_sma"] * self.breakout_volume_threshold.value) &
                (dataframe["rsi"] < 70)
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "breakout_long")

        # 2. Fake Breakout reversal Long (Slight dip + Rapid Reversal + Exhausted Volume)
        dataframe.loc[
            (
                is_bullish &
                (dataframe["low"].shift(1) < dataframe[f"box_bottom_{self.inf_1h}"].shift(2)) &
                (dataframe["close"] > dataframe[f"box_bottom_{self.inf_1h}"].shift(1)) &
                (dataframe["volume"] < dataframe["volume_sma"] * self.volume_exhaustion_threshold.value) &
                (dataframe["rsi"] > 35) & (dataframe["rsi"] < 50)
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "fake_breakout_long")

        # 3. Pullback Long (Bullish Trend + Price at 1H Box Bottom + Volume Exhaustion)
        dataframe.loc[
            (
                is_bullish &
                (dataframe["close"] <= dataframe[f"box_bottom_{self.inf_1h}"] * 1.002) &
                (dataframe["volume"] < dataframe["volume_sma"] * self.volume_exhaustion_threshold.value) &
                (dataframe["rsi"] > 35)
            ),
            ["enter_long", "enter_tag"],
        ] = (1, "pullback_long")

        # Short Entry Conditions
        # 1. Breakout Short (Bearish Trend + 1H Box Breakdown + Volume Spike)
        dataframe.loc[
            (
                is_bearish &
                dataframe[f"is_valid_{self.inf_1h}"].shift(1) &
                (dataframe["close"] < dataframe[f"box_bottom_{self.inf_1h}"].shift(1)) &
                (dataframe["volume"] > dataframe["volume_sma"] * self.breakout_volume_threshold.value) &
                (dataframe["rsi"] > 30)
            ),
            ["enter_short", "enter_tag"],
        ] = (1, "breakout_short")

        # 2. Fake Breakout reversal Short (Slight peak + Rapid Reversal + Exhausted Volume)
        dataframe.loc[
            (
                is_bearish &
                (dataframe["high"].shift(1) > dataframe[f"box_top_{self.inf_1h}"].shift(2)) &
                (dataframe["close"] < dataframe[f"box_top_{self.inf_1h}"].shift(1)) &
                (dataframe["volume"] < dataframe["volume_sma"] * self.volume_exhaustion_threshold.value) &
                (dataframe["rsi"] < 65) & (dataframe["rsi"] > 50)
            ),
            ["enter_short", "enter_tag"],
        ] = (1, "fake_breakout_short")

        # 3. Pullback Short (Bearish Trend + Price at 1H Box Top + Volume Exhaustion)
        dataframe.loc[
            (
                is_bearish &
                (dataframe["close"] >= dataframe[f"box_top_{self.inf_1h}"] * 0.998) &
                (dataframe["volume"] < dataframe["volume_sma"] * self.volume_exhaustion_threshold.value) &
                (dataframe["rsi"] < 65)
            ),
            ["enter_short", "enter_tag"],
        ] = (1, "pullback_short")

        return dataframe

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # HTF Reversal Exit (Safety Stop)
        # Long Exit: Price breaches 4H box bottom (Sign of real breakdown)
        dataframe.loc[
            (dataframe["close"] < dataframe[f"box_bottom_{self.inf_4h}"]), "exit_long"
        ] = 1

        # Short Exit: Price breaches 4H box top (Sign of real breakout)
        dataframe.loc[
            (dataframe["close"] > dataframe[f"box_top_{self.inf_4h}"]), "exit_short"
        ] = 1

        return dataframe

    def adjust_trade_position(
        self,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        min_stake: float | None,
        max_stake: float,
        current_entry_rate: float,
        current_exit_rate: float,
        current_entry_profit: float,
        current_exit_profit: float,
        **kwargs,
    ) -> float | None:
        """
        Optimized DCA logic for Box Theory.
        DCA Suspension: Stop adding if the HTF (Big Zone) is breached.
        """

        if trade.nr_of_successful_entries >= self.max_entry_count.value:
            return None

        # --- SAFETY: CHECK FOR OPEN ORDERS ---
        # If there's already a pending entry order, do not add more.
        if any(o.status == "open" for o in trade.orders):
            return None

        # Get Analyzed Dataframe
        dataframe, _ = self.dp.get_analyzed_dataframe(trade.pair, self.timeframe)
        if dataframe.empty:
            return None

        last_candle = dataframe.iloc[-1].squeeze()
        
        # --- DCA SUSPENSION CHECK (HTF Reversal) ---
        if not trade.is_short:
            # Long DCA Suspension: If price is below 4H box bottom, do NOT DCA
            if current_rate < last_candle[f"box_bottom_{self.inf_4h}"]:
                return None
        else:
            # Short DCA Suspension: If price is above 4H box top, do NOT DCA
            if current_rate > last_candle[f"box_top_{self.inf_4h}"]:
                return None

        # --- ANCHORING: GET ACCURATE LAST ENTRY PRICE ---
        # We MUST use the price of the VERY LAST filled entry, not the average open_rate.
        entry_sides = ["buy", "long"] if not trade.is_short else ["sell", "short"]
        filled_entries = [o for o in trade.orders if o.status == "closed" and o.side in entry_sides]

        if not filled_entries:
            # Fallback (should not happen if trade is open), but safety first.
            last_entry_price = trade.open_rate
        else:
            # Use the price of the last successful entry order
            last_order = filled_entries[-1]
            last_entry_price = getattr(last_order, "average_price", getattr(last_order, "price", trade.open_rate))

        if not trade.is_short:
            # LONG DCA
            # 1. Price drop > N%
            pct_drop = (last_entry_price - current_rate) / last_entry_price

            # 2. Reaches bottom of boxes (1H or 15M)
            at_box_bottom = (current_rate <= last_candle[f"box_bottom_{self.inf_1h}"]) or (
                current_rate <= last_candle["box_bottom"]
            )

            if pct_drop >= self.dca_min_pct.value and at_box_bottom:
                return trade.stake_amount
        else:
            # SHORT DCA
            # 1. Price rise > N%
            pct_rise = (current_rate - last_entry_price) / last_entry_price

            # 2. Reaches top of boxes (1H or 15M)
            at_box_top = (current_rate >= last_candle[f"box_top_{self.inf_1h}"]) or (
                current_rate >= last_candle["box_top"]
            )

            if pct_rise >= self.dca_min_pct.value and at_box_top:
                return trade.stake_amount

        return None
