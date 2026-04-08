综合前述对回测报告的诊断、FreqAI 的回归能力以及 High/Low 预测逻辑，我为你构建了一个**“三位一体”的量化交易方案**。该方案将预测分为三个维度：**入场空间预测、动态止盈设定、以及基于风险的智能出场**。

以下是基于 `FreqaiExampleHybridStrategy.py` 框架的深度修改方案：

---

### 1. 目标设定：多维度回归预测 (Targets)
我们不再预测涨跌，而是预测未来 40 根 K 线内的**潜在空间**和**风险垫**。

```python
def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
    # 1. 预测高峰（潜在最大利润空间）
    dataframe["&-max_upside"] = (
        dataframe["high"].rolling(window=40).max().shift(-40) / dataframe["close"] - 1
    )
    # 2. 预测低谷（潜在最大回撤空间/风险垫）
    dataframe["&-max_downside"] = (
        dataframe["low"].rolling(window=40).min().shift(-40) / dataframe["close"] - 1
    )
    # 3. 预测波动率（用于设定动态追踪止损的间距）
    dataframe["&-atr_pred"] = (
        (dataframe["high"].rolling(20).max() - dataframe["low"].rolling(20).min()) / dataframe["close"]
    ).shift(-20)

    return dataframe
```

---

### 2. 入场逻辑：盈亏比驱动 (Entry)
只有当模型预测的“向上空间”远大于“向下回撤”时才入场。这能有效解决你之前回测中出现的“赚小钱赔大钱”问题。

```python
def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
    # 动态阈值：要求预测涨幅 > 2.5%，且预测盈亏比 > 2.0
    min_profit_space = 0.025 
    rr_ratio = 2.0

    df.loc[
        (
            (df["do_predict"] == 1) &
            (df["&-max_upside"] > min_profit_space) & 
            (df["&-max_upside"] / df["&-max_downside"].abs() > rr_ratio) &
            # 基础过滤：RSI不在超买区且趋势向上
            (df["rsi"] < 60) &
            (df["tema"] > df["tema"].shift(1))
        ),
        "enter_long",
    ] = 1

    # 做空逻辑同理反向
    df.loc[
        (
            (df["do_predict"] == 1) &
            (df["&-max_downside"].abs() > min_profit_space) &
            (df["&-max_downside"].abs() / df["&-max_upside"] > rr_ratio) &
            (df["rsi"] > 40) &
            (df["tema"] < df["tema"].shift(1))
        ),
        "enter_short",
    ] = 1
    return df
```

---

### 3. 出场与跟踪：动态追踪止损 (Exit & Trailing)
为了获取最大利润，我们放弃固定 ROI，改为**由 ML 预测值驱动的追踪止损**。

#### A. 初始保护：MAE 预测止损
利用预测的 `&-max_downside` 来设定初始止损。如果模型预测这波行情正常回撤是 1.5%，你可以将止损设在 2%，给行情留出呼吸空间。

#### B. 趋势跟踪：动态 Trail
在 Freqtrade 配置文件或策略类中设置：
```python
# 启用动态追踪止损
trailing_stop = True
trailing_stop_positive = 0.01  # 盈利 1% 后开启
trailing_stop_positive_offset = 0.02  # 始终保持 2% 的回调距离
trailing_only_offset_is_reached = True
```

**进阶技巧：在代码中根据预测波动率修改追踪间距**
```python
def confirm_trade_exit(self, pair, trade, order_type, amount, rate, time_in_force, sell_reason, **kwargs):
    # 如果模型预测未来波动率 (&-atr_pred) 变大，可以调宽追踪距离防止被震出
    # 如果预测波动率变小，则收紧追踪距离锁定利润
    pass
```

---

### 4. 方案综合评价

| 维度 | 旧方案 (ichiV1) | 新方案 (ML-HighLow) |
| :--- | :--- | :--- |
| **入场依据** | 指标交叉（滞后） | 空间预测（领先） |
| **止损方式** | 固定硬止损 (-20%) | 基于 `max_downside` 的动态止损 |
| **盈利捕捉** | 触碰 ROI 离场 | 追踪止损随趋势上移，捕捉大波段 |
| **风险控制** | 胜率高但单笔亏损大 | 强制盈亏比过滤，优化 Profit Factor |



### 核心建议：
1.  **特征工程 (Features)**：必须包含 `BB_width` 和 `Volume_ROC`。日内合约交易中，波动率的收缩往往是入场的最佳时机。
2.  **模型选择**：使用 `CatboostRegressor`。由于需要预测具体的百分比数值，回归模型的表现会比分类模型更细腻。
3.  **时间窗口**：建议使用 `5m` 或 `15m` 周期，并在特征中加入 `1h` 的趋势预测。

这种架构下，你的策略不再是盲目地“赌”涨跌，而是在寻找**“风险极低且上方空间巨大”**的概率非对称机会。