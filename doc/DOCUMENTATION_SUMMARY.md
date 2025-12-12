# OKX API 文档提取摘要

## 概述
本项目成功从 OKX API 文档网站（https://www.okx.com/docs-v5/zh/）提取了完整的API文档信息，包括多个API模块的详细信息。

## 已提取的文档

### 1. 交易账户 API (okx_api_trading_account.md)
- **接口数量**: 51个
- **类型**: REST API
- **内容**: 包括获取交易产品基础信息、查看账户余额、查看持仓信息、账单流水查询等功能

### 2. 撮合交易 API (okx_api_order_book_trading.md)
- **接口数量**: 35个
- **类型**: REST API + WebSocket
- **内容**: 包括下单、撤单、改单、查询订单等功能

### 3. 公共数据 API (okx_api_public_data.md)
- **接口数量**: 42个
- **类型**: REST API + WebSocket
- **内容**: 包括交易产品信息、资金费率、标记价格、指数价格等公共数据

### 4. 资金账户 API (okx_api_funding_account.md)
- **接口数量**: 29个
- **类型**: REST API + WebSocket
- **内容**: 包括资金划转、充值提币、资产估值等功能

### 5. 错误码信息 (okx_api_error_code.md)
- **错误码数量**: 14个已明确标识的错误码
- **类型**: REST API 和 WebSocket 错误码
- **内容**: 包括常见错误码及描述

## 提取方法
- 使用 Python 脚本直接下载并解析完整的 HTML 文档
- 通过 BeautifulSoup 解析 HTML 结构
- 提取所有 API 接口的详细信息，包括：
  - 接口描述
  - HTTP 请求方法和路径
  - 请求参数表格
  - 返回参数表格
  - 限速规则
  - 示例代码

## 文档结构
每个API文档都包含以下结构：
- API 接口标题和描述
- 限速信息
- HTTP 请求方法和路径
- 请求参数（表格格式）
- 返回参数（表格格式）
- 示例代码
- WebSocket 频道信息（如适用）

## 用途
这些文档可以用于：
- API 集成开发
- 了解 OKX 交易所的 API 接口规范
- 自动化交易系统开发
- API 调试和测试