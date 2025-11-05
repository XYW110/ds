[Root Directory](./CLAUDE.md) > **完整策略版**

## 模块职责

**完整策略版** - 项目的第四个也是最终版本（`deepseek_ok_带市场情绪+指标版本.py`），集成了所有前版本的优点，新增市场情绪数据API、智能仓位管理系统、防频繁交易机制等高级功能，提供最完整和可靠的交易解决方案。

## 入口与启动

### 主函数入口
```python
if __name__ == "__main__":
    main()
```

### 启动流程
1. **初始化阶段**: 与技术指标增强版相同
2. **交易所安全检查**:
   - 检测现有持仓模式
   - 禁止逐仓模式，强制全仓
   - 设置单向持仓模式
3. **智能功能启动**:
   - 情绪数据获取模块
   - 智能仓位计算引擎
   - 防频繁交易保护
4. **整点定时执行**: 严格按15分钟整点执行

## 外部接口

### 核心 API 集成

#### DeepSeek AI 分析接口
```python
# 与前版本相同，temperature 设置为 0.1
deepseek_client.chat.completions.create(
    model="deepseek-chat",
    temperature=0.1  # 低随机性
)
```

#### OKX 永续合约接口
与技术指标增强版相同

#### 市场情绪数据 API
```python
API_URL = "https://service.cryptoracle.network/openapi/v2/endpoint"
API_KEY = "7ad48a56-8730-4238-a714-eebc30834e3e"

# 获取情绪指标
endpoints = ["CO-A-02-01", "CO-A-02-02"]
timeType = "15m"
token = ["BTC"]
```

### 主要方法

#### 1. `setup_exchange()` - 交易所安全设置
```python
def setup_exchange():
    # 1. 检查现有持仓模式
    # 2. 如果有逐仓持仓，提示并退出
    # 3. 设置单向持仓模式
    # 4. 设置全仓模式和杠杆
    # 5. 验证账户设置
```

#### 2. `calculate_intelligent_position()` - 智能仓位计算
```python
def calculate_intelligent_position(signal_data, price_data, current_position):
    config = TRADE_CONFIG['position_management']

    # 计算逻辑：
    # 1. 获取账户余额
    # 2. 根据信心程度调整倍数
    # 3. 根据趋势强度调整
    # 4. 根据RSI状态调整
    # 5. 风险管理：不超过总资金指定比例
    # 6. 计算合约张数

    # 公式：合约张数 = (投入USDT) / (当前价格 * 合约乘数)
```

**智能仓位规则**:
- **HIGH信心**: 1.5x 基础仓位
- **MEDIUM信心**: 1.0x 基础仓位
- **LOW信心**: 0.5x 基础仓位
- **强势趋势**: +1.2x 趋势强度倍数
- **超买超卖区域**: -0.7x RSI调整

#### 3. `get_sentiment_indicators()` - 市场情绪数据
```python
def get_sentiment_indicators():
    # 获取最近4小时数据
    # 解析情绪指标:
    #   - CO-A-02-01: 乐观比例
    #   - CO-A-02-02: 悲观比例
    # 计算净值: 乐观 - 悲观

    return {
        'positive_ratio': float,    # 乐观比例 (0-1)
        'negative_ratio': float,    # 悲观比例 (0-1)
        'net_sentiment': float,     # 情绪净值
        'data_time': str,           # 数据时间
        'data_delay_minutes': int   # 数据延迟分钟数
    }
```

#### 4. `execute_intelligent_trade()` - 智能交易执行
```python
def execute_intelligent_trade(signal_data, price_data):
    # 防频繁反转检查
    # 计算智能仓位
    # 执行交易 (支持同方向加仓减仓)
    # 错误恢复机制
```

**交易逻辑优化**:
- 同方向持仓可加仓/减仓
- 反转需要高信心 + 避免近期重复信号
- 完整错误恢复 (直接开仓失败时尝试替代方案)

#### 5. `wait_for_next_period()` - 整点等待
```python
def wait_for_next_period():
    # 计算到下一个15分钟整点的等待时间
    # 整点时间: 00, 15, 30, 45分
    # 返回等待秒数
```

#### 6. `analyze_with_deepseek_with_retry()` - 带重试的AI分析
```python
def analyze_with_deepseek_with_retry(price_data, max_retries=2):
    # 最多重试2次
    # 失败后使用备用信号
    # 备用信号: HOLD + 保守止损止盈
```

## 关键依赖

### Python 依赖包
与技术指标增强版相同，新增:
```
requests==2.x  # 市场情绪API调用
```

### 外部服务
- **DeepSeek API**: 市场分析和信号生成
- **OKX 永续合约**: 交易执行
- **CryptOracle API**: 市场情绪数据
  - 端点: CO-A-02-01 (乐观), CO-A-02-02 (悲观)
  - 更新频率: 15分钟
  - 数据延迟: 通常 < 10分钟

## 数据模型

### 交易配置 (TRADE_CONFIG)
```python
{
    'symbol': 'BTC/USDT:USDT',
    'leverage': 10,
    'timeframe': '15m',
    'test_mode': False,
    'data_points': 96,
    'analysis_periods': {
        'short_term': 20,
        'medium_term': 50,
        'long_term': 96
    },
    # 新增：智能仓位管理
    'position_management': {
        'enable_intelligent_position': True,   # 启用智能仓位
        'base_usdt_amount': 100,               # 基础USDT投入
        'high_confidence_multiplier': 1.5,     # 高信心倍数
        'medium_confidence_multiplier': 1.0,   # 中信心倍数
        'low_confidence_multiplier': 0.5,      # 低信心倍数
        'max_position_ratio': 10,              # 最大仓位比例
        'trend_strength_multiplier': 1.2       # 趋势强度倍数
    }
}
```

### 市场情绪数据
```python
{
    'positive_ratio': float,       # 0-1之间的乐观比例
    'negative_ratio': float,       # 0-1之间的悲观比例
    'net_sentiment': float,        # 净值 = 乐观 - 悲观
    'data_time': str,              # "YYYY-MM-DD HH:MM:SS"
    'data_delay_minutes': int      # 延迟分钟数
}
```

### 智能仓位计算结果
```python
{
    'base_usdt': float,            # 基础USDT投入
    'confidence_multiplier': float, # 信心倍数
    'trend_multiplier': float,     # 趋势倍数
    'rsi_multiplier': float,       # RSI倍数
    'suggested_usdt': float,       # 建议USDT
    'final_usdt': float,           # 最终USDT (考虑风险)
    'contract_size': float,        # 合约张数
    'min_contracts': float         # 最小交易量
}
```

## 测试与质量保障

### 智能功能测试
- ✅ 智能仓位计算准确性
- ✅ 情绪数据有效性验证
- ✅ 防频繁交易机制
- ✅ 整点执行精确度
- ✅ 错误重试和恢复

### 安全机制
- ✅ 强制单向持仓检查
- ✅ 禁止逐仓模式
- ✅ 保证金充足性验证
- ✅ 信心度风险控制

### 数据验证
- ✅ 情绪数据延迟检查
- ✅ API响应格式验证
- ✅ 数值范围合理性
- ✅ JSON 安全解析

## 常见问题 (FAQ)

### Q: 智能仓位如何工作？
A: 根据AI分析的信心程度动态调整仓位:
- 高信心 (HIGH): 1.5倍基础仓位
- 中信心 (MEDIUM): 1.0倍基础仓位
- 低信心 (LOW): 0.5倍基础仓位
- 强势趋势时额外 +1.2倍

### Q: 市场情绪数据如何使用？
A: 情绪数据占分析权重30%:
- 情绪与技术同向 → 增强信号信心
- 情绪与技术背离 → 以技术分析为主
- 情绪数据延迟 → 降低权重

### Q: 如何防止频繁交易？
A: 多层防护机制:
1. 连续3次相同信号时提示
2. 反转需要 HIGH 信心
3. 检查最近信号历史，避免重复
4. 整点执行，减少触发频率

### Q: 整点执行的优势？
A:
- 避免在单根K线中间执行
- 确保数据完整性 (每根K线结束时执行)
- 更容易回测和验证
- 符合专业交易习惯

### Q: 备用信号何时使用？
A: 当以下情况发生:
- DeepSeek API 调用失败
- JSON 解析失败
- 重试2次后仍失败
- 备用信号: HOLD + ��守止损止盈 (±2%)

### Q: 如何处理持仓调整？
A:
- 同方向信号 → 可加仓/减仓 (智能计算差异)
- 反向信号 → 需要HIGH信心 + 历史检查
- HOLD信号 → 不执行任何操作

## 与前版本对比

| 特性 | 技术指标增强版 | 完整策略版 |
|------|----------------|------------|
| 技术指标 | ✅ 完整指标库 | ✅ 完整指标库 |
| 基础仓位 | 固定0.01张 | 智能动态计算 |
| 市场情绪 | ❌ | ✅ CryptOracle API |
| 防频繁交易 | 基础检查 | 多层防护机制 |
| 定时执行 | 每分钟检查 | 严格整点等待 |
| 错误恢复 | 基础异常处理 | 重试+备用信号 |
| 持仓模式 | 双向持仓 | 单向持仓+全仓强制 |
| 交易优化 | 基础订单执行 | 同方向加仓减仓 |

## 相关文件

| 文件 | 用途 |
|------|------|
| `deepseek_ok_带指标plus版本.py` | 技术指标增强版 (v3.0) |
| `deepseek_ok版本.py` | OKX基础版 (v2.0) |
| `deepseek.py` | 基础版策略 (v1.0) |

## 变更日志 (Changelog)

### v4.0 - 2025-11-05
- ✨ 发布完整功能版本
- ✅ 新增市场情绪数据集成 (CryptOracle API)
- ✅ 实现智能仓位管理系统
- ✅ 添加防频繁交易多层防护机制
- ✅ 实现严格整点定时执行 (15分钟周期)
- ✅ 完善错误处理和重试机制
- ✅ 添加备用信号生成 (HOLD + 保守策略)
- ✅ 强制单向持仓 + 全仓模式
- ✅ 同方向持仓智能加仓/减仓
- ✅ 信号连续性检查和提示
- ✅ 逐仓持仓检测和禁止机制
- ✅ 保证金风险控制

- 🔧 **重大改进**:
  - 重构仓位计算算法，支持多因素动态调整
  - 增强错误恢复机制，提高系统稳定性
  - 优化交易执行逻辑，支持精细化仓位管理
  - 完善数据验证，确保市场情绪数据质量

- 📊 **新增功能**:
  - 情绪净值计算 (乐观-悲观)
  - 趋势强度倍数调整
  - RSI超买超卖区域减仓
  - 整点等待和友好提示
  - 持仓模式强制检查

---

**模块类型**: 完整交易系统
**推荐使用**: ✅ 是 (最新最全功能)
**更新时间**: 2025-11-05 11:26:39
