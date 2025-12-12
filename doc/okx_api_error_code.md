# OKX API 错误码

## REST API 错误码

| 错误码 | 描述 |
|--------|--------|
| 0 | 200 |
| 1 | Operation failed. |
| 1000 | BboTbtChannelEvent |
| 1001 | BooksL2TbtChannelEvent |
| 1003 | BooksL2TbtElpChannelEvent |
| 1005 | TradesChannelEvent |
| 2 | Bulk operation partially |
| 3366 | 6:3368:8" |
| 3368 | 8:3372:8" |
| 4000 | 根据持仓事件推送，且根据设置的时间间隔定时推送（ms）若不添加该字段或将其设置为上述合法值以外的其他值，数据将根据事件推送并大约每 5 秒定期推送一次。使用该字段需严格遵守以下格式。"extraParams": "{\"updateInterval\": \"0\"}" |
| 51000 | Incorrect type of posSide (leg with Instrument Id [BTC-USD-SWAP]) |
| 51008 | Order failed. Insufficient BTC margin in account |
| 55123 | 100 |
| 60009 | Login failed. |
| 60012 | Invalid request: {\ |
| 60013 | Invalid args |
| 64008 | The connection will soon be closed for a service upgrade. Please reconnect. |

## WebSocket 错误码

WebSocket连接和消息相关的错误码：

| 错误码 | 描述 |
|--------|--------|
| 6000 | 认证失败 |
| 6001 | 重复登录 |
| 6002 | 业务异常 |
| 6003 | 订阅失败 |
| 6004 | 交易对不合法 |
| 6005 | 请重新登录 |
| 6006 | 请求过于频繁 |
