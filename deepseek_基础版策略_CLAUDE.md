[Root Directory](./CLAUDE.md) > **基础版策略**

## 模块职责

**基础版 DeepSeek 交易策略** - 项目的第一个版本（`deepseek.py`），提供了完整的交易机器人基础框架，集成了 DeepSeek AI 分析和 Binance 交易所接口。

## 入口与启动

### 主函数入口
```python
if __name__ == "__main__":
    main()
```

### 启动流程
1. **初始化阶段**:
   - 加载 `.env` 环境变量
   - 初始化 DeepSeek API 客户端
   - 配置 Binance 期货接口
   - 设置交易参数 (`TRADE_CONFIG`)

2. **交易所设置**:
   - 设置杠杆倍数 (默认10x)
   - 获取账户余额
   - 验证连接状态

3. **调度启动**:
   - 根据时间周期配置执行频率
     - `1h` 周期: 每小时执行一次
     - `15m` 周期: 每15分钟执行一次
   - 立即执行一次策略
   - 进入主循环等待

## 外部接口

### 核心 API 集成

#### DeepSeek AI 分析接口
```python
# API配置
deepseek_client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

# 分析模型
model="deepseek-chat"
temperature=0.1
```

#### Binance 期货接口
```python
exchange = ccxt.binance({
    'options': {'defaultType': 'future'},
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_SECRET'),
})
```

### 主要方法

#### 1. `get_btc_ohlcv()` - 数据获取
- **功能**: 获取 BTC/USDT K线数据
- **参数**:
  - 时间周期: `15m` 或 `1h` (可配置)
  - 数据量: 最近10根K线
- **返回**: 价格、时间、高低、成交量、变化百分比

#### 2. `analyze_with_deepseek()` - AI分析
- **功能**: 使用 DeepSeek 分析市场数据
- **输入**:
  - K线数据 (最近5根)
  - 技术指标 (5周期SMA)
  - 历史信号
  - 当前持仓
- **输出**: JSON格式交易信号
```json
{
    "signal": "BUY|SELL|HOLD",
    "reason": "分析理由",
    "stop_loss": 价格,
    "take_profit": 价格,
    "confidence": "HIGH|MEDIUM|LOW"
}
```

#### 3. `execute_trade()` - 订单执行
- **功能**: 执行交易决策
- **逻辑**:
  - 检查当前持仓
  - 根据信号方向下单
  - 支持开仓/平仓/反向开仓

#### 4. `get_current_position()` - 持仓查询
- **功能**: 获取当前持仓状态
- **返回**:
  - 持仓方向 (long/short)
  - 持仓数量
  - 入场价格
  - 未实现盈亏

## 关键依赖

### Python 依赖包
```
ccxt==4.x          # 交易所接口
openai==1.x        # DeepSeek API
pandas==2.x        # 数据处理
schedule==1.x      # 任务调度
python-dotenv==1.x # 环境变量
```

### 外部服务
- **DeepSeek API**: 市场分析和信号生成
- **Binance 期货**: 交易执行和账户管理

### 环境变量 (.env)
```bash
DEEPSEEK_API_KEY=your_deepseek_key
BINANCE_API_KEY=your_binance_key
BINANCE_SECRET=your_binance_secret
```

## 数据模型

### 交易配置 (TRADE_CONFIG)
```python
{
    'symbol': 'BTC/USDT',       # 交易对
    'amount': 0.001,            # 交易数量 (BTC)
    'leverage': 10,             # 杠杆倍数
    'timeframe': '15m',         # K线周期
    'test_mode': False          # 测试模式
}
```

### 价格数据结构
```python
{
    'price': float,             # 当前价格
    'timestamp': str,           # 时间戳
    'high': float,              # 最高价
    'low': float,               # 最低价
    'volume': float,            # 成交量
    'timeframe': str,           # 时间周期
    'price_change': float,      # 价格变化百分比
    'kline_data': list          # 最近5根K线数据
}
```

### 持仓数据结构
```python
{
    'side': str,                # long/short
    'size': float,              # 持仓数量
    'entry_price': float,       # 入场价格
    'unrealized_pnl': float,    # 未实现盈亏
    'symbol': str               # 交易对符号
}
```

## 测试与质量保障

### 测试模式
- `test_mode: True` - 仅模拟，不执行真实订单
- **重要**: 首次运行建议启用测试模式

### 错误处理机制
- **API调用失败**: 打印错误信息，继续运行
- **数据获取失败**: 返回 None，跳过本次交易
- **订单执行失败**: 完整异常追踪和回滚

### 数据验证
- ✅ K线数据完整性检查
- ✅ 持仓数据有效性验证
- ✅ API响应格式检查
- ✅ JSON 解析安全处理

### 日志输出
- 执行时间戳
- 当前价格和变化
- AI分析信号详情
- 订单执行状态
- 持仓变化跟踪

## 常见问题 (FAQ)

### Q: 如何切换到测试网？
A: 在 `TRADE_CONFIG` 中设置 `test_mode: True`，程序将只模拟交易不执行真实订单。

### Q: 如何调整交易频率？
A: 修改 `TRADE_CONFIG['timeframe']`:
- `'1h'` - 每小时执行一次
- `'15m'` - 每15分钟执行一次

### Q: 如何修改交易数量？
A: 在 `TRADE_CONFIG` 中调整 `'amount'` 值，默认为 0.001 BTC。

### Q: DeepSeek 分析失败怎么办？
A: 程序会打印错误信息并跳过本次交易，下次周期继续尝试。

### Q: 如何查看交易历史？
A: 程序会打印每次交易的详细信息，包括信号、理由和执行结果。

## 相关文件

| 文件 | 用途 |
|------|------|
| `deepseek_ok版本.py` | OKX交易所版本 (v2.0) |
| `deepseek_ok_带指标plus版本.py` | 技术指标增强版 (v3.0) |
| `deepseek_ok_带市场情绪+指标版本.py` | 完整版策略 (v4.0) |
| `requirements.txt` | Python 依赖列表 |
| `README.md` | 项目说明文档 |

## 变更日志 (Changelog)

### v1.0 - 2025-11-05
- ✨ 初始版本发布
- ✅ 集成 DeepSeek AI 分析
- ✅ 实现 Binance 期货接口
- ✅ 基础交易逻辑 (开仓/平仓/反向)
- ✅ 自动调度系统
- ✅ 持仓跟踪功能

---

**模块类型**: 基础策略框架
**更新时间**: 2025-11-05 11:26:39
