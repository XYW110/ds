# OKX API 撮合交易

## POST / 撤单

撤销之前下的未完成订单。


### 限速：60次/2s


### 限速规则（期权以外）：User ID + Instrument ID


### 限速规则（只限期权）：User ID + Instrument Family


### 权限：交易


### HTTP请求

POST /api/v5/trade/cancel-order


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| ordId | String | 可选 | 订单ID，ordId和clOrdId必须传一个，若传两个，以ordId为主 |
| clOrdId | String | 可选 | 用户自定义ID |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| code | String | 结果代码，0表示成功 |
| msg | String | 错误信息，代码为0时，该字段为空 |
| data | Array of objects | 包含结果的对象数组 |
| > ordId | String | 订单ID |
| > clOrdId | String | 客户自定义订单ID |
| > ts | String | 系统完成订单请求处理的时间戳，Unix时间戳的毫秒数格式，如1597026383085 |
| > sCode | String | 事件执行结果的code，0代表成功 |
| > sMsg | String | 事件执行失败时的msg |
| inTime | String | REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。 |
| outTime | String | REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |



---

## POST / 修改订单

修改当前未成交的挂单


### 限速：60次/2s


### 跟单交易带单员带单产品的限速：4个/2s


### 限速规则：User ID + Instrument ID


### 权限：交易

该接口限速同时受到子账户限速及基于成交比率的子账户限速限速规则的影响。


### HTTP请求

POST /api/v5/trade/amend-order


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID |
| cxlOnFail | Boolean | 否 | 当订单修改失败时，该订单是否需要自动撤销。默认为falsefalse：不自动撤单true：自动撤单 |
| ordId | String | 可选 | 订单IDordId和clOrdId必须传一个，若传两个，以ordId为主 |
| clOrdId | String | 可选 | 用户自定义订单ID |
| reqId | String | 否 | 用户自定义修改事件ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。 |
| newSz | String | 可选 | 修改的新数量，必须大于0，对于部分成交订单，该数量应包含已成交数量。 |
| newPx | String | 可选 | 修改后的新价格修改的新价格期权改单时，newPx/newPxUsd/newPxVol 只能填一个，且必须与下单参数保持一致，如下单用px，改单时需使用newPx |
| newPxUsd | String | 可选 | 以USD价格进行期权改单仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个 |
| newPxVol | String | 可选 | 以隐含波动率进行期权改单，如 1 代表 100%仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个 |
| pxAmendType | String | 否 | 订单价格修正类型0：当newPx超出价格限制时，不允许系统修改订单价格1：当newPx超出价格限制时，允许系统将价格修改为限制范围内的最优值默认值为0 |
| attachAlgoOrds | Array of objects | 否 | 修改附带止盈止损信息 |
| > attachAlgoId | String | 可选 | 附带止盈止损的订单ID，由系统生成，改单时必填，用来标识该笔附带止盈止损订单。下止盈止损委托单时，该值不会传给 algoId |
| > attachAlgoClOrdId | String | 可选 | 下单附带止盈止损时，客户自定义的策略订单ID |
| > newTpTriggerPx | String | 可选 | 止盈触发价如果止盈触发价或者委托价为0，那代表删除止盈。 |
| > newTpTriggerRatio | String | 可选 | 止盈触发比例，0.3 代表 30%仅适用于交割/永续合约如果主单为买入订单，必须大于 0，如果主单为卖出订单，必须处于 -1 和 0 之间。0 代表删除止盈。 |
| > newTpOrdPx | String | 可选 | 止盈委托价委托价格为-1时，执行市价止盈。 |
| > newTpOrdKind | String | 否 | 止盈订单类型condition: 条件单limit: 限价单 |
| > newSlTriggerPx | String | 可选 | 止损触发价如果止损触发价或者委托价为0，那代表删除止损。 |
| > newSlTriggerRatio | String | 可选 | 止损触发比例，0.3 代表 30%仅适用于交割/永续合约如果主单为买入订单，必须处于 0 和 1 之间，如果主单为卖出订单，必须大于 0。0 代表删除止损。 |
| > newSlOrdPx | String | 可选 | 止损委托价委托价格为-1时，执行市价止损。 |
| > newTpTriggerPxType | String | 可选 | 止盈触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止盈，该参数必填 |
| > newSlTriggerPxType | String | 可选 | 止损触发价类型last：最新价格index：指数价格mark：标记价格只适用于交割/永续如果要新增止损，该参数必填 |
| > sz | String | 可选 | 新的张数。仅适用于“多笔止盈”的止盈订单且必填 |
| > amendPxOnTriggerType | String | 否 | 是否启用开仓价止损，仅适用于分批止盈的止损订单0：不开启，默认值1：开启 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| code | String | 结果代码，0表示成功 |
| msg | String | 错误信息，代码为0时，该字段为空 |
| data | Array of objects | 包含结果的对象数组 |
| > ordId | String | 订单ID |
| > clOrdId | String | 用户自定义ID |
| > ts | String | 系统完成订单请求处理的时间戳，Unix时间戳的毫秒数格式，如1597026383085 |
| > reqId | String | 用户自定义修改事件ID |
| > sCode | String | 事件执行结果的code，0代表成功 |
| > sMsg | String | 事件执行失败时的msg |
| inTime | String | REST网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123返回的时间是请求验证后的时间。 |
| outTime | String | REST网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |



---

## GET / 获取一键还债历史记录

查询一键还债近7天的历史记录与进度状态。仅适用于跨币种保证金模式/组合保证金模式。


### 限速：1次/2s


### 限速规则：User ID


### 权限：读取


### HTTP 请求

GET /api/v5/trade/one-click-repay-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| after | String | 否 | 查询在此之前的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085 |
| before | String | 否 | 查询在此之后的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085 |
| limit | String | 否 | 返回的结果集数量，默认为100，最大为100 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| debtCcy | String | 负债币种 |
| fillDebtSz | String | 对应的负债币种成交数量 |
| repayCcy | String | 偿还币种 |
| fillRepaySz | String | 偿还币种实际支付数量 |
| status | String | 当前还债进度/状态running: 进行中filled: 已完成failed: 失败 |
| uTime | String | 交易时间戳，Unix时间戳为毫秒数格式，如 1597026383085 |



---

## GET / 获取一键还债历史记录(新)

查询一键还债近7天的历史记录与进度状态。仅适用于现货模式。


### 限速：1次/2s


### 限速规则：User ID


### 权限：读取


### HTTP 请求

GET /api/v5/trade/one-click-repay-history-v2


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| after | String | 否 | 查询在指定请求时间ts之前(包含)的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085 |
| before | String | 否 | 查询在指定请求时间ts之后(包含)的内容，值为时间戳，Unix时间戳为毫秒数格式，如1597026383085 |
| limit | String | 否 | 返回的结果集数量，默认为100，最大为100 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| debtCcy | String | 负债币种 |
| repayCcyList | Array of strings | 偿还币种列表，如 ["USDC","BTC"] |
| fillDebtSz | String | 对应的负债币种成交数量 |
| status | String | 当前还债进度/状态running：进行中filled：已完成failed：失败 |
| ordIdInfo | Array of objects | 相关订单信息 |
| > ordId | String | 订单ID |
| > instId | String | 产品ID，如BTC-USDT |
| > ordType | String | 订单类型ioc：立即成交并取消剩余 |
| > side | String | 订单方向buysell |
| > px | String | 委托价格 |
| > sz | String | 委托数量 |
| > fillPx | String | 最新成交价格如果成交数量为0，该字段为"" |
| > fillSz | String | 最新成交数量 |
| > state | String | 订单状态filled：完全成交canceled：撤单成功 |
| > cTime | String | 订单创建时间，Unix时间戳的毫秒数格式，如1597026383085 |
| ts | String | 请求时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## POST / 倒计时全部撤单

在倒计时结束后，取消所有挂单。适用于所有撮合交易产品（不包括价差交易）。


### 限速：1次/s


### 限速规则：User ID + tag


### 权限：交易


### HTTP请求

POST /api/v5/trade/cancel-all-after


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| timeOut | String | 是 | 取消挂单的倒计时，单位为秒取值范围为 0, [10, 120]0 代表不使用该功能 |
| tag | String | 否 | CAA订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| triggerTime | String | 触发撤单的时间triggerTime=0 代表未使用该功能 |
| tag | String | CAA订单标签 |
| ts | String | 请求被接收到的时间 |



---

## GET / 获取账户限速

获取账户限速相关信息

仅有新订单及修改订单请求会被计入此限制。对于包含多个订单的批量请求，每个订单将被单独计数。

更多细节，请见基于成交比率的子账户限速


### 限速：1次/s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/trade/account-rate-limit


### 请求参数

None


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| fillRatio | String | 监测期内子账户的成交比率适用于交易费等级 >= VIP 5的用户，其余用户返回""对于监测期内没有交易量的账户，返回"0"。对于监测期内有交易量，但没有订单操作数的用户，返回"9999"。 |
| mainFillRatio | String | 监测期内母账户合计成交比率适用于交易费等级 >= VIP 5的用户，其余用户返回""对于监测期内没有交易量的账户，返回"0" |
| accRateLimit | String | 当前子账户交易限速（每两秒） |
| nextAccRateLimit | String | 预计下一周期子账户交易限速（每两秒）适用于交易费等级 >= VIP 5的用户，其余用户返回"" |
| ts | String | 数据更新时间对于交易费等级>= VIP 5的用户，数据将于每日16:00（UTC+8）生成对于交易费等级 < VIP 5的用户，返回当前时间戳 |



---

## POST / 订单预检查

用来预先查看订单下单前后的账户的对比信息，仅适用于跨币种保证金模式和组合保证金模式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/trade/order-precheck


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| tdMode | String | 是 | 交易模式保证金模式：isolated：逐仓 ；cross：全仓非保证金模式：cash：非保证金spot_isolated：现货逐仓(仅适用于现货带单) ，现货带单时，tdMode的值需要指定为spot_isolated |
| side | String | 是 | 订单方向buy：买，sell：卖 |
| posSide | String | 可选 | 持仓方向在开平仓模式下必填，且仅可选择long或short。 仅适用交割、永续。 |
| ordType | String | 是 | 订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消ioc：立即成交并取消剩余optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）elp：流动性增强计划订单 |
| sz | String | 是 | 委托数量 |
| px | String | 可选 | 委托价格，仅适用于limit、post_only、fok、ioc类型的订单 |
| reduceOnly | Boolean | 否 | 是否只减仓，true或false，默认false仅适用于币币杠杆，以及买卖模式下的交割/永续仅适用于合约模式和跨币种保证金模式 |
| tgtCcy | String | 否 | 市价单委托数量sz的单位，仅适用于币币市价订单base_ccy: 交易货币 ；quote_ccy：计价货币买单默认quote_ccy， 卖单默认base_ccy |
| attachAlgoOrds | Array of objects | 否 | 下单附带止盈止损信息 |
| > attachAlgoClOrdId | String | 否 | 下单附带止盈止损时，客户自定义的策略订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。订单完全成交，下止盈止损委托单时，该值会传给algoClOrdId |
| > tpTriggerPx | String | 可选 | 止盈触发价对于条件止盈单，如果填写此参数，必须填写 止盈委托价 |
| > tpOrdPx | String | 可选 | 止盈委托价对于条件止盈单，如果填写此参数，必须填写 止盈触发价对于限价止盈单，需填写此参数，不需要填写止盈触发价委托价格为-1时，执行市价止盈 |
| > tpOrdKind | String | 否 | 止盈订单类型condition: 条件单limit: 限价单默认为condition |
| > slTriggerPx | String | 可选 | 止损触发价，如果填写此参数，必须填写 止损委托价 |
| > slOrdPx | String | 可选 | 止损委托价，如果填写此参数，必须填写 止损触发价委托价格为-1时，执行市价止损 |
| > tpTriggerPxType | String | 否 | 止盈触发价类型last：最新价格index：指数价格mark：标记价格默认为last |
| > slTriggerPxType | String | 否 | 止损触发价类型last：最新价格index：指数价格mark：标记价格默认为last |
| > sz | String | 可选 | 数量。仅适用于“多笔止盈”的止盈订单，且对于“多笔止盈”的止盈订单必填 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| adjEq | String | 当前美金层面有效保证金 |
| adjEqChg | String | 下单后，美金层面有效保证金的变动数量 |
| imr | String | 当前美金层面占用保证金 |
| imrChg | String | 下单后，美金层面占用保证金的变动数量 |
| mmr | String | 当前美金层面维持保证金 |
| mmrChg | String | 下单后，美金层面维持保证金的变动数量 |
| mgnRatio | String | 当前美金层面维持保证金率 |
| mgnRatioChg | String | 下单后，美金层面维持保证金率的变动数量 |
| availBal | String | 当前币种可用余额，仅适用于关闭自动借币时 |
| availBalChg | String | 下单后，币种可用余额的变动数量，仅适用于关闭自动借币时 |
| liqPx | String | 当前预估强平价 |
| liqPxDiff | String | 下单后，预估强平价与标记价格的差距 |
| liqPxDiffRatio | String | 下单后，预估强平价与标记价格的差距比率 |
| posBal | String | 当前杠杆逐仓仓位正资产，仅适用于逐仓杠杆 |
| posBalChg | String | 下单后，杠杆逐仓仓位正资产的变动数量，仅适用于逐仓杠杆 |
| liab | String | 当前负债如果是全仓，对应全仓负债，如果是逐仓，对应逐仓负债 |
| liabChg | String | 下单后，当前负债的变动数量如果是全仓，对应全仓负债，如果是逐仓，对应逐仓负债 |
| liabChgCcy | String | 下单后，当前负债变动数量的单位仅适用于全仓，开启自动借币时 |
| type | String | 仓位正资产(posBal)的单位类型，仅适用于杠杆逐仓，用来确定posBal的单位1:下单前后都是交易货币2:下单前是交易货币，下单后是计价货币3:下单前是计价货币，下单后是交易货币4:下单前后都是计价货币 |



---

## WS / 订单频道

获取订单信息，首次订阅不推送，只有当下单、订单变更时，推送数据该频道的并发连接受到如下规则限制：WebSocket 连接限制


### 服务地址

/ws/v5/private (需要登录)


### 请求参数



| 参数 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| id | String | 否 | 消息的唯一标识。用户提供，返回参数中会返回以便于找到相应的请求。字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度必须要在1-32位之间。 |
| op | String | 是 | 操作subscribeunsubscribe |
| args | Array of objects | 是 | 请求订阅的频道列表 |
| > channel | String | 是 | 频道名orders |
| > instType | String | 是 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权ANY：全部 |
| > instFamily | String | 否 | 交易品种适用于交割/永续/期权 |
| > instId | String | 否 | 产品ID |



### 返回参数



| 参数 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| id | String | 否 | 消息的唯一标识 |
| event | String | 是 | 事件subscribeunsubscribeerror |
| arg | Object | 否 | 订阅的频道 |
| > channel | String | 是 | 频道名 |
| > instType | String | 是 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权ANY：全部 |
| > instFamily | String | 否 | 交易品种适用于交割/永续/期权 |
| > instId | String | 否 | 产品ID |
| code | String | 否 | 错误码 |
| msg | String | 否 | 错误消息 |
| connId | String | 是 | WebSocket连接ID |



### 推送数据参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| arg | Object | 订阅成功的频道 |
| > channel | String | 频道名 |
| > uid | String | 用户标识 |
| > instType | String | 产品类型 |
| > instFamily | String | 交易品种 |
| > instId | String | 产品ID |
| data | Array of objects | 订阅的数据 |
| > instType | String | 产品类型 |
| > instId | String | 产品ID |
| > ccy | String | 保证金币种，适用于逐仓杠杆及合约模式下的全仓杠杆订单以及交割、永续和期权合约订单。 |
| > ordId | String | 订单ID |
| > clOrdId | String | 由用户设置的订单ID来识别您的订单 |
| > tag | String | 订单标签 |
| > px | String | 委托价格，对于期权，以币(如BTC, ETH)为单位 |
| > pxUsd | String | 期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串"" |
| > pxVol | String | 期权订单的隐含波动率仅适用于期权，其他业务线返回空字符串"" |
| > pxType | String | 期权的价格类型px：代表按价格下单，单位为币 (请求参数 px 的数值单位是BTC或ETH)pxVol：代表按pxVol下单pxUsd：代表按照pxUsd下单，单位为USD (请求参数px 的数值单位是USD) |
| > sz | String | 原始委托数量，币币/币币杠杆，以币为单位；交割/永续/期权，以张为单位 |
| > notionalUsd | String | 委托单预估美元价值 |
| > fillNotionalUsd | String | 委托单已成交的美元价值 |
| > ordType | String | 订单类型market：市价单limit：限价单post_only：只做maker单fok：全部成交或立即取消单ioc：立即成交并取消剩余单optimal_limit_ioc：市价委托立即成交并取消剩余（仅适用交割、永续）mmp：做市商保护(仅适用于组合保证金账户模式下的期权订单)mmp_and_post_only：做市商保护且只做maker单(仅适用于组合保证金账户模式下的期权订单)op_fok：期权简选（全部成交或立即取消）elp：流动性增强计划订单 |
| > side | String | 订单方向，buysell |
| > posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| > tdMode | String | 交易模式保证金模式isolated：逐仓cross：全仓非保证金模式cash：现金 |
| > tgtCcy | String | 市价单委托数量sz的单位base_ccy: 交易货币quote_ccy：计价货币 |
| > fillPx | String | 当前推送消息的成交价格 |
| > tradeId | String | 当前推送消息的成交ID |
| > fillSz | String | 当前推送消息的成交数量对于币币和杠杆，单位为交易货币，如 BTC-USDT, 单位为 BTC；对于市价单，无论tgtCcy是base_ccy，还是quote_ccy，单位均为交易货币；对于交割、永续以及期权，单位为张。 |
| > fillPnl | String | 当前推送消息的成交收益，适用于有成交的平仓订单。其他情况均为0。 |
| > fillTime | String | 当前推送消息的成交时间 |
| > fillFee | String | 当前推送消息的成交手续费金额或者返佣金额：手续费扣除 为 ‘负数’，如 -0.01 ；手续费返佣 为 ‘正数’，如 0.01 |
| > fillFeeCcy | String | 当前推送消息的成交手续费币种或者返佣币种。如果fillFee小于0，为手续费币种；如果fillFee大于等于0，为返佣币种 |
| > fillPxVol | String | 成交时的隐含波动率仅适用于期权，其他业务线返回空字符串"" |
| > fillPxUsd | String | 成交时的期权价格，以USD为单位仅适用于期权，其他业务线返回空字符串"" |
| > fillMarkVol | String | 成交时的标记波动率，仅适用于期权，其他业务线返回空字符串"" |
| > fillFwdPx | String | 成交时的远期价格，仅适用于期权，其他业务线返回空字符串"" |
| > fillMarkPx | String | 成交时的标记价格，仅适用于交割/永续/期权 |
| > fillIdxPx | String | 交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如LTC-ETH，该字段返回LTC-USDT的指数价格。 |
| > execType | String | 当前推送消息成交的流动性方向    T：taker   M：maker |
| > accFillSz | String | 累计成交数量对于币币和杠杆，单位为交易货币，如 BTC-USDT, 单位为 BTC；对于市价单，无论tgtCcy是base_ccy，还是quote_ccy，单位均为交易货币；对于交割、永续以及期权，单位为张。 |
| > avgPx | String | 成交均价，如果成交数量为0，该字段也为0 |
| > state | String | 订单状态canceled：撤单成功live：等待成交partially_filled：部分成交filled：完全成交mmp_canceled：做市商保护机制导致的自动撤单 |
| > lever | String | 杠杆倍数，0.01到125之间的数值，仅适用于币币杠杆/交割/永续 |
| > attachAlgoClOrdId | String | 下单附带止盈止损时，客户自定义的策略订单ID |
| > tpTriggerPx | String | 止盈触发价 |
| > tpTriggerPxType | String | 止盈触发价类型last：最新价格index：指数价格mark：标记价格 |
| > tpOrdPx | String | 止盈委托价，止盈委托价格为-1时，执行市价止盈 |
| > slTriggerPx | String | 止损触发价 |
| > slTriggerPxType | String | 止损触发价类型last：最新价格index：指数价格mark：标记价格 |
| > slOrdPx | String | 止损委托价，止损委托价格为-1时，执行市价止损 |
| > attachAlgoOrds | Array of objects | 下单附带止盈止损信息 |
| >> attachAlgoId | String | 附带止盈止损的订单ID，改单时，可用来标识该笔附带止盈止损订单。下止盈止损委托单时，该值不会传给 algoId |
| >> attachAlgoClOrdId | String | 下单附带止盈止损时，客户自定义的策略订单ID |
| >> tpOrdKind | String | 止盈订单类型condition: 条件单limit: 限价单 |
| >> tpTriggerPx | String | 止盈触发价 |
| >> tpTriggerRatio | String | 止盈触发比例，0.3 代表 30%仅适用于交割/永续合约 |
| >> tpTriggerPxType | String | 止盈触发价类型last：最新价格index：指数价格mark：标记价格 |
| >> tpOrdPx | String | 止盈委托价 |
| >> slTriggerPx | String | 止损触发价 |
| >> slTriggerRatio | String | 止损触发比例，0.3 代表 30%仅适用于交割/永续合约 |
| >> slTriggerPxType | String | 止损触发价类型last：最新价格index：指数价格mark：标记价格 |
| >> slOrdPx | String | 止损委托价 |
| >> sz | String | 张数。仅适用于“多笔止盈”的止盈订单 |
| >> amendPxOnTriggerType | String | 是否启用开仓价止损，仅适用于分批止盈的止损订单0：不开启，默认值1：开启 |
| > linkedAlgoOrd | Object | 止损订单信息，仅适用于包含限价止盈单的双向止盈止损订单，触发后生成的普通订单 |
| >> algoId | Object | 策略订单唯一标识 |
| > stpId | String | 自成交保护ID如果自成交保护不适用则返回""（已弃用） |
| > stpMode | String | 自成交保护模式 |
| > feeCcy | String | 手续费币种对于币币和杠杆的挂单卖单，表示计价币种；其他情况下，表示收取手续费的币种 |
| > fee | String | 手续费金额对于币币和杠杆（除挂单卖单外）：平台收取的累计手续费，始终为负数。对于币币和杠杆的挂单卖单、交割、永续和期权：累计手续费和返佣（币币和杠杆挂单卖单始终以计价币种计算） |
| > rebateCcy | String | 返佣币种对于币币和杠杆的挂单卖单，表示交易币种；其他情况下，表示支付返佣的币种 |
| > rebate | String | 返佣金额，仅适用于币币和杠杆对于挂单卖单：以交易币种为单位的累计手续费和返佣金额。其他情况下，表示挂单返佣金额，始终为正数，如无返佣时返回""。 |
| > pnl | String | 收益(不包括手续费)适用于有成交的平仓订单，其他情况均为0对于合约全仓爆仓，将包含相应强平惩罚金 |
| > source | String | 订单来源6：计划委托策略触发后的生成的普通单7：止盈止损策略触发后的生成的普通单13：策略委托单触发后的生成的普通单25：移动止盈止损策略触发后的生成的普通单34: 追逐限价委托生成的普通单 |
| > cancelSource | String | 订单取消的来源有效值及对应的含义是：0: 已撤单：系统撤单1: 用户主动撤单2: 已撤单：预减仓撤单，用户保证金不足导致挂单被撤回3: 已撤单：风控撤单，用户保证金不足有爆仓风险，导致挂单被撤回4: 已撤单：币种借币量达到平台硬顶，系统已撤回该订单6: 已撤单：触发 ADL 撤单，用户维持保证金率较低且有爆仓风险，导致挂单被撤回7: 已撤单：交割合约到期9: 已撤单：扣除资金费用后可用余额不足，系统已撤回该订单10: 已撤单：期权合约到期13: 已撤单：FOK 委托订单未完全成交，导致挂单被完全撤回14: 已撤单：IOC 委托订单未完全成交，仅部分成交，导致部分挂单被撤回15: 已撤单：该订单委托价不在限价范围内17: 已撤单：平仓单被撤单，由于仓位已被市价全平20: 系统倒计时撤单21: 已撤单：相关仓位被完全平仓，系统已撤销该止盈止损订单22已撤单：存在更优价格的同方向订单，系统自动撤销当前操作的只减仓订单23已撤单：存在更优价格的同方向订单，系统自动撤销已存在的只减仓订单27: 成交滑点超过5%，触发成交差价保护导致系统撤单31: 当前只挂单订单 (Post only) 将会吃掉挂单深度32: 自成交保护33: 当前 taker 订单匹配的订单数量超过最大限制36: 关联止损被触发，撤销限价止盈37: 关联止损被撤销，撤销限价止盈38: 您已撤销做市商保护 (MMP) 类型订单39: 因做市商保护 (MMP) 被触发，该类型订单已被撤销42: 初始下单价格与最新的买一或卖一价已达到最大追逐距离，您的订单已被自动取消43: 由于买单价格高于指数价格或卖单价格低于指数价格，导致系统撤单44：由于该币种的可用余额不足，无法在触发自动换币后进行兑换，您的订单已撤销，撤销订单后恢复的余额将用于自动换币。当该币种的总抵押借贷量达到平台抵押借贷风控上限时，则会触发自动换币。45：ELP订单价格校验失败46：由于降低Delta而导致的撤单 |
| > amendSource | String | 订单修改的来源1: 用户主动改单，改单成功2: 用户主动改单，并且当前这笔订单被只减仓修改，改单成功3: 用户主动下单，并且当前这笔订单被只减仓修改，改单成功4: 用户当前已存在的挂单（非当前操作的订单），被只减仓修改，改单成功5：期权 px, pxVol 或 pxUsd 的跟随变动导致的改单，比如 iv=60，USD，px 锚定iv=60 时，USD, px 产生变动时的改单 |
| > category | String | 订单种类分类normal：普通委托订单种类twap：TWAP订单种类adl：ADL订单种类full_liquidation：爆仓订单种类partial_liquidation：减仓订单种类delivery：交割ddh：对冲减仓类型订单auto_conversion：抵押借币自动还币订单 |
| > isTpLimit | String | 是否为限价止盈，true 或 false. |
| > uTime | String | 订单更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| > cTime | String | 订单创建时间，Unix时间戳的毫秒数格式，如1597026383085 |
| > reqId | String | 修改订单时使用的request ID，如果没有修改，该字段为"" |
| > amendResult | String | 修改订单的结果-1：失败0：成功1：自动撤单（修改请求返回成功但最终改单失败导致自动撤销）2: 自动改单成功，仅适用于期权pxUsd和pxVol订单的自动改单通过API修改订单时，如果cxlOnFail设置为true且修改返回结果为失败时，则返回 ""通过API修改订单时，如果修改返回结果为成功但修改最终失败后，当cxlOnFail设置为false时返回-1;当cxlOnFail设置为true时则返回1通过Web/APP修改订单时，如果修改失败后，则返回-1 |
| > reduceOnly | String | 是否只减仓，true或false |
| > quickMgnType | String | 一键借币类型，仅适用于杠杆逐仓的一键借币模式manual：手动，auto_borrow：自动借币，auto_repay：自动还币 |
| > algoClOrdId | String | 客户自定义策略订单ID。策略订单触发，且策略单有algoClOrdId时有值，否则为"", |
| > algoId | String | 策略委托单ID，策略订单触发时有值，否则为"" |
| > lastPx | String | 最新成交价 |
| > code | String | 错误码，默认为0 |
| > msg | String | 错误消息，默认为"" |
| > tradeQuoteCcy | String | 用于交易的计价币种。 |



---

## WS / 撤单

撤销当前未完成订单


### 服务地址

/ws/v5/private (需要登录)


### 限速：60次/2s


### 限速规则（期权以外）：User ID + Instrument ID


### 限速规则（只限期权）：User ID + Instrument Family


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| id | String | 是 | 消息的唯一标识用户提供，返回参数中会返回以便于找到相应的请求。字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度必须要在1-32位之间。 |
| op | String | 是 | 支持的业务操作，如cancel-order |
| args | Array of objects | 是 | 请求参数 |
| > instIdCode | Integer | 可选 | 产品唯一标识代码。instId 和 instIdCode 两个都传时，instIdCode 优先级更高 |
| > instId | String | 可选 | 产品ID将于 2026 年 2 月 上旬下线 |
| > ordId | String | 可选 | 订单IDordId和clOrdId必须传一个，若传两个，以 ordId 为主 |
| > clOrdId | String | 可选 | 用户提供的订单ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度要在1-32位之间。 |



### 返回参数



| 参数 | 类型 | 描述 |
|--------|--------|--------|
| id | String | 消息的唯一标识 |
| op | String | 业务操作 |
| code | String | 代码 |
| msg | String | 消息 |
| data | Array of objects | 请求成功后返回的数据 |
| > ordId | String | 订单ID |
| > clOrdId | String | 由用户设置的订单ID |
| > ts | String | 系统完成订单请求处理的时间戳，Unix时间戳的毫秒数格式，如1597026383085 |
| > sCode | String | 订单状态码，0 代表成功 |
| > sMsg | String | 订单状态消息 |
| inTime | String | WebSocket 网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |
| outTime | String | WebSocket 网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |



---

## WS / 改单

修改当前未成交的订单


### 服务地址

/ws/v5/private (需要登录)


### 限速：60次/2s


### 跟单交易带单员带单产品的限速：4次/2s


### 限速规则（期权以外）：User ID + Instrument ID


### 限速规则（只限期权）：User ID + Instrument Family

该接口限速同时受到子账户限速及基于成交比率的子账户限速限速规则的影响。


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| id | String | 是 | 消息的唯一标识用户提供，返回参数中会返回以便于找到相应的请求。字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度必须要在1-32位之间。 |
| op | String | 是 | 支持的业务操作，如amend-order |
| args | Array of objects | 是 | 请求参数 |
| > instIdCode | Integer | 可选 | 产品唯一标识代码。instId 和 instIdCode 两个都传时，instIdCode 优先级更高 |
| > instId | String | 可选 | 产品ID将于 2026 年 2 月 上旬下线 |
| > cxlOnFail | Boolean | 否 | 当订单修改失败时，该订单是否需要自动撤销。默认为falsefalse：不自动撤单true：自动撤单 |
| > ordId | String | 可选 | 订单IDordId和clOrdId必须传一个，若传两个，以 ordId 为主 |
| > clOrdId | String | 可选 | 用户提供的订单ID |
| > reqId | String | 否 | 用户提供的reqId如果提供，那在返回参数中返回reqId，方便找到相应的修改请求。字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间。 |
| > newSz | String | 可选 | 请求修改的新数量，必须大于0。newSz和newPx不可同时为空。对于部分成交订单，该数量应包含已成交数量。 |
| > newPx | String | 可选 | 修改后的新价格修改的新价格期权改单时，newPx/newPxUsd/newPxVol 只能填一个，且必须与下单参数保持一致，如下单用px，改单时需使用newPx |
| > newPxUsd | String | 可选 | 以USD价格进行期权改单仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个 |
| > newPxVol | String | 可选 | 以隐含波动率进行期权改单，例如 1 代表 100%仅适用于期权，期权改单时，newPx/newPxUsd/newPxVol 只能填一个 |
| > pxAmendType | String | 否 | 订单价格修正类型0：当newPx超出价格限制时，不允许系统修改订单价格1：当newPx超出价格限制时，允许系统将价格修改为限制范围内的最优值默认值为0 |
| expTime | String | 否 | 请求有效截止时间。Unix时间戳的毫秒数格式，如1597026383085 |



### 返回参数



| 参数 | 类型 | 描述 |
|--------|--------|--------|
| id | String | 消息的唯一标识 |
| op | String | 业务操作 |
| code | String | 代码 |
| msg | String | 消息 |
| data | Array of objects | 请求成功后返回的数据 |
| > ordId | String | 订单ID |
| > clOrdId | String | 用户提供的订单ID |
| > ts | String | 系统完成订单请求处理的时间戳，Unix时间戳的毫秒数格式，如1597026383085 |
| > reqId | String | 用户提供的reqId如果用户在请求中提供reqId，则返回相应reqId |
| > sCode | String | 订单状态码，0 代表成功 |
| > sMsg | String | 订单状态消息 |
| inTime | String | WebSocket 网关接收请求时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |
| outTime | String | WebSocket 网关发送响应时的时间戳，Unix时间戳的微秒数格式，如1597026383085123 |



---
