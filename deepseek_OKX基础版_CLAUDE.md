[Root Directory](./CLAUDE.md) > **OKX基础版**

## 模块职责

**OKX 交易所基础适配版** - 项目的第二个版本（`deepseek_ok版本.py`），从 Binance 迁移到 OKX 交易所，适配永续合约交易接口，使用全仓模式和单向持仓。

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
   - 配置 OKX 永续合约接口
   - 设置交易参数 (`TRADE_CONFIG`)

2. **交易所设置**:
   - 设置全仓模式和杠杆倍数 (10x)
   - 获取账户余额
   - 验证合约规格信息

3. **调度启动**:
   - 每15分钟执行一次策略
   - 立即执行一次策略
   - 进入主循环等待

## 外部接口

### 核心 API 集成

#### DeepSeek AI 分析接口
```python
# API配置 (与基础版相同)
deepseek_client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)
```

#### OKX 永续合约接口
```python
exchange = ccxt.okx({
    'options': {
        'defaultType': 'swap',  # 永续合约
    },
    'apiKey': os.getenv('OKX_API_KEY'),
    'secret': os.getenv('OKX_SECRET'),
    'password': os.getenv('OKX_PASSWORD'),  # OKX需要交易密码
})
```

### 主要方法

#### 1. `setup_exchange()` - 交易所初始化
- **功能**: 设置 OKX 交易参数
- **特殊处理**:
  - 全仓模式设置 (`mgnMode: cross`)
  - 杠杆倍数配置 (10x)
  - 账户余额获取

#### 2. `get_btc_ohlcv()` - 数据获取
- **功能**: 获取 BTC/USDT 永续合约 K线数据
- **特点**: 与基础版相同，但使用 OKX 数据源

#### 3. `analyze_with_deepseek()` - AI分析
- **功能**: 使用 DeepSeek 分析市场数据
- **提示词**: 与基础版相同，专业交易员角色设定

#### 4. `execute_trade()` - 订单执行
- **功能**: 执行 OKX 永续合约交易
- **OKX 特性**:
  - 使用 `tag` 参数标识订单来源
  - 双向持仓模式
  - reduceOnly 参数平仓

## 关键依赖

### Python 依赖包
与基础版相同，额外依赖:
```
ccxt==4.x  # 支持OKX交易所
```

### 外部服务
- **DeepSeek API**: 市场分析和信号生成
- **OKX 永续合约**: 交易执行和账户管理

### 环境变量 (.env)
```bash
DEEPSEEK_API_KEY=your_deepseek_key
OKX_API_KEY=your_okx_key
OKX_SECRET=your_okx_secret
OKX_PASSWORD=your_okx_password
```

## 数据模型

### 交易配置 (TRADE_CONFIG)
```python
{
    'symbol': 'BTC/USDT:USDT',  # OKX合约符号格式
    'amount': 0.01,             # 交易数量 (BTC)
    'leverage': 10,             # 杠杆倍数
    'timeframe': '15m',         # K线周期
    'test_mode': False          # 测试模式
}
```

### 持仓数据结构
与基础版相同，但字段来源于 OKX:
```python
{
    'side': str,                # long/short
    'size': float,              # 持仓数量(合约张数)
    'entry_price': float,       # 入场价格
    'unrealized_pnl': float,    # 未实现盈亏
    'leverage': float,          # 杠杆倍数
    'symbol': str               # 交易对符号
}
```

## 测试与质量保障

### 测试模式
与基础版相同，`test_mode: True` 启用模拟交易

### OKX 特有错误处理
- **合约规格错误**: 检查合约乘数和最小交易量
- **余额不足**: 验证保证金充足性
- **权限错误**: 确认 API 权限和交易密码

### 数据验证
- ✅ OKX 合约符号格式验证
- ✅ 持仓模式检查 (双向持仓)
- ✅ 杠杆设置有效性
- ✅ 订单参数完整性

## 常见问题 (FAQ)

### Q: OKX 和 Binance 有什么区别？
A:
- 符号格式: OKX 使用 `BTC/USDT:USDT`，Binance 使用 `BTC/USDT`
- 交易密码: OKX 需要额外的 `password` 参数
- 合约类型: OKX 使用 `swap` 表示永续��约
- 订单参数: OKX 支持 `tag` 参数

### Q: 如何设置杠杆倍数？
A: 在 `TRADE_CONFIG['leverage']` 中设置，默认为 10x，支持 1-50x

### Q: 全仓和逐仓有什么区别？
A:
- 全仓 (cross): 所有可用余额作为保证金，风险更高
- 逐仓 (isolated): 单独计算每笔订单保证金
- 本策略强制使用全仓模式

### Q: 为什么需要交易密码？
A: OKX 要求交易操作必须提供交易密码（不是登录密码），用于安全验证

## 与基础版对比

| 特性 | 基础版 (Binance) | OKX基础版 |
|------|------------------|----------|
| 交易所 | Binance 期货 | OKX 永续合约 |
| 符号格式 | BTC/USDT | BTC/USDT:USDT |
| 额外认证 | 无 | 需要 password |
| 杠杆设置 | 标准设置 | 需要指定 mgnMode |
| 订单标识 | 标准订单 | 支持 tag 参数 |
| 持仓模式 | 双向持仓 | 双向持仓 |

## 相关文件

| 文件 | 用途 |
|------|------|
| `deepseek.py` | 基础版策略 (v1.0) |
| `deepseek_ok_带指标plus版本.py` | 技术指标增强版 (v3.0) |
| `deepseek_ok_带市场情绪+指标版本.py` | 完整版策略 (v4.0) |
| `requirements.txt` | Python 依赖列表 |

## 变更日志 (Changelog)

### v2.0 - 2025-11-05
- ✨ 迁移到 OKX 交易所
- ✅ 适配 OKX 永续合约接口
- ✅ 全仓模式设置
- ✅ 合约规格处理
- ✅ 双向持仓支持
- ✅ 交易密码集成
- ✅ tag 订单标识

---

**模块类型**: 交易所适配层
**更新时间**: 2025-11-05 11:26:39
