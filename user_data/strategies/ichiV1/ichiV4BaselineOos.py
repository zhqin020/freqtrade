from freqtrade.strategy import CategoricalParameter, DecimalParameter, IntParameter

from ichiV4 import ichiV4


class ichiV4BaselineOos(ichiV4):
    leverage_long_value = IntParameter(1, 5, default=1, space="buy")
    leverage_short_value = IntParameter(1, 5, default=1, space="sell")

    sell_trend_indicator = CategoricalParameter(
        ["trend_close_1h", "trend_close_2h", "trend_close_4h"],
        default="trend_close_1h",
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