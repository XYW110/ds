[Root Directory](./CLAUDE.md) > **技术指标增强版**

## 模块职责

**技术指标增强版** - 项目的第三个版本（`deepseek_ok_带指标plus版本.py`），在 OKX 基础上添加完整的技术指标分析系统，包括移动平均线、MACD、RSI、布林带等，提供更准确的市场趋势判断。

## 入口与启动

### 主函数入口
```python
if __name__ == "__main__":
    main()
```

### 启动流程
1. **初始化阶段**: 与 OKX基础版相同
2. **数据加载**: 获取96根K线数据 (24小时)
3. **技术指标计算**:
   - SMA/EMA 移动平均线
   - MACD 指标
   - RSI 强弱指数
   - 布林带
4. **定时执行**: 每15分钟整点执行

## 外部接口

### 核心 API 集成
与 OKX基础版相同，额外集成完整技术分析模块

### 主要方法

#### 1. `calculate_technical_indicators()` - 技术指标计算
```python
def calculate_technical_indicators(df):
    # 移动平均线
    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_20'] = df['close'].rolling(window=20).mean()
    df['sma_50'] = df['close'].rolling(window=50).mean()

    # 指数移动平均线
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()
    df['macd'] = df['ema_12'] - df['ema_26']
    df['macd_signal'] = df['macd'].ewm(span=9).mean()
    df['macd_histogram'] = df['macd'] - df['macd_signal']

    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # 布林带
    df['bb_middle'] = df['close'].rolling(20).mean()
    bb_std = df['close'].rolling(20).std()
    df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
    df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
    df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])

    # 成交量分析
    df['volume_ma'] = df['volume'].rolling(20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma']

    # 支撑阻力
    df['resistance'] = df['high'].rolling(20).max()
    df['support'] = df['low'].rolling(20).min()
```

#### 2. `get_support_resistance_levels()` - 支撑阻力位
- **静态支撑阻力**: 最近20周期的高低点
- **动态支撑阻力**: 布林带上下轨
- **价格相对位置**: 距离支撑阻力的百分比

#### 3. `get_market_trend()` - 趋势判断
- **短期趋势**: 价格 vs 20周期均线
- **中期趋势**: 价格 vs 50周期均线
- **MACD 趋势**: MACD vs 信号线
- **综合判断**: 强势上涨 / 强势下跌 / 震荡整理

#### 4. `get_btc_ohlcv_enhanced()` - 增强数据获取
- **功能**: 获取K线 + 计算技术指标 + 趋势分析
- **数据量**: 96根K线 (24小时)
- **返回**:
  ```python
  {
      'price': float,
      'timestamp': str,
      'high': float,
      'low': float,
      'volume': float,
      'timeframe': str,
      'price_change': float,
      'kline_data': list,          # 最近10根K线
      'technical_data': {           # 技术指标
          'sma_5': float,
          'sma_20': float,
          'sma_50': float,
          'rsi': float,
          'macd': float,
          'macd_signal': float,
          'macd_histogram': float,
          'bb_upper': float,
          'bb_lower': float,
          'bb_position': float,
          'volume_ratio': float
      },
      'trend_analysis': {            # 趋势分析
          'short_term': str,
          'medium_term': str,
          'macd': str,
          'overall': str,
          'rsi_level': float
      },
      'levels_analysis': {           # 支撑阻力分析
          'static_resistance': float,
          'static_support': float,
          'dynamic_resistance': float,
          'dynamic_support': float,
          'price_vs_resistance': float,
          'price_vs_support': float
      }
  }
  ```

#### 5. `generate_technical_analysis_text()` - 分析文本生成
- **功能**: 将技术指标转换为可读的文本描述
- **包含**:
  - 移动平均线位置和偏离度
  - RSI 状态 (超买/超卖/中性)
  - MACD 方向和强度
  - 布林带位置
  - 关键支撑阻力位

## 关键依赖

### Python 依赖包
与 OKX基础版相同，额外使用:
```
pandas==2.x  # 数据处理增强，大量指标计算
```

### 技术分析数据源
- **OKX K线数据**: 96根15分钟K线 (24小时历史)
- **DeepSeek AI**: 综合技术分析生成信号

## 数据模型

### 交易配置 (TRADE_CONFIG)
```python
{
    'symbol': 'BTC/USDT:USDT',
    'amount': 0.01,
    'leverage': 10,
    'timeframe': '15m',
    'test_mode': False,
    'data_points': 96,              # 新增：24小时数据
    'analysis_periods': {           # 新增：分析周期
        'short_term': 20,
        'medium_term': 50,
        'long_term': 96
    }
}
```

### 技术指标数据
```python
{
    'sma_5': float,                 # 5周期简单均线
    'sma_20': float,                # 20周期简单均线
    'sma_50': float,                # 50周期简单均线
    'ema_12': float,                # 12周期指数均线
    'ema_26': float,                # 26周期指数均线
    'macd': float,                  # MACD值
    'macd_signal': float,           # MACD信号线
    'macd_histogram': float,        # MACD柱状图
    'rsi': float,                   # 相对强弱指数
    'bb_upper': float,              # 布林带上轨
    'bb_middle': float,             # 布林带中轨
    'bb_lower': float,              # 布林带下轨
    'bb_position': float,           # 布林带位置(0-1)
    'volume_ratio': float           # 成交量比率
}
```

## 测试与质量保障

### 技术指标验证
- ✅ 移动平均线正确性检查
- ✅ RSI 计算准确性 (0-100 范围)
- ✅ MACD 金叉死叉判断
- ✅ 布林带上下轨有效性
- ✅ 支撑阻力位合理性

### 增强数据处理
- ✅ NaN 值填充 (bfill/ffill)
- ✅ 数据平滑处理
- ✅ 边界条件处理
- ✅ 计算精度控制

### 错误处理
- **技术指标计算失败**: 使用上次有效值或默认值
- **数据不足**: 逐步减少计算窗口
- **异常值**: 过滤极值并平滑处理

## 常见问题 (FAQ)

### Q: 为什么需要96根K线数据？
A: 为了计算50周期均线和长期趋势分析，需要足够的历史数据。96根 = 24小时 (15分钟 × 4 × 24)。

### Q: 技术指标冲突怎么办？
A: DeepSeek AI 会综合所有指标进行分析，权重分配:
- 趋势(均线排列) > RSI > MACD > 布林带

### Q: 如何解读布林带位置？
A: `bb_position` 值:
- 0.8-1.0: 价格接近上轨，可能超买
- 0.2-0.0: 价格接近下轨，可能超卖
- 0.3-0.7: 正常波动区间

### Q: 成交量比率有什么作用？
A: `volume_ratio > 1.5` 表示成交量放大，是趋势确认的重要信号。

### Q: MACD 柱状图代表什么？
A: `macd_histogram > 0` 表示多头力量，< 0 表示空头力量，绝对值越大趋势越强。

## 与前版本对比

| 特性 | OKX基础版 | 技术指标增强版 |
|------|----------|----------------|
| 数据量 | 10根K线 | 96根K线 (24小时) |
| 基础分析 | 5周期SMA | 完整技术指标库 |
| 趋势判断 | 简单价格对比 | 多周期趋势分析 |
| 市场结构 | 无 | 支撑阻力位分析 |
| 动量指标 | 无 | RSI, MACD, 布林带 |
| 成交量分析 | 无 | 成交量比率 |

## 相关文件

| 文件 | 用途 |
|------|------|
| `deepseek_ok版本.py` | OKX基础版 (v2.0) |
| `deepseek_ok_带市场情绪+指标版本.py` | 完整版策略 (v4.0) |
| `deepseek.py` | 基础版策略 (v1.0) |

## 变更日志 (Changelog)

### v3.0 - 2025-11-05
- ✨ 添加完整技术指标分析系统
- ✅ 移动平均线系统 (SMA, EMA)
- ✅ MACD 指标 (12, 26, 9)
- ✅ RSI 强弱指数 (14周期)
- ✅ 布林带系统 (20周期, 2倍标准差)
- ✅ 成交量分析 (20周期均线)
- ✅ 支撑阻力位计算
- ✅ 多时间框架趋势判断
- ✅ 24小时历史数据分析
- ✅ 技术分析文本生成

---

**模块类型**: 技术分析引擎
**更新时间**: 2025-11-05 11:26:39
