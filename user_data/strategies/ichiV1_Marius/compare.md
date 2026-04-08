我先快速抓两份策略的关键段落（参数、进出场、持仓管理），然后给你一份并排对比和适用场景建议。

Read [](file:///home/watson/work/freqtrd/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py#150-150), lines 150 to 260

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1/ichiV1.py#1-1), lines 1 to 140

Read [](file:///home/watson/work/freqtrd/user_data/strategies/ichiV1/ichiV1.py#140-140), lines 140 to 237

我再补读 Marius 的进出场和多周期数据部分，这样能把“复杂度差异”和“实盘风控差异”说清楚。

Read [](file:///home/watson/work/freqtrd/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py#260-260), lines 260 to 430

Read [](file:///home/watson/work/freqtrd/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py#430-430), lines 430 to 620

我会再抓几个精确行号（DCA、止损、买卖开关、疑似拼写问题），这样对比会更直观。

Searched for regex `position_adjustment_enable|max_dca_orders|def adjust_trade_position|custom_stake_amount|use_custom_stoploss|use_sell_signal|ignore_roi_if_buy_signal|buy_tag == 'telsa_'|buy_tag']` (`**/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py`), no results

Searched for regex `INTERFACE_VERSION|minimal_roi|stoploss|startup_candle_count|process_only_new_candles|use_exit_signal|ignore_roi_if_entry_signal|populate_buy_trend|populate_sell_trend` (`**/user_data/strategies/ichiV1/ichiV1.py`), 13 results

Searched for regex `buy_min_fan_magnitude_gain\s*=\s*DecimalParameter\(|def custom_stoploss|def confirm_trade_exit|def informative_pairs` (`**/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py`), 4 results

Searched for regex `position_adjustment_enable|max_dca_orders|def adjust_trade_position|def custom_stake_amount|use_custom_stoploss|use_sell_signal|ignore_roi_if_buy_signal|buy_tag == 'telsa_'|buy_tag\]` (`**/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py`), 10 results

Searched for regex `minimal_roi|stoploss =|startup_candle_count|process_only_new_candles|informative_timeframe|inf_15m|def confirm_trade_entry|def custom_sell` (`**/user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py`), 17 results

这两个都属于 Ichimoku 趋势系，但定位差很多:  
ichiV1 是轻量基础版，ichiV1_Marius 是重度实盘增强版（带 DCA、多层风控、更多数据源）。

1. 核心差异
1. 复杂度
1. ichiV1: 主要是 Ichimoku + 多周期 EMA 趋势判断，逻辑直白，ichiV1.py 和 ichiV1.py 很干净。
2. ichiV1_Marius: 在同类趋势骨架上叠加 BTC 过滤、15m 抽水检测、滑点保护、DCA、自定义止损/离场，复杂很多，ichiV1_Marius.py 到 ichiV1_Marius.py 一整套增强。

2. 持仓管理
1. ichiV1: 没有 DCA/加仓机制。
2. ichiV1_Marius: 明确启用 DCA，ichiV1_Marius.py, ichiV1_Marius.py, ichiV1_Marius.py, 还有配套资金分配 ichiV1_Marius.py。

3. 风控与出场
1. ichiV1: 主要靠固定 ROI/止损，ichiV1.py, ichiV1.py。
2. ichiV1_Marius: 增加了自定义止损与离场拦截，ichiV1_Marius.py, ichiV1_Marius.py, ichiV1_Marius.py, 还有超时解套 ichiV1_Marius.py。

4. 数据与启动成本
1. ichiV1: startup 较小，[startup_candle_count = 96](user_data/strategies/ichiV1/ichiV1.py#L50)。
2. ichiV1_Marius: startup 更大，[startup_candle_count = 499](user_data/freqtrade-strategies/strategies/ichiV1_Marius/ichiV1_Marius.py#L269)，并且依赖 1h/15m/BTC 多数据流，ichiV1_Marius.py, ichiV1_Marius.py。

2. 兼容性与代码风险（重点）
1. ichiV1 明确是 V3 接口，[INTERFACE_VERSION = 3](user_data/strategies/ichiV1/ichiV1.py#L18)，并提供了 ichiV1.py/ichiV1.py。
2. ichiV1_Marius 存在一个可疑拼写：买入打的是 tesla_，但判断里有 telsa_，见 ichiV1_Marius.py 和 ichiV1_Marius.py。
3. ichiV1_Marius 还有一个明显可疑参数区间：buy_min_fan_magnitude_gain 的范围写成 70~90，但默认值是 1.0022，见 ichiV1_Marius.py。

3. 选型建议
1. 想先稳定理解策略逻辑、快速跑回测: 选 ichiV1。
2. 想研究 DCA + 风控工程化 + 多周期过滤: 选 ichiV1_Marius，但建议先修上面两个可疑点再实盘/长测。
