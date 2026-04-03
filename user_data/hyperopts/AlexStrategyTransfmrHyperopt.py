from freqtrade.optimize.space import Categorical, Dimension, Integer, Real
from freqtrade.optimize.hyperopt import IHyperOpt

class AlexStrategyTransfmrHyperopt(IHyperOpt):
    @staticmethod
    def indicator_space():
        return [
            Real(0.01, 0.05, name='trailing_stop_positive'),
            Real(0.01, 0.1, name='trailing_stop_positive_offset'),
            Real(-0.05, -0.01, name='stoploss'),
            # ROI table: 这里只做示例，实际可用 Categorical 或自定义空间
            # Categorical([(0.01, 0.02, 0.03, 0.04), (0.02, 0.03, 0.04, 0.05)], name='roi_table'),
            # 指标阈值
            Integer(10, 50, name='rsi_buy'),
            Integer(10, 50, name='rsi_sell'),
            Integer(-200, 200, name='cci_buy'),
            Integer(-200, 200, name='cci_sell'),
            # FreqAI参数
            Integer(60, 180, 10, name='train_period_days'),
            Integer(10, 40, 5, name='backtest_period_days'),
            Categorical(['1h', '2h', '4h'], name='include_timeframes'),
            Categorical([10, 20], name='indicator_periods_candles'),
            Integer(6, 16, 2, name='label_period_candles'),
            Integer(3, 12, 3, name='include_shifted_candidates'),
            Real(1e-5, 1e-3, name='learning_rate', log=True),
            Integer(2, 6, name='n_layer'),
            Integer(2, 8, name='n_head'),
            Integer(32, 256, name='hidden_dim'),
        ]

    @staticmethod
    def sell_space():
        return []

    @staticmethod
    def trailing_space():
        return []

    @staticmethod
    def generate_roi_table(params):
        # 可根据 params 生成动态 ROI table
        return {
            0: 0.04,
            30: 0.03,
            60: 0.02,
            120: 0.01
        }

    @staticmethod
    def stoploss_space():
        return []

    @staticmethod
    def buy_space():
        return []

    @staticmethod
    def protections_space():
        return []

    @staticmethod
    def custom_hyperopt_loss():
        return None
