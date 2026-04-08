
好的，我现在为你做一份**从K线进入到信号输出的完整数据流讲解**。

---

## 📊 **一根K线的完整生命周期（数据流追踪）**

### **阶段 0：K线到达前的初始化**
```
配置中的 indicator_periods_candles: [10, 20]
      ↓
策略会为这两个周期都执行 feature_engineering_expand_all()
```

---

### **阶段 1：特征工程第一层（expand_all）**
**触发时机**：每根K线来临时

| 函数 | 代码行 | 输出列，说明 |
|------|-------|-----------|
| `feature_engineering_expand_all()` | FreqaiExampleHybridStrategy.py | 为该K线逐个计算 RSI、MFI、ADX、SMA、EMA（10周期、20周期分别计算一遍）|
| | FreqaiExampleHybridStrategy.py | 计算布林带，导出 bb_width、close/bb_lower 比值 |
| | FreqaiExampleHybridStrategy.py | ROC、相对成交量 |
| **输出样例** | | 列如：%-rsi-period-10、%-ema-period-20、%-bb_width-period-10 |

💡 **关键点**：每列名前缀是 `%`，这样 FreqAI 才认（见 FreqaiExampleHybridStrategy.py）。

---

### **阶段 2：特征工程第二层（expand_basic）**
**触发时机**：同K线，但特征不再按 indicator_periods 重复

| 函数 | 代码行 | 输出列 |
|------|-------|-------|
| `feature_engineering_expand_basic()` | FreqaiExampleHybridStrategy.py | 添加 %-pct-change、%-raw_volume、%-raw_price |
| **作用** | | 这三列会按 include_timeframes 和 include_shifted_candles 扩展，但 **不** 会再按周期扩展 |

---

### **阶段 3：特征工程第三层（standard）**
**触发时机**：所有其他特征都准备好后，最后一步

| 函数 | 代码行 | 输出列 |
|------|-------|-------|
| `feature_engineering_standard()` | FreqaiExampleHybridStrategy.py | %-day_of_week（0-6）、%-hour_of_day（0-23）|
| **作用** | | 从 dataframe["date"] 提取，**不自动扩展**多客对或时间框架 |

**此时 dataframe 包含的列**：
```
所有特征列（%-开头）
    ↓
+ 目标列占位（暂为空，待补充）
```

---

### **阶段 4：设置监督目标（set_freqai_targets）**
**触发时机**：特征工程完成后

| 函数 | 代码行 | 核心逻辑 |
|------|-------|---------|
| `set_freqai_targets()` | FreqaiExampleHybridStrategy.py | 定义类别名：["down", "up"] |
| | FreqaiExampleHybridStrategy.py | **关键标签公式**：如果 close.shift(-50) > close，标签="up"，否则="down" |
| | 重点 | **shift(-50) 表示向未来看50根K线** |

**含义浅析**：
- 当前K线索引为 i
- 查看 i+50 根K线的收盘价与 i 根的比较
- 用于训练"预测50根K线后的方向"模型

**此时 dataframe 新增列**：
```
&s-up_or_down  (值为 "up" 或 "down")
```

---

### **阶段 5：FreqAI 处理（训练/推理入口）**
**触发时机**：populate_indicators() 被 freqtrade 核心调用时

| 函数 | 代码行 | 动作 |
|------|-------|------|
| `populate_indicators()` | FreqaiExampleHybridStrategy.py | **关键行**：`self.freqai.start(dataframe, metadata, self)` |
| | | FreqAI 内部流程：<br/> ① 数据准备（应用所有特征工程）<br/> ② 数据分割（train/test）<br/> ③ 模型训练或推理<br/> ④ 回填 `do_predict` 和 `prediction` 列 |

**此时 dataframe 新增列**：
```
do_predict         (0/1，模型置信度过滤：1=有效预测，0=无效)
prediction         (不在这份代码中显式使用，但内部存在)
```

---

### **阶段 6：传统指标补充（规则入场前的最后准备）**
**触发时机**：同 populate_indicators，但在 self.freqai.start() 之后

| 指标 | 代码行 | 说明 |
|------|-------|------|
| RSI | FreqaiExampleHybridStrategy.py | 基础 RSI(14)，用于规则信号触发 |
| 布林带 | FreqaiExampleHybridStrategy.py | BB(20, 2)，三线 + bb_percent + bb_width |
| TEMA | FreqaiExampleHybridStrategy.py | Triple EMA(9)，平滑的价格跟踪 |

**此时 dataframe 的形象**：
```
特征列（%-开头）  ← FreqAI 特征
目标列（&-开头）  ← 标签（历史数据中有值）
do_predict        ← 模型置信度（当前/近期K线有值）
rsi, bb_*, tema   ← 传统指标（每根K线都有）
```

---

### **阶段 7：入场决策（populate_entry_trend）**
**触发时机**：populate_entry_trend() 在 populate_indicators() 后被调用

#### **做多判断逻辑**（FreqaiExampleHybridStrategy.py）

```
条件 1: RSI 上穿阈值               ← crossed_above(df["rsi"], buy_rsi.value)
条件 2: TEMA 位置低                ← df["tema"] <= df["bb_middleband"]
条件 3: TEMA 动量正                ← df["tema"] > df["tema"].shift(1)
条件 4: 确认有成交                 ← df["volume"] > 0
条件 5: 🔴 模型置信度过             ← df["do_predict"] == 1
条件 6: 🔴 模型方向许可             ← df["&s-up_or_down"] == "up"

所有条件 AND → entry_long = 1
```

**模型角色**：条件 5 是"质量阀门"，条件 6 是"方向确认"。

#### **做空判断逻辑**（FreqaiExampleHybridStrategy.py）

```
条件 1: RSI 上穿高位                ← crossed_above(df["rsi"], short_rsi.value)  [默认70]
条件 2: TEMA 位置高                ← df["tema"] > df["bb_middleband"]
条件 3: TEMA 动量负                ← df["tema"] < df["tema"].shift(1)
条件 4: 确认有成交                 ← df["volume"] > 0
条件 5: 🔴 模型置信度过             ← df["do_predict"] == 1
条件 6: 🔴 模型方向许可             ← df["&s-up_or_down"] == "down"

所有条件 AND → enter_short = 1
```

---

### **阶段 8：出场决策（populate_exit_trend）**
**触发时机**：populate_exit_trend() 同样被调用

#### **多单出场**（FreqaiExampleHybridStrategy.py）

```
条件 1: RSI 上穿出场线              ← crossed_above(df["rsi"], sell_rsi.value)  [默认70]
条件 2: TEMA 走弱                   ← df["tema"] > df["bb_middleband"] AND df["tema"] < df["tema"].shift(1)
条件 3: 有成交量                    ← df["volume"] > 0

→ exit_long = 1
```

**注意**：**没有** do_predict 检查，强调"宁可早离，不等模型"。

#### **空单出场**（FreqaiExampleHybridStrategy.py）

```
条件 1: RSI 上穿低位                ← crossed_above(df["rsi"], exit_short_rsi.value)  [默认30]
条件 2: TEMA 走强                   ← df["tema"] <= df["bb_middleband"] AND df["tema"] > df["tema"].shift(1)
条件 3: 有成交量                    ← df["volume"] > 0

→ exit_short = 1
```

---

## 🎯 **关键时间线总结**

| 时序 | 操作 | 输出 | 用途 |
|------|------|------|------|
| T0 | expand_all | %-rsi-*、%-mfi-* 等 | 给 FreqAI 用 |
| T1 | expand_basic | %-pct-change 等 | 给 FreqAI 用|
| T2 | standard | %-day_of_week 等 | 给 FreqAI 用 |
| T3 | set_targets | &s-up_or_down | 标签（历史训练） |
| **T4** | **freqai.start()** | **do_predict** | **模型输出** ← 🔑 关键 |
| T5 | 传统指标 | rsi, bb_*, tema | 规则触发 |
| T6 | populate_entry | entry_long / enter_short | 下单决策 |
| T7 | populate_exit | exit_long / exit_short | 平仓决策 |

---

## 💡 **三个最常见的改造点**

1. **换标签窗口**：shift(-50) 改成 shift(-20)  
   → 学习短期涨跌而非趋势

2. **加特征**：在 expand_all 里加 CCI、STOCH 等  
   → 模型获得更多信息，但也更容易过拟合

3. **改出场规则**：在 populate_exit_trend 里加 do_predict 和模型方向  
   → 让出场也听模型，风险更高但可能更平滑

---

这就是一根K线从进入到变成一个交易信号的完整旅程。你现在可以指着这份图遮挡代码，能讲出来吗？😄