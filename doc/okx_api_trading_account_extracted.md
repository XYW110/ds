# OKX API 交易账户

## 获取交易产品基础信息

获取当前账户可交易产品的信息列表。


### 限速：20次/2s


### 限速规则：User ID + Instrument Type


### 权限：读取


### HTTP请求

GET /api/v5/account/instruments


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instFamily | String | 可选 | 交易品种，仅适用于交割/永续/期权，期权必填 |
| instId | String | 否 | 产品ID |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| instId | String | 产品id， 如BTC-USDT |
| uly | String | 标的指数，如BTC-USD，仅适用于杠杆/交割/永续/期权 |
| groupId | String | 交易产品手续费分组ID现货：1：USDT现货2：USDC及Crypto现货3：TRY现货4：EUR现货5：BRL现货7：AED现货8：AUD现货9：USD现货10：SGD现货11：零手续费现货12：现货分组一13：现货分组二14：现货分组三15: 现货特别分组交割合约：1：币本位交割合约2：USDT本位交割合约3：USDC本位交割合约4：盘前交易交割合约5：交割合约分组一6：交割合约分组二永续合约：1：币本位永续合约2：USDT本位永续合约3：USDC本位永续合约4：永续合约分组一5：永续合约分组二期权：1：币本位期权2：USDC本位期权用户需要同时使用instType和groupId来确定一个交易产品的交易手续费分组；用户应该将此接口和获取当前账户交易手续费费率一起使用，以获取特定交易产品的手续费率部分枚举值可能不适用于您，以实际返回为准 |
| instFamily | String | 交易品种，如BTC-USD，仅适用于杠杆/交割/永续/期权 |
| baseCcy | String | 交易货币币种，如BTC-USDT中的BTC，仅适用于币币/币币杠杆 |
| quoteCcy | String | 计价货币币种，如BTC-USDT中的USDT，仅适用于币币/币币杠杆 |
| settleCcy | String | 盈亏结算和保证金币种，如BTC仅适用于交割/永续/期权 |
| ctVal | String | 合约面值，仅适用于交割/永续/期权 |
| ctMult | String | 合约乘数，仅适用于交割/永续/期权 |
| ctValCcy | String | 合约面值计价币种，仅适用于交割/永续/期权 |
| optType | String | 期权类型，C或P仅适用于期权 |
| stk | String | 行权价格，仅适用于期权 |
| listTime | String | 上线时间Unix时间戳的毫秒数格式，如1597026383085 |
| auctionEndTime | String | 集合竞价结束时间，Unix时间戳的毫秒数格式，如1597026383085仅适用于通过集合竞价方式上线的币币，其余情况返回""（已废弃，请使用contTdSwTime） |
| contTdSwTime | String | 连续交易开始时间，从集合竞价、提前挂单切换到连续交易的时间，Unix时间戳格式，单位为毫秒。e.g.1597026383085。仅适用于通过集合竞价或提前挂单上线的SPOT/MARGIN，在其他情况下返回""。 |
| preMktSwTime | String | 盘前永续合约转为普通永续合约的时间，Unix时间戳的毫秒数格式，如1597026383085仅适用于盘前SWAP |
| openType | String | 开盘类型fix_price: 定价开盘pre_quote: 提前挂单call_auction: 集合竞价只适用于SPOT/MARGIN，其他业务线返回"" |
| expTime | String | 产品下线时间适用于币币/杠杆/交割/永续/期权，对于交割/期权，为交割/行权日期；亦可以为产品下线时间，有变动就会推送。 |
| lever | String | 该instId支持的最大杠杆倍数，不适用于币币、期权 |
| tickSz | String | 下单价格精度，如0.0001对于期权来说，是梯度中的最小下单价格精度，如果想要获取期权价格梯度，请使用"获取期权价格梯度"接口 |
| lotSz | String | 下单数量精度合约的数量单位是张，现货的数量单位是交易货币 |
| minSz | String | 最小下单数量合约的数量单位是张，现货的数量单位是交易货币 |
| ctType | String | 合约类型linear：正向合约inverse：反向合约仅适用于交割/永续 |
| state | String | 产品状态live：交易中suspend：暂停中preopen：预上线，交割和期权合约轮转生成到开始交易；部分交易产品上线前test：测试中（测试产品，不可交易） |
| ruleType | String | 交易规则类型normal：普通交易pre_market：盘前交易 |
| posLmtAmt | String | 单一用户层面的该产品最大持仓名义价值（USD），按同方向已持仓与挂单的美元名义价值计算。单用户有效上限为 max(posLmtAmt, oiUSD × posLmtPct)。适用于SWAP/FUTURES。 |
| posLmtPct | String | 单一用户相对于平台当前总持仓名义价值可持有的最大比例（如 30 表示 30%）。单用户有效上限为 max(posLmtAmt, oiUSD × posLmtPct)。适用于SWAP/FUTURES。 |
| maxPlatOILmt | String | 该产品的全平台最大持仓名义价值（USD）。当开启全平台持仓限制开关且平台总持仓达到或超过该值时，系统将拒绝所有用户的新开仓委托；否则订单通过校验。 |
| maxLmtSz | String | 限价单的单笔最大委托数量合约的数量单位是张，现货的数量单位是交易货币 |
| maxMktSz | String | 市价单的单笔最大委托数量合约的数量单位是张，现货的数量单位是USDT |
| maxLmtAmt | String | 限价单的单笔最大美元价值 |
| maxMktAmt | String | 市价单的单笔最大美元价值仅适用于币币/币币杠杆 |
| maxTwapSz | String | 时间加权单的单笔最大委托数量合约的数量单位是张，现货的数量单位是交易货币单笔最小委托数量为 minSz*2 |
| maxIcebergSz | String | 冰山委托的单笔最大委托数量合约的数量单位是张，现货的数量单位是交易货币 |
| maxTriggerSz | String | 计划委托委托的单笔最大委托数量合约的数量单位是张，现货的数量单位是交易货币 |
| maxStopSz | String | 止盈止损市价委托的单笔最大委托数量合约的数量单位是张，现货的数量单位是USDT |
| futureSettlement | Boolean | 交割合约是否支持每日结算适用于全仓交割 |
| tradeQuoteCcyList | Array of strings | 可用于交易的计价币种列表，如 ["USD", "USDC"]. |
| instIdCode | Integer | 产品唯一标识代码。对于简单二进制编码，您必须使用instIdCode而不是instId。对于同一instId，实盘和模拟盘的值可能会不一样。当值还未生成时，返回null。 |



---

## 查看账户余额

获取交易账户中资金余额信息。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/balance


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| uTime | String | 账户信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| totalEq | String | 美金层面权益 |
| isoEq | String | 美金层面逐仓仓位权益适用于合约模式/跨币种保证金模式/组合保证金模式 |
| adjEq | String | 美金层面有效保证金适用于现货模式/跨币种保证金模式/组合保证金模式 |
| availEq | String | 账户美金层面可用保证金，排除因总质押借币上限而被限制的币种适用于跨币种保证金模式/组合保证金模式 |
| ordFroz | String | 美金层面全仓挂单占用保证金仅适用于现货模式/跨币种保证金模式/组合保证金模式 |
| imr | String | 美金层面占用保证金适用于现货模式/跨币种保证金模式/组合保证金模式 |
| mmr | String | 美金层面维持保证金适用于现货模式/跨币种保证金模式/组合保证金模式 |
| borrowFroz | String | 账户美金层面潜在借币占用保证金仅适用于现货模式/跨币种保证金模式/组合保证金模式。在其他账户模式下为""。 |
| mgnRatio | String | 美金层面维持保证金率适用于现货模式/跨币种保证金模式/组合保证金模式 |
| notionalUsd | String | 以美金价值为单位的持仓数量，即仓位美金价值适用于现货模式/跨币种保证金模式/组合保证金模式 |
| notionalUsdForBorrow | String | 借币金额（美元价值）适用于现货模式/跨币种保证金模式/组合保证金模式 |
| notionalUsdForSwap | String | 永续合约持仓美元价值适用于跨币种保证金模式/组合保证金模式 |
| notionalUsdForFutures | String | 交割合约持仓美元价值适用于跨币种保证金模式/组合保证金模式 |
| notionalUsdForOption | String | 期权持仓美元价值适用于现货模式/跨币种保证金模式/组合保证金模式 |
| upl | String | 账户层面全仓未实现盈亏（美元单位）适用于跨币种保证金模式/组合保证金模式 |
| delta | String | Delta (USD) |
| deltaLever | String | Delta权益比率deltaLever = delta/totalEq |
| deltaNeutralStatus | String | Delta 风险状态0: 普通1: 限制划转2: 仅支持降低 Delta - 相同基础货币的现货、交割和永续合约视为同一标的资产。同一标的资产内，仅能新下一笔降低 Delta 值的订单，且下单时不应存在其他挂单。如果触发此限制，且您的账户 Delta 大于 500,000 USD，您的所有限价、市价、高级限价单挂单将被撤销。 |
| details | Array of objects | 各币种资产详细信息 |
| > ccy | String | 币种 |
| > eq | String | 币种总权益 |
| > cashBal | String | 币种余额 |
| > uTime | String | 币种余额信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| > isoEq | String | 币种逐仓仓位权益适用于合约模式/跨币种保证金模式/组合保证金模式 |
| > availEq | String | 可用保证金适用于合约模式/跨币种保证金模式/组合保证金模式 |
| > disEq | String | 美金层面币种折算权益适用于现货模式(开通了借币功能)/跨币种保证金模式/组合保证金模式 |
| > fixedBal | String | 抄底宝、逃顶宝功能的币种冻结金额 |
| > availBal | String | 可用余额 |
| > frozenBal | String | 币种占用金额 |
| > ordFrozen | String | 挂单冻结数量适用于现货模式/合约模式/跨币种保证金模式 |
| > liab | String | 币种负债额值为正数，如 "21625.64"适用于现货模式/跨币种保证金模式/组合保证金模式 |
| > upl | String | 未实现盈亏适用于合约模式/跨币种保证金模式/组合保证金模式 |
| > uplLiab | String | 由于仓位未实现亏损导致的负债适用于跨币种保证金模式/组合保证金模式 |
| > crossLiab | String | 币种全仓负债额适用于现货模式/跨币种保证金模式/组合保证金模式 |
| > isoLiab | String | 币种逐仓负债额适用于跨币种保证金模式/组合保证金模式 |
| > rewardBal | String | 体验金余额 |
| > mgnRatio | String | 币种全仓维持保证金率，衡量账户内某项资产风险的指标适用于合约模式且有全仓仓位时 |
| > imr | String | 币种维度全仓占用保证金适用于合约模式且有全仓仓位时 |
| > mmr | String | 币种维度全仓维持保证金适用于合约模式且有全仓仓位时 |
| > interest | String | 计息，应扣未扣利息值为正数，如9.01适用于现货模式/跨币种保证金模式/组合保证金模式 |
| > twap | String | 当前负债币种触发自动换币的风险0、1、2、3、4、5其中之一，数字越大代表您的负债币种触发自动换币概率越高适用于现货模式/跨币种保证金模式/组合保证金模式 |
| > frpType | String | 自动换币类型0：未发生自动换币1：基于用户的自动换币2：基于平台借币限额的自动换币当twap>=1时返回1或2代表自动换币风险类型，适用于现货模式/跨币种保证金模式/组合保证金模式 |
| > maxLoan | String | 币种最大可借适用于现货模式/跨币种保证金模式/组合保证金模式的全仓 |
| > eqUsd | String | 币种权益美金价值 |
| > borrowFroz | String | 币种美金层面潜在借币占用保证金仅适用于现货模式/跨币种保证金模式/组合保证金模式。在其他账户模式下为""。 |
| > notionalLever | String | 币种杠杆倍数适用于合约模式 |
| > stgyEq | String | 策略权益 |
| > isoUpl | String | 逐仓未实现盈亏适用于合约模式/跨币种保证金模式/组合保证金模式 |
| > spotInUseAmt | String | 现货对冲占用数量适用于组合保证金模式 |
| > clSpotInUseAmt | String | 用户自定义现货占用数量适用于组合保证金模式 |
| > maxSpotInUse | String | 系统计算得到的最大可能现货占用数量适用于组合保证金模式 |
| > spotIsoBal | String | 现货逐仓余额仅适用于现货带单/跟单适用于现货模式/合约模式 |
| > smtSyncEq | String | 合约智能跟单权益默认为0，仅适用于跟单人。 |
| > spotCopyTradingEq | String | 现货智能跟单权益默认为0，仅适用于跟单人。 |
| > spotBal | String | 现货余额 ，单位为 币种，比如 BTC。详情 |
| > openAvgPx | String | 现货开仓成本价 单位 USD。详情 |
| > accAvgPx | String | 现货累计成本价 单位 USD。详情 |
| > spotUpl | String | 现货未实现收益，单位 USD。详情 |
| > spotUplRatio | String | 现货未实现收益率。详情 |
| > totalPnl | String | 现货累计收益，单位 USD。详情 |
| > totalPnlRatio | String | 现货累计收益率。详情 |
| > colRes | String | 平台维度质押限制状态0：限制未触发1：限制未触发，但该币种接近平台质押上限2：限制已触发。该币种不可用作新订单的保证金，这可能会导致下单失败。但它仍会被计入账户有效保证金，保证金率不会收到影响。更多详情，请参阅平台总质押借币上限说明。 |
| > colBorrAutoConversion | String | 基于平台质押借币限额的自动换币风险指标。分为1-5多个等级，数字越大，触发自动换币的可能性越大。默认值为0，表示当前无风险。5表示该用户正在进行自动换币，4代表该用户即将被进行自动换币，1/2/3表示存在自动换币风险。适用于现货模式/合约模式/跨币种保证金模式/组合保证金模式当某币种的全平台质押借币量超出平台总上限一定比例时，对于质押该币种且借币量较大的用户，平台将通过自动换币降低质押借币风险。请减少该币种的质押数量或偿还负债，以降低风险。更多详情，请参阅平台总质押借币上限说明。 |
| > collateralRestrict | Boolean | 平台维度的质押借币限制truefalse（已弃用，请使用colRes） |
| > collateralEnabled | Boolean | true：质押币false：非质押币适用于`跨币种保证金模式 |
| > autoLendStatus | String | 自动借出状态unsupported：该币种不支持自动借出off：自动借出功能关闭pending：自动借出功能开启但未匹配active：自动借出功能开启且已匹配 |
| > autoLendMtAmt | String | 自动借出已匹配量当 autoLendStatus 为unsupported/off/pending时返回 0当 autoLendStatus 为active时返回已匹配量 |


各账户等级下有效字段分布



| 参数 | 现货模式 | 合约模式 | 跨币种保证金模式 | 组合保证金模式 |
|--------|--------|--------|--------|--------|
| uTime | 是 | 是 | 是 | 是 |
| totalEq | 是 | 是 | 是 | 是 |
| isoEq |  | 是 | 是 | 是 |
| adjEq | 是 |  | 是 | 是 |
| availEq |  |  | 是 | 是 |
| ordFroz | 是 |  | 是 | 是 |
| imr | 是 |  | 是 | 是 |
| mmr | 是 |  | 是 | 是 |
| borrowFroz | 是 |  | 是 | 是 |
| mgnRatio | 是 |  | 是 | 是 |
| notionalUsd | 是 |  | 是 | 是 |
| notionalUsdForSwap |  |  | 是 | 是 |
| notionalUsdForFutures |  |  | 是 | 是 |
| notionalUsdForOption | 是 |  | 是 | 是 |
| notionalUsdForBorrow | 是 |  | 是 | 是 |
| upl |  |  | 是 | 是 |
| details |  |  |  |  |
| > ccy | 是 | 是 | 是 | 是 |
| > eq | 是 | 是 | 是 | 是 |
| > cashBal | 是 | 是 | 是 | 是 |
| > uTime | 是 | 是 | 是 | 是 |
| > isoEq |  | 是 | 是 | 是 |
| > availEq |  | 是 | 是 | 是 |
| > disEq | 是 |  | 是 | 是 |
| > availBal | 是 | 是 | 是 | 是 |
| > frozenBal | 是 | 是 | 是 | 是 |
| > ordFrozen | 是 | 是 | 是 | 是 |
| > liab | 是 |  | 是 | 是 |
| > upl |  | 是 | 是 | 是 |
| > uplLiab |  |  | 是 | 是 |
| > crossLiab | 是 |  | 是 | 是 |
| > isoLiab |  |  | 是 | 是 |
| > mgnRatio |  | 是 |  |  |
| > interest | 是 |  | 是 | 是 |
| > twap | 是 |  | 是 | 是 |
| > maxLoan | 是 |  | 是 | 是 |
| > eqUsd | 是 | 是 | 是 | 是 |
| > borrowFroz | 是 |  | 是 | 是 |
| > notionalLever |  | 是 |  |  |
| > stgyEq | 是 | 是 | 是 | 是 |
| > isoUpl |  | 是 | 是 | 是 |
| > spotInUseAmt |  |  |  | 是 |
| > spotIsoBal | 是 | 是 |  |  |
| > imr |  | 是 |  |  |
| > mmr |  | 是 |  |  |
| > spotBal | 是 | 是 | 是 | 是 |
| > openAvgPx | 是 | 是 | 是 | 是 |
| > accAvgPx | 是 | 是 | 是 | 是 |
| > spotUpl | 是 | 是 | 是 | 是 |
| > spotUplRatio | 是 | 是 | 是 | 是 |
| > totalPnl | 是 | 是 | 是 | 是 |
| > totalPnlRatio | 是 | 是 | 是 | 是 |
| > collateralEnabled |  |  | 是 |  |



---

## 查看持仓信息

获取该账户下拥有实际持仓的信息。账户为买卖模式会显示净持仓（net），账户为开平仓模式下会分别返回开多（long）或开空（short）的仓位。按照仓位创建时间倒序排列。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/positions


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权instType和instId同时传入的时候会校验instId与instType是否一致。 |
| instId | String | 否 | 交易产品ID，如：BTC-USDT-SWAP支持多个instId查询（不超过10个），半角逗号分隔 |
| posId | String | 否 | 持仓ID支持多个posId查询（不超过20个）。存在有效期的属性，自最近一次完全平仓算起，满30天 posId 以及整个仓位会被清除。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| posId | String | 持仓ID |
| posSide | String | 持仓方向long：开平仓模式开多，pos为正short：开平仓模式开空，pos为正net：买卖模式（交割/永续/期权：pos为正代表开多，pos为负代表开空。币币杠杆时，pos均为正，posCcy为交易货币时，代表开多；posCcy为计价货币时，代表开空。） |
| pos | String | 持仓数量，逐仓自主划转模式下，转入保证金后会产生pos为0的仓位 |
| hedgedPos | String | 对冲持仓数量仅在delta 中性策略模式的账户返回stgyType:1，对普通策略模式的账户返回"" |
| baseBal | String | 交易币余额，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| quoteBal | String | 计价币余额 ，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| baseBorrowed | String | 交易币已借，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| baseInterest | String | 交易币计息，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| quoteBorrowed | String | 计价币已借，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| quoteInterest | String | 计价币计息，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| posCcy | String | 仓位资产币种，仅适用于币币杠杆仓位 |
| availPos | String | 可平仓数量，适用于币币杠杆，期权对于杠杆仓位，平仓时，杠杆还清负债后，余下的部分会视为币币交易，如果想要减少币币交易的数量，可通过"获取最大可用数量"接口获取只减仓的可用数量。 |
| avgPx | String | 开仓均价会随结算周期变化，特别是在交割合约全仓模式下，结算时开仓均价会更新为结算价格，同时新增头寸也会改变开仓均价。 |
| nonSettleAvgPx | String | 未结算均价不受结算影响的加权开仓价格，仅在新增头寸时更新，和开仓均价的主要区别在于是否受到结算影响。仅适用于全仓交割 |
| upl | String | 未实现收益（以标记价格计算） |
| uplRatio | String | 未实现收益率（以标记价格计算 |
| uplLastPx | String | 以最新成交价格计算的未实现收益，主要做展示使用，实际值还是 upl |
| uplRatioLastPx | String | 以最新成交价格计算的未实现收益率 |
| instId | String | 产品ID，如BTC-USDT-SWAP |
| lever | String | 杠杆倍数，不适用于期权以及组合保证金模式下的全仓仓位 |
| liqPx | String | 预估强平价不适用于期权 |
| markPx | String | 最新标记价格 |
| imr | String | 初始保证金，仅适用于全仓 |
| margin | String | 保证金余额，可增减，仅适用于逐仓 |
| mgnRatio | String | 维持保证金率 |
| mmr | String | 维持保证金 |
| liab | String | 负债额，仅适用于币币杠杆 |
| liabCcy | String | 负债币种，仅适用于币币杠杆 |
| interest | String | 利息，已经生成的未扣利息 |
| tradeId | String | 最新成交ID |
| optVal | String | 期权市值，仅适用于期权 |
| pendingCloseOrdLiabVal | String | 逐仓杠杆负债对应平仓挂单的数量 |
| notionalUsd | String | 以美金价值为单位的持仓数量 |
| adl | String | 自动减仓信号区分为6档，从0到5，数字越小代表adl强度越弱仅适用于交割/永续/期权 |
| ccy | String | 占用保证金的币种 |
| last | String | 最新成交价 |
| idxPx | String | 最新指数价格 |
| usdPx | String | 保证金币种的市场最新美金价格 仅适用于交割/永续/期权 |
| bePx | String | 盈亏平衡价 |
| deltaBS | String | 美金本位持仓仓位delta，仅适用于期权 |
| deltaPA | String | 币本位持仓仓位delta，仅适用于期权 |
| gammaBS | String | 美金本位持仓仓位gamma，仅适用于期权 |
| gammaPA | String | 币本位持仓仓位gamma，仅适用于期权 |
| thetaBS | String | 美金本位持仓仓位theta，仅适用于期权 |
| thetaPA | String | 币本位持仓仓位theta，仅适用于期权 |
| vegaBS | String | 美金本位持仓仓位vega，仅适用于期权 |
| vegaPA | String | 币本位持仓仓位vega，仅适用于期权 |
| spotInUseAmt | String | 现货对冲占用数量适用于组合保证金模式 |
| spotInUseCcy | String | 现货对冲占用币种，如BTC适用于组合保证金模式 |
| clSpotInUseAmt | String | 用户自定义现货占用数量适用于组合保证金模式 |
| maxSpotInUseAmt | String | 系统计算得到的最大可能现货占用数量适用于组合保证金模式 |
| realizedPnl | String | 已实现收益仅适用于交割/永续/期权realizedPnl=pnl+fee+fundingFee+liqPenalty+settledPnl |
| settledPnl | String | 已结算收益仅适用于全仓交割 |
| pnl | String | 平仓订单累计收益额(不包括手续费) |
| fee | String | 累计手续费金额，正数代表平台返佣 ，负数代表平台扣除 |
| fundingFee | String | 累计资金费用 |
| liqPenalty | String | 累计爆仓罚金，有值时为负数。 |
| closeOrderAlgo | Array of objects | 平仓策略委托订单。调用策略委托下单，且closeFraction=1 时，该数组才会有值。 |
| > algoId | String | 策略委托单ID |
| > slTriggerPx | String | 止损触发价 |
| > slTriggerPxType | String | 止损触发价类型last：最新价格index：指数价格mark：标记价格 |
| > tpTriggerPx | String | 止盈触发价 |
| > tpTriggerPxType | String | 止盈触发价类型last：最新价格index：指数价格mark：标记价格 |
| > closeFraction | String | 策略委托触发时，平仓的百分比。1 代表100% |
| cTime | String | 持仓创建时间，Unix时间戳的毫秒数格式，如1597026383085 |
| uTime | String | 最近一次持仓更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| bizRefId | String | 外部业务id，如 体验券id |
| bizRefType | String | 外部业务类型 |



---

## 查看历史持仓信息

获取最近3个月有更新的仓位信息，按照仓位更新时间倒序排列。于2024年11月11日中午12:00（UTC+8）开始支持组合保证金账户模式下的历史持仓。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/positions-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instId | String | 否 | 交易产品ID，如：BTC-USD-SWAP |
| mgnMode | String | 否 | 保证金模式cross：全仓，isolated：逐仓 |
| type | String | 否 | 最近一次平仓的类型1：部分平仓;2：完全平仓;3：强平;4：强减;5：ADL自动减仓 - 仓位未完全平仓;6：ADL自动减仓 - 仓位完全平仓状态叠加时，以最新的平仓类型为准状态为准。 |
| posId | String | 否 | 持仓ID。存在有效期的属性，自最近一次完全平仓算起，满30天 posId 会失效，之后的仓位，会使用新的 posId。 |
| after | String | 否 | 查询仓位更新 (uTime) 之前的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085 |
| before | String | 否 | 查询仓位更新 (uTime) 之后的内容，值为时间戳，Unix 时间戳为毫秒数格式，如1597026383085 |
| limit | String | 否 | 分页返回结果的数量，最大为100，默认100条，uTime 相同的记录均会在当前请求中全部返回 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| instId | String | 交易产品ID |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| type | String | 最近一次平仓的类型1：部分平仓2：完全平仓3：强平4：强减5：ADL自动减仓状态叠加时，以最新的平仓类型为准状态为准。 |
| cTime | String | 仓位创建时间 |
| uTime | String | 仓位更新时间 |
| openAvgPx | String | 开仓均价会随结算周期变化，特别是在交割合约全仓模式下，结算时开仓均价会更新为结算价格，同时新增头寸也会改变开仓均价。 |
| nonSettleAvgPx | String | 未结算均价不受结算影响的加权开仓价格，仅在新增头寸时更新，和开仓均价的主要区别在于是否受到结算影响。仅适用于全仓交割 |
| closeAvgPx | String | 平仓均价 |
| posId | String | 仓位ID |
| openMaxPos | String | 最大持仓量 |
| closeTotalPos | String | 累计平仓量 |
| realizedPnl | String | 已实现收益仅适用于交割/永续/期权realizedPnl=pnl+fee+fundingFee+liqPenalty+settledPnl |
| settledPnl | String | 已实现收益仅适用于全仓交割 |
| pnlRatio | String | 已实现收益率 |
| fee | String | 累计手续费金额正数代表平台返佣，负数代表平台扣除。 |
| fundingFee | String | 累计资金费用 |
| liqPenalty | String | 累计爆仓罚金，有值时为负数。 |
| pnl | String | 已实现收益(不包括手续费) |
| posSide | String | 持仓模式方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| lever | String | 杠杆倍数 |
| direction | String | 持仓方向long：多short：空仅适用于杠杆/交割/永续/期权 |
| triggerPx | String | 触发标记价格type为3,4,5时有值；为1,2时为空 |
| uly | String | 标的指数 |
| ccy | String | 占用保证金的币种 |



---

## 查看账户持仓风险

查看账户整体风险。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/account-position-risk


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ts | String | 获取账户信息数据的时间，Unix时间戳的毫秒数格式，如1597026383085 |
| adjEq | String | 美金层面有效保证金适用于跨币种保证金模式和组合保证金模式 |
| balData | Array of objects | 币种资产信息 |
| > ccy | String | 币种 |
| > eq | String | 币种总权益 |
| > disEq | String | 美金层面币种折算权益 |
| posData | Array of objects | 持仓详细信息 |
| > instType | String | 产品类型 |
| > mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| > posId | String | 持仓ID |
| > instId | String | 产品ID，如BTC-USDT-SWAP |
| > pos | String | 以张为单位的持仓数量，逐仓自主划转模式下，转入保证金后会产生pos为0的仓位 |
| > baseBal | String | 交易币余额，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| > quoteBal | String | 计价币余额 ，适用于币币杠杆（逐仓一键借币模式）（已弃用） |
| > posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式（交割/永续/期权：pos为正代表开多，pos为负代表开空。币币杠杆：posCcy为交易货币时，代表开多；posCcy为计价货币时，代表开空。） |
| > posCcy | String | 仓位资产币种，仅适用于币币杠杆仓位 |
| > ccy | String | 占用保证金的币种 |
| > notionalCcy | String | 以币为单位的持仓数量 |
| > notionalUsd | String | 以美金价值为单位的持仓数量 |



---

## 账单流水查询（近七天）

帐户资产流水是指导致帐户余额增加或减少的行为。本接口可以查询最近7天的账单数据。


### 限速：5次/s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/bills


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instId | String | 否 | 产品ID，如BTC-USDT |
| ccy | String | 否 | 账单币种 |
| mgnMode | String | 否 | 仓位类型isolated：逐仓cross：全仓 |
| ctType | String | 否 | 合约类型linear：正向合约inverse：反向合约仅交割/永续有效 |
| type | String | 否 | 账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14：大宗交易15：一键借币16：借币22：一键还债24：价差交易26：结构化产品27：闪兑28：小额兑换29：一键还债30：简单交易32：移仓33：借贷34：结算250：跟单人分润支出251：跟单人分润退还 |
| subType | String | 否 | 账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出108：穿仓补偿110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权（实值期权买方）171：到期被行权（实值期权卖方）172：到期作废（非实值期权的买方和卖方）112：交割平多 （适用于FUTURES过期和SWAP下线）113：交割平空 （适用于FUTURES过期和SWAP下线）117：交割/行权穿仓补偿173：资金费支出174：资金费收入200：系统转入201：手动转入202：系统转出203：手动转出204：大宗交易买205：大宗交易卖206：大宗交易开多207：大宗交易开空208：大宗交易平多209：大宗交易平空210：一键借币的手动借币211：一键借币的手动还币212：一键借币的自动借币213：一键借币的自动还币220：USDT 买期权转入221：USDT 买期权转出16：强制还币17：强制借币还息224：一键还债买入225：一键还债卖出236：小额兑换买入237：小额兑换卖出250：永续分润支出251：永续分润退还280：现货分润支出281：现货分润退还282：现货分润收入283：现货跟单资产划转284：跟单自动转入285：跟单手动转入286：跟单自动转出287：跟单手动转出270：价差交易买271：价差交易卖272：价差交易开多273：价差交易开空274：价差交易平多275：价差交易平空290：系统转出小额资产293：固定借币扣息294：固定借币利息退款295：固定借币逾期利息296：结构化下单转出297：结构化下单转入298：结构化结算转出299：结构化结算转入306：手动借币307：自动借币308：手动还币309：自动还币312：自动折抵318：闪兑买入319：闪兑卖出320：简单交易买入321：简单交易卖出324：移仓买入325：移仓卖出326：移仓开多327：移仓开空328：移仓平多329：移仓平空332：逐仓杠杆仓位转入保证金333：逐仓杠杆仓位转出保证金334：逐仓杆仓位保证金平仓消耗355：结算盈亏376：质押借币超限买入377： 质押借币超限卖出381：自动出借利息转入372：策略空投转入373：策略空投转出374：策略空投回收转入375：策略空投回收转出381：自动赚币（自动借出） |
| after | String | 否 | 请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId |
| before | String | 否 | 请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId |
| begin | String | 否 | 筛选的开始时间戳ts，Unix 时间戳为毫秒数格式，如 1597026383085 |
| end | String | 否 | 筛选的结束时间戳ts，Unix 时间戳为毫秒数格式，如 1597027383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| billId | String | 账单ID |
| type | String | 账单类型 |
| subType | String | 账单子类型 |
| ts | String | 余额更新完成的时间，Unix时间戳的毫秒数格式，如1597026383085 |
| balChg | String | 账户层面的余额变动数量 |
| posBalChg | String | 仓位层面的余额变动数量 |
| bal | String | 账户层面的余额数量 |
| posBal | String | 仓位层面的余额数量 |
| sz | String | 数量对于交割、永续以及期权，为成交或者持仓的数量，单位为张，总为正数。其他情况下，单位为账户余额币种（ccy）。 |
| px | String | 价格，与 subType 相关为成交价格时有1：买入2：卖出3：开多4：开空5：平多6：平空204：大宗交易买205：大宗交易卖206：大宗交易开多207：大宗交易开空208：大宗交易平多209：大宗交易平空114：自动换币买入115：自动换币卖出为强平价格时有100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出16：强制还币17：强制借币还息110：强平换币转入111：强平换币转出为交割价格时有112：交割平多113：交割平空为行权价格时有170：到期行权171：到期被行权172：到期作废为标记价格时有173：资金费支出174：资金费收入 |
| ccy | String | 账户余额币种 |
| pnl | String | 收益 |
| fee | String | 手续费正数代表平台返佣 ，负数代表平台扣除手续费规则 |
| earnAmt | String | 自动赚币数量仅适用于type 381 |
| earnApr | String | 自动赚币实际年利率仅适用于type 381 |
| mgnMode | String | 保证金模式isolated：逐仓cross：全仓cash：非保证金如果账单不是由交易产生的，该字段返回 "" |
| instId | String | 产品ID，如BTC-USDT |
| ordId | String | 订单ID当type为2/5/9时，返回相应订单id无订单时，该字段返回 "" |
| execType | String | 流动性方向T：takerM：maker |
| from | String | 转出账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 "" |
| to | String | 转入账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 "" |
| notes | String | 备注 |
| interest | String | 利息 |
| tag | String | 订单标签字母（区分大小写）与数字的组合，可以是纯字母、纯数字，且长度在1-16位之间。 |
| fillTime | String | 最新成交时间 |
| tradeId | String | 最新成交ID |
| clOrdId | String | 客户自定义订单ID |
| fillIdxPx | String | 交易执行时的指数价格 d对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例如 LTC-ETH，该字段返回 LTC-USDT 的指数价格。 |
| fillMarkPx | String | 成交时的标记价格，仅适用于交割/永续/期权 |
| fillPxVol | String | 成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillPxUsd | String | 成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串"" |
| fillMarkVol | String | 成交时的标记波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillFwdPx | String | 成交时的远期价格，仅适用于期权，其他业务线返回空字符串"" |



---

## 账单流水查询（近三个月）

帐户资产流水是指导致帐户余额增加或减少的行为。本接口可以查询最近 3 个月的账单数据。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/bills-archive


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instId | String | 否 | 产品ID，如BTC-USDT |
| ccy | String | 否 | 账单币种 |
| mgnMode | String | 否 | 仓位类型isolated：逐仓cross：全仓 |
| ctType | String | 否 | 合约类型linear：正向合约inverse：反向合约仅交割/永续有效 |
| type | String | 否 | 账单类型1：划转2：交易3：交割4：自动换币5：强平6：保证金划转7：扣息8：资金费9：自动减仓10：穿仓补偿11：系统换币12：策略划拨13：对冲减仓14：大宗交易15：一键借币16：借币22：一键还债24：价差交易26：结构化产品27：闪兑28：小额兑换29：一键还债30：简单交易32：移仓33：借贷34：结算250：跟单人分润支出251：跟单人分润退还 |
| subType | String | 否 | 账单子类型1：买入2：卖出3：开多4：开空5：平多6：平空9：市场借币扣息11：转入12：转出14：尊享借币扣息160：手动追加保证金161：手动减少保证金162：自动追加保证金114：自动换币买入115：自动换币卖出118：系统换币转入119：系统换币转出100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出108：穿仓补偿110：强平换币转入111：强平换币转出125：自动减仓平多126：自动减仓平空127：自动减仓买入128：自动减仓卖出131：对冲买入132：对冲卖出170：到期行权（实值期权买方）171：到期被行权（实值期权卖方）172：到期作废（非实值期权的买方和卖方）112：交割平多 （适用于FUTURES过期和SWAP下线）113：交割平空 （适用于FUTURES过期和SWAP下线）117：交割/行权穿仓补偿173：资金费支出174：资金费收入200：系统转入201：手动转入202：系统转出203：手动转出204：大宗交易买205：大宗交易卖206：大宗交易开多207：大宗交易开空208：大宗交易平多209：大宗交易平空210：一键借币的手动借币211：一键借币的手动还币212：一键借币的自动借币213：一键借币的自动还币220：USDT 买期权转入221：USDT 买期权转出16：强制还币17：强制借币还息224：一键还债买入225：一键还债卖出236：小额兑换买入237：小额兑换卖出250：永续分润支出251：永续分润退还280：现货分润支出281：现货分润退还282：现货分润收入283：现货跟单资产划转284：跟单自动转入285：跟单手动转入286：跟单自动转出287：跟单手动转出270：价差交易买271：价差交易卖272：价差交易开多273：价差交易开空274：价差交易平多275：价差交易平空290：系统转出小额资产293：固定借币扣息294：固定借币利息退款295：固定借币逾期利息296：结构化下单转出297：结构化下单转入298：结构化结算转出299：结构化结算转入306：手动借币307：自动借币308：手动还币309：自动还币312：自动折抵318：闪兑买入319：闪兑卖出320：简单交易买入321：简单交易卖出324：移仓买入325：移仓卖出326：移仓开多327：移仓开空328：移仓平多329：移仓平空332：逐仓杠杆仓位转入保证金333：逐仓杠杆仓位转出保证金334：逐仓杆仓位保证金平仓消耗355：结算盈亏376：质押借币超限买入377： 质押借币超限卖出381：自动出借利息转入372：策略空投转入373：策略空投转出374：策略空投回收转入375：策略空投回收转出381：自动赚币（自动借出） |
| after | String | 否 | 请求此id之前（更旧的数据）的分页内容，传的值为对应接口的billId |
| before | String | 否 | 请求此id之后（更新的数据）的分页内容，传的值为对应接口的billId |
| begin | String | 否 | 筛选的开始时间戳ts，Unix 时间戳为毫秒数格式，如1597026383085 |
| end | String | 否 | 筛选的结束时间戳ts，Unix 时间戳为毫秒数格式，如1597027383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| billId | String | 账单ID |
| type | String | 账单类型 |
| subType | String | 账单子类型 |
| ts | String | 余额更新完成的时间，Unix时间戳的毫秒数格式，如1597026383085 |
| balChg | String | 账户层面的余额变动数量 |
| posBalChg | String | 仓位层面的余额变动数量 |
| bal | String | 账户层面的余额数量 |
| posBal | String | 仓位层面的余额数量 |
| sz | String | 数量对于交割、永续以及期权，为成交或者持仓的数量，单位为张，总为正数。其他情况下，单位为账户余额币种（ccy）。 |
| px | String | 价格，与 subType 相关为成交价格时有1：买入2：卖出3：开多4：开空5：平多6：平空204：大宗交易买205：大宗交易卖206：大宗交易开多207：大宗交易开空208：大宗交易平多209：大宗交易平空114：自动换币买入115：自动换币卖出为强平价格时有100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出16：强制还币17：强制借币还息110：强平换币转入111：强平换币转出为交割价格时有112：交割平多113：交割平空为行权价格时有170：到期行权171：到期被行权172：到期作废为标记价格时有173：资金费支出174：资金费收入 |
| ccy | String | 账户余额币种 |
| pnl | String | 收益 |
| fee | String | 手续费正数代表平台返佣 ，负数代表平台扣除手续费规则 |
| earnAmt | String | 自动赚币数量仅适用于type 381 |
| earnApr | String | 自动赚币实际年利率仅适用于type 381 |
| mgnMode | String | 保证金模式isolated：逐仓cross：全仓cash：非保证金如果账单不是由交易产生的，该字段返回 "" |
| instId | String | 产品ID，如BTC-USDT |
| ordId | String | 订单ID当type为2/5/9时，返回相应订单id无订单时，该字段返回 "" |
| execType | String | 流动性方向T：takerM：maker |
| from | String | 转出账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 "" |
| to | String | 转入账户6：资金账户18：交易账户仅适用于资金划转，不是资金划转时，返回 "" |
| notes | String | 备注 |
| interest | String | 利息 |
| tag | String | 订单标签 |
| fillTime | String | 最新成交时间 |
| tradeId | String | 最新成交ID |
| clOrdId | String | 客户自定义订单ID |
| fillIdxPx | String | 交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例 LTC-ETH，该字段返回 LTC-USDT 的指数价格。 |
| fillMarkPx | String | 成交时的标记价格，仅适用于交割/永续/期权 |
| fillPxVol | String | 成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillPxUsd | String | 成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串"" |
| fillMarkVol | String | 成交时的标记波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillFwdPx | String | 成交时的远期价格，仅适用于期权，其他业务线返回空字符串"" |



---

## 申请账单流水（自 2021 年）

申请自 2021 年 2 月 1 日以来的账单数据，不包括当前季度。


### 限速：12 次/天


### 限速规则：User ID


### 权限：读取


### HTTP 请求

POST /api/v5/account/bills-history-archive


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| year | String | 是 | 4位数字的年份，如2023 |
| quarter | String | 是 | 季度，有效值Q1Q2Q3Q4 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| result | String | 是否已经存在该区间的下载链接true：已存在，可以通过"获取账单流水（自 2021 年）"接口获取false：不存在，正在生成，请 2 个小时后查看下载链接 |
| ts | String | 服务端首次收到请求的时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 获取账单流水（自 2021 年）

获取自 2021 年 2 月 1 日以来的账单数据


### 限速：10 次/2s


### 限速规则：User ID


### 权限：读取


### HTTP 请求

GET /api/v5/account/bills-history-archive


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| year | String | 是 | 4位数字的年份，如2023 |
| quarter | String | 是 | 季度，有效值Q1Q2Q3Q4 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| fileHref | String | 文件链接。每个链接的有效期为 5 个半小时，如果已经申请过同一季度的数据，则30天内无需再次申请。 |
| ts | String | 服务端首次收到请求的时间，Unix时间戳的毫秒数格式 ，如1597026383085 |
| state | String | 下载链接状态finished：已生成ongoing：进行中failed：生成失败，请重新生成 |



### 解压后CSV里的字段说明



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instType | String | 产品类型 |
| billId | String | 账单ID |
| subType | String | 账单子类型 |
| ts | String | 余额更新完成的时间，Unix时间戳的毫秒数格式，如1597026383085 |
| balChg | String | 账户层面的余额变动数量 |
| posBalChg | String | 仓位层面的余额变动数量 |
| bal | String | 账户层面的余额数量 |
| posBal | String | 仓位层面的余额数量 |
| sz | String | 数量 |
| px | String | 价格，与 subType 相关为成交价格时有1：买入2：卖出3：开多4：开空5：平多6：平空204：大宗交易买205：大宗交易卖206：大宗交易开多207：大宗交易开空208：大宗交易平多209：大宗交易平空114：自动换币买入115：自动换币卖出为强平价格时有100：强减平多101：强减平空102：强减买入103：强减卖出104：强平平多105：强平平空106：强平买入107：强平卖出16：强制还币17：强制借币还息110：强平换币转入111：强平换币转出为交割价格时有112：交割平多113：交割平空为行权价格时有170：到期行权171：到期被行权172：到期作废为标记价格时有173：资金费支出174：资金费收入 |
| ccy | String | 账户余额币种 |
| pnl | String | 收益 |
| fee | String | 手续费正数代表平台返佣 ，负数代表平台扣除手续费规则 |
| mgnMode | String | 保证金模式isolated：逐仓cross：全仓cash：非保证金如果账单不是由交易产生的，该字段返回 "" |
| instId | String | 产品ID，如BTC-USDT |
| ordId | String | 订单ID无订单时，该字段返回 "" |
| execType | String | 流动性方向T：takerM：maker |
| interest | String | 利息 |
| tag | String | 订单标签 |
| fillTime | String | 最新成交时间 |
| tradeId | String | 最新成交ID |
| clOrdId | String | 客户自定义订单ID |
| fillIdxPx | String | 交易执行时的指数价格对于交叉现货币对，返回 baseCcy-USDT 的指数价格。 例 LTC-ETH，该字段返回 LTC-USDT 的指数价格。 |
| fillMarkPx | String | 成交时的标记价格，仅适用于交割/永续/期权 |
| fillPxVol | String | 成交时的隐含波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillPxUsd | String | 成交时的期权价格，以USD为单位，仅适用于期权，其他业务线返回空字符串"" |
| fillMarkVol | String | 成交时的标记波动率，仅适用于期权，其他业务线返回空字符串"" |
| fillFwdPx | String | 成交时的远期价格，仅适用于期权，其他业务线返回空字符串"" |



---

## 查看账户配置

查看当前账户的配置信息。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/config


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| uid | String | 当前请求的账户ID，账户uid和app上的一致 |
| mainUid | String | 当前请求的母账户ID如果 uid = mainUid，代表当前账号为母账户；如果 uid != mainUid，代表当前账户为子账户。 |
| acctLv | String | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |
| acctStpMode | String | 账户自成交保护模式cancel_maker：撤销挂单cancel_taker：撤销吃单cancel_both：撤销挂单和吃单默认为cancel_maker，用户可通过母账户登录网页修改该配置 |
| posMode | String | 持仓方式long_short_mode：开平仓模式net_mode：买卖模式仅适用交割/永续 |
| autoLoan | Boolean | 是否自动借币true：自动借币false：非自动借币 |
| greeksType | String | 当前希腊字母展示方式PA：币本位BS：美元本位 |
| feeType | String | 手续费类型0：手续费以获取币种收取1：手续费以计价币种收取 |
| level | String | 当前在平台上真实交易量的用户等级，如Lv1，代表普通用户等级。 |
| levelTmp | String | 特约用户的临时体验用户等级，如Lv1 |
| ctIsoMode | String | 衍生品的逐仓保证金划转模式automatic：开仓划转autonomy：自主划转 |
| spotOffsetType | String | 现货对冲类型1：现货对冲模式U模式2：现货对冲模式币模式3：非现货对冲模式适用于组合保证金模式已废弃 |
| stgyType | String | 策略类型0：普通策略模式1：delta 中性策略模式 |
| roleType | String | 用户角色0：普通用户1：带单者2：跟单者 |
| traderInsts | Array of strings | 当前账号已经设置的带单合约，仅适用于带单者 |
| spotRoleType | String | 现货跟单角色。0：普通用户；1：带单者；2：跟单者 |
| spotTraderInsts | Array of strings | 当前账号已经设置的带单币对，仅适用于带单者 |
| opAuth | String | 是否开通期权交易0：未开通1：已经开通 |
| kycLv | String | 母账户KYC等级0: 未认证1: 已完成 level 1 认证2: 已完成 level 2 认证3: 已完成 level 3认证如果请求来自子账户, kycLv 为其母账户的等级如果请求来自母账户, kycLv 为当前请求的母账户等级 |
| label | String | 当前请求API key的备注名，不超过50位字母（区分大小写）或数字，可以是纯字母或纯数字。 |
| ip | String | 当前请求API key绑定的ip地址，多个ip用半角逗号隔开，如：117.37.203.58,117.37.203.57。如果没有绑定ip，会返回空字符串"" |
| perm | String | 当前请求的 API key 或 Access token 的权限read_only：读取trade：交易withdraw：提币 |
| liquidationGear | String | 强平提醒的维持保证金率水平3和-1代表维持保证金率达到 300% 时，每隔 1 小时 app 和 ”爆仓风险预警推送频道“会推送通知。-1是初始值，与-3有着同样效果0代表不提醒 |
| enableSpotBorrow | Boolean | 现货模式下是否支持借币true：支持false：不支持 |
| spotBorrowAutoRepay | Boolean | 现货模式下是否支持自动还币true：支持false：不支持 |
| type | String | 账户类型0：母账户1：普通子账户2：资管子账户5：托管交易子账户 - Copper9：资管交易子账户 - Copper12：托管交易子账户 - Komainu |
| settleCcy | String | 当前账户的 USD 本位合约结算币种 |
| settleCcyList | String | 当前账户的 USD 本位合约结算币种列表，如 ["USD", "USDC", "USDG"]。 |



---

## 设置持仓模式

合约模式和跨币种保证金模式：交割和永续合约支持开平仓模式和买卖模式。买卖模式只会有一个方向的仓位；开平仓模式可以分别持有多、空2个方向的仓位。组合保证金模式：交割和永续仅支持买卖模式


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-position-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| posMode | String | 是 | 持仓方式long_short_mode：开平仓模式net_mode：买卖模式仅适用交割/永续 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| posMode | String | 持仓方式 |



---

## 设置杠杆倍数

一个产品可以有如下10种杠杆倍数的设置场景：

注意请求参数 posSide 仅在交割/永续的开平仓持仓模式下才需要填写（参见场景8和11）。请参阅右侧对应的每个案例的请求示例。


### 限速：20次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-leverage


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 可选 | 产品ID：币对、合约仅适用于现货模式/跨币种保证金模式/组合保证金模式的全仓交割永续，合约模式的全仓币币杠杆交割永续以及逐仓。且在适用场景下必填。 |
| ccy | String | 可选 | 保证金币种，用于设置开启自动借币模式下币种维度的杠杆。仅适用于现货模式/跨币种保证金模式/组合保证金模式的全仓币币杠杆。且在适用场景下必填。 |
| lever | String | 是 | 杠杆倍数 |
| mgnMode | String | 是 | 保证金模式isolated：逐仓cross：全仓如果ccy有效传值，该参数值只能为cross。 |
| posSide | String | 可选 | 持仓方向long：开平仓模式开多short：开平仓模式开空仅适用于逐仓交割/永续在开平仓模式且保证金模式为逐仓条件下必填 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| lever | String | 杠杆倍数 |
| mgnMode | String | 保证金模式isolated：逐仓cross：全仓 |
| instId | String | 产品ID |
| posSide | String | 持仓方向 |



---

## 获取最大可下单数量

获取最大可下单数量，可对应下单时的 "sz" 字段


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-size


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT支持同一业务线下的多产品ID查询（不超过5个），半角逗号分隔 |
| tdMode | String | 是 | 交易模式cross：全仓isolated：逐仓cash：非保证金spot_isolated：现货逐仓，仅适用于合约模式 |
| ccy | String | 可选 | 保证金币种，适用于逐仓杠杆及合约模式下的全仓杠杆订单 |
| px | String | 否 | 委托价格当不填委托价时，交割和永续会取当前限价计算，其他业务线会按当前最新成交价计算当指定多个产品ID查询时，忽略该参数，当未填写处理 |
| leverage | String | 否 | 开仓杠杆倍数默认为当前杠杆倍数仅适用于币币杠杆/交割/永续 |
| tradeQuoteCcy | String | 否 | 用于交易的计价币种。仅适用于币币。默认值为instId的计价币种，比如：对于BTC-USD，默认取USD。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| ccy | String | 保证金币种 |
| maxBuy | String | 币币/币币杠杆：最大可买的交易币数量合约模式下的全仓杠杆订单，为交易币数量交割/永续/期权：最大可开多的合约张数 |
| maxSell | String | 币币/币币杠杆：最大可卖的计价币数量合约模式下的全仓杠杆订单，为交易币数量交割/永续/期权：最大可开空的合约张数 |



---

## 获取最大可用余额/保证金

币币和逐仓时为可用余额，全仓时为可用保证金


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-avail-size


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔 |
| tdMode | String | 是 | 交易模式cross：全仓isolated：逐仓cash：非保证金spot_isolated：现货逐仓，仅适用于合约模式 |
| ccy | String | 可选 | 保证金币种，适用于逐仓杠杆及合约模式下的全仓杠杆 |
| reduceOnly | Boolean | 否 | 是否为只减仓模式，仅适用于币币杠杆 |
| px | String | 否 | 平仓价格，默认为市价。仅适用于杠杆只减仓 |
| tradeQuoteCcy | String | 否 | 用于交易的计价币种。仅适用于币币。默认值为instId的计价币种，比如：对于BTC-USD，默认取USD。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| availBuy | String | 最大买入可用余额/保证金 |
| availSell | String | 最大卖出可用余额/保证金 |



---

## 调整保证金

增加或者减少逐仓保证金。减少保证金可能会导致实际杠杆倍数发生变化。


### 限速：20次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/position/margin-balance


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID |
| posSide | String | 是 | 持仓方向，默认值是netlong：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| type | String | 是 | 增加/减少保证金add：增加reduce：减少 |
| amt | String | 是 | 增加或减少的保证金数量 |
| ccy | String | 可选 | 增加或减少的保证金的币种，适用于逐仓杠杆仓位 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| posSide | String | 持仓方向 |
| amt | String | 已增加/减少的保证金数量 |
| type | String | 增加/减少保证金 |
| leverage | String | 调整保证金后的实际杠杆倍数 |
| ccy | String | 增加或减少的保证金的币种 |



---

## 获取杠杆倍数


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/leverage-info


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 可选 | 产品ID支持多个instId查询，半角逗号分隔。instId个数不超过20个。 |
| ccy | String | 可选 | 币种，用于币种维度的杠杆。仅适用于现货模式/跨币种保证金模式/组合保证金模式的全仓币币杠杆。支持多ccy查询，半角逗号分隔。ccy个数不超过20个。 |
| mgnMode | String | 是 | 保证金模式isolated：逐仓cross：全仓 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| ccy | String | 币种，用于币种维度的杠杆。仅适用于现货模式/跨币种保证金模式/组合保证金模式的全仓币币杠杆。 |
| mgnMode | String | 保证金模式 |
| posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式开平仓模式下会返回两个方向的杠杆倍数 |
| lever | String | 杠杆倍数 |



---

## 获取杠杆倍数预估信息

获取指定杠杆倍数下，相关的预估信息。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/adjust-leverage-info


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约 |
| mgnMode | String | 是 | 保证金模式isolated：逐仓cross：全仓 |
| lever | String | 是 | 杠杆倍数 |
| instId | String | 可选 | 产品ID，如BTC-USDT必填的场景有：交割永续，逐仓杠杆，以及合约模式下全仓杠杆。 |
| ccy | String | 可选 | 保证金币种，如BTC逐仓杠杆及合约模式/跨币种保证金模式/组合保证金模式的全仓杠杆时必填。 |
| posSide | String | 否 | 持仓方向net: 默认值，代表买卖模式long: 开平模式下的多仓short：开平模式下的空仓适用于交割/永续。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| estAvailQuoteTrans | String | 对应杠杆倍数下，计价货币预估可转出的保证金数量全仓时，为交易账户最大可转出逐仓时，为逐仓仓位可减少的保证金。仅适用于杠杆 |
| estAvailTrans | String | 对应杠杆倍数下，预估可转出的保证金数量全仓时，为交易账户最大可转出逐仓时，为逐仓仓位可减少的保证金对于杠杆，单位为交易货币不适用于交割,永续的逐仓，调大杠杆的场景 |
| estLiqPx | String | 对应杠杆倍数下的预估强平价，仅在有仓位时有值 |
| estMgn | String | 对应杠杆倍数下，仓位预估所需的保证金数量对于杠杆仓位，为所需交易货币保证金对于交割或永续仓位，为仓位所需保证金 |
| estQuoteMgn | String | 对应杠杆倍数下，仓位预估所需的计价货币保证金数量 |
| estMaxAmt | String | 对于杠杆，为对应杠杆倍数下，交易货币预估最大可借对于交割和永续，为对应杠杆倍数下，预估的最大可开张数 |
| estQuoteMaxAmt | String | 对应杠杆倍数下，杠杆计价货币预估最大可借 |
| existOrd | Boolean | 当前是否存在挂单true：存在挂单false：不存在挂单 |
| maxLever | String | 最大杠杆倍数 |
| minLever | String | 最小杠杆倍数 |



---

## 获取交易产品最大可借


### 限速：20 次/2s


### 限速规则：User ID


### 权限：读取


### HTTP 请求

GET /api/v5/account/max-loan


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| mgnMode | String | 是 | 仓位类型isolated：逐仓cross：全仓 |
| instId | String | 可选 | 产品 ID，如BTC-USDT支持多产品ID查询（不超过5个），半角逗号分隔 |
| ccy | String | 可选 | 币种仅适用于现货模式下手动借币币种最大可借 |
| mgnCcy | String | 可选 | 保证金币种，如BTC适用于逐仓杠杆及合约模式下的全仓杠杆 |
| tradeQuoteCcy | String | 否 | 用于交易的计价币种。仅适用于币币。默认值为instId的计价币种，比如：对于BTC-USD，默认取USD。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品 ID |
| mgnMode | String | 仓位类型 |
| mgnCcy | String | 保证金币种 |
| maxLoan | String | 最大可借 |
| ccy | String | 币种 |
| side | String | 订单方向 |



---

## 获取当前账户交易手续费费率


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/trade-fee


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型SPOT：币币MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instId | String | 否 | 产品ID，如BTC-USDT仅适用于instType为币币/币币杠杆 |
| instFamily | String | 否 | 交易品种适用于交割/永续/期权，如BTC-USD |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| level | String | 手续费等级 |
| feeGroup | Array of objects | 手续费分组适用于SPOT/MARGIN/SWAP/FUTURES/OPTION |
| > taker | String | 吃单手续费 |
| > maker | String | 挂单手续费 |
| > groupId | String | 交易产品手续费分组ID用户需要同时使用instType和groupId来确定一个交易产品的交易手续费分组；用户应该将此接口和获取交易产品基础信息一起使用，以获取特定交易产品的手续费率 |
| delivery | String | 交割手续费率 |
| exercise | String | 行权手续费率 |
| instType | String | 产品类型 |
| ts | String | 数据返回时间，Unix时间戳的毫秒数格式，如1597026383085 |
| taker | String | 对于币币/杠杆，为 USDT 交易区的吃单手续费率；对于永续，交割和期权合约，为币本位合约费率（已废弃） |
| maker | String | 对于币币/杠杆，为 USDT 交易区的挂单手续费率；对于永续，交割和期权合约，为币本位合约费率（已废弃） |
| takerU | String | USDT 合约吃单手续费率，仅适用于交割/永续（已废弃） |
| makerU | String | USDT 合约挂单手续费率，仅适用于交割/永续（已废弃） |
| takerUSDC | String | 对于币币/杠杆，为 USDⓈ&Crypto 交易区的吃单手续费率；对于永续和交割合约，为 USDC 合约费率（已废弃） |
| makerUSDC | String | 对于币币/杠杆，为 USDⓈ&Crypto 交易区的挂单手续费率；对于永续和交割合约，为 USDC 合约费率（已废弃） |
| ruleType | String | 交易规则类型normal：普通交易pre_market：盘前交易（已废弃） |
| category | String | 币种类别（已废弃） |
| fiat | Array of objects | 法币费率（已废弃） |
| > ccy | String | 法币币种 |
| > taker | String | 吃单手续费率 |
| > maker | String | 挂单手续费率 |



---

## 获取计息记录

获取过去一年的计息记录


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/interest-accrued


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| type | String | 否 | 借币类型2：市场借币默认为2 |
| ccy | String | 否 | 借贷币种，如BTC仅适用于市场借币仅适用于币币杠杆 |
| instId | String | 否 | 产品ID，如BTC-USDT仅适用于市场借币 |
| mgnMode | String | 否 | 保证金模式cross：全仓isolated：逐仓仅适用于市场借币 |
| after | String | 否 | 请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| before | String | 否 | 请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| type | String | 类型2：市场借币 |
| ccy | String | 借贷币种，如BTC |
| instId | String | 产品ID，如BTC-USDT仅适用于市场借币 |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| interest | String | 利息累计 |
| interestRate | String | 借款计息利率(小时) |
| liab | String | 计息负债 |
| totalLiab | String | 当前账户总负债量 |
| interestFreeLiab | String | 当前账户免息负债量 |
| ts | String | 计息时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 获取用户当前市场借币利率


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/interest-rate


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| interestRate | String | 每小时借币利率 |
| ccy | String | 币种 |



---

## 设置手续费计价方式

设置手续费计价方式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP 请求

POST /api/v5/account/set-fee-type


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| feeType | String | 是 | 手续费计价方式0: 按交易获得的币种收取手续费（默认）1: 始终按交易对的计价币种收取手续费（仅适用于现货） |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| feeType | String | 手续费计价方式0: 按交易获得的币种收取手续费1: 始终按交易对的计价币种收取手续费 |



---

## 期权greeks的PA/BS切换

设置greeks的展示方式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-greeks


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| greeksType | String | 是 | 希腊字母展示方式PA：币本位，BS：美元本位 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| greeksType | String | 当前希腊字母展示方式 |



---

## 逐仓交易设置

可以通过该接口设置币币杠杆和交割、永续的逐仓仓位保证金的划转模式


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-isolated-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| isoMode | String | 是 | 逐仓保证金划转模式auto_transfers_ccy：新版开仓自动划转，支持交易货币及计价货币作为保证金，仅适用于币币杠杆automatic：开仓自动划转 |
| type | String | 是 | 业务线类型MARGIN：币币杠杆CONTRACTS：合约 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| isoMode | String | 逐仓保证金划转模式auto_transfers_ccy：新版开仓自动划转automatic：开仓自动划转 |



---

## 查看账户最大可转余额

当指定币种时会返回该币种的交易账户到资金账户的最大可划转数量，不指定币种会返回所有拥有的币种资产可划转数量。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-withdrawal


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| maxWd | String | 最大可划转数量（不包含跨币种保证金模式/组合保证金模式借币金额） |
| maxWdEx | String | 最大可划转数量（包含跨币种保证金模式/组合保证金模式借币金额） |
| spotOffsetMaxWd | String | 现货对冲不支持借币最大可转数量仅适用于组合保证金模式 |
| spotOffsetMaxWdEx | String | 现货对冲支持借币的最大可转数量仅适用于组合保证金模式 |



---

## 查看账户特定风险状态

仅适用于PM账户


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/risk-state


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| atRisk | Boolean | 自动借币模式下的账户风险状态true： 当前账户为特定风险状态false： 当前不是特定风险状态 |
| atRiskIdx | Array of strings | 衍生品的risk unit列表 |
| atRiskMgn | Array of strings | 杠杆的risk unit列表 |
| ts | String | 接口数据返回时间 ，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 获取借币利率与限额


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/interest-limits


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| type | String | 否 | 借币类型2：市场借币默认为2 |
| ccy | String | 否 | 借贷币种，如BTC |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| debt | String | 当前负债，单位为USD |
| interest | String | 当前记息，单位为USD仅适用于市场借币 |
| nextDiscountTime | String | 下次扣息时间，Unix时间戳的毫秒数格式，如1597026383085 |
| nextInterestTime | String | 下次计息时间，Unix时间戳的毫秒数格式，如1597026383085 |
| loanAlloc | String | 当前交易账户尊享借币可用额度的比率（百分比）1. 范围为[0, 100]. 精度为 0.01% (2位小数)2. 0 代表母账户没有为子账户分配；3. "" 代表母子账户共享已废弃 |
| records | Array of objects | 各币种详细信息 |
| > ccy | String | 借贷币种，如BTC |
| > rate | String | 当前日借币利率 |
| > loanQuota | String | 母账户维度借币限额如果已配置可用额度，该字段代表当前交易账户的借币限额 |
| > usedLmt | String | 当前账户已借额度如果已配置可用额度，该字段代表当前交易账户的已借额度 |
| > interest | String | 已计未扣利息仅适用于市场借币 |
| > interestFreeLiab | String | 当前账户免息负债 |
| > potentialBorrowingAmt | String | 当前账户潜在借币量 |
| > surplusLmt | String | 母子账户剩余可借如果已配置可用额度，该字段代表当前交易账户的剩余可借 |
| > surplusLmtDetails | Object | 母子账户剩余可借额度详情，母子账户剩余可借额度的值取该数组中的最小值，可以用来判断是什么原因导致可借额度不足仅适用于尊享借币已废弃 |
| >> allAcctRemainingQuota | String | 母子账户剩余额度 |
| >> curAcctRemainingQuota | String | 当前账户剩余额度仅适用于为子账户分配限额的场景 |
| >> platRemainingQuota | String | 平台剩余额度，当平台剩余额度大于curAcctRemainingQuota或者allAcctRemainingQuota时，会显示大于某个值，如">1000" |
| > posLoan | String | 当前账户负债占用（锁定额度内）仅适用于尊享借币已废弃 |
| > availLoan | String | 当前账户剩余可用（锁定额度内）仅适用于尊享借币已废弃 |
| > usedLoan | String | 当前账户已借额度仅适用于尊享借币已废弃 |
| > avgRate | String | 已借币种平均每小时利率，仅适用于尊享借币已废弃 |



---

## 手动借/还币

仅适用于现货模式已开通借币的情况。


### 限速：1次/3s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/spot-manual-borrow-repay


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| side | String | 是 | 方向borrow：借币repay：还币 |
| amt | String | 是 | 数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种，如BTC |
| side | String | 方向borrow：借币repay：还币 |
| amt | String | 实际数量 |



---

## 设置自动还币

仅适用于现货模式已开通借币的情况。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-auto-repay


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| autoRepay | Boolean | 是 | 是否支持现货模式下自动还币true：支持false：不支持 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| autoRepay | Boolean | 是否支持现货模式下自动还币true：支持false：不支持 |



---

## 获取借/还币历史

获取现货模式下的借/还币历史。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/spot-borrow-repay-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC |
| type | String | 否 | 事件类型auto_borrow：自动借币auto_repay：自动还币manual_borrow：手动借币manual_repay：手动还币 |
| after | String | 否 | 请求发生时间ts之前（包含）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| before | String | 否 | 请求发生时间ts之后（包含）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 返回结果的数量，最大为100，默认100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种，如BTC |
| type | String | 事件类型auto_borrow：自动借币auto_repay：自动还币manual_borrow：手动借币manual_repay：手动还币 |
| amt | String | 数量 |
| accBorrowed | String | 累计借币数量 |
| ts | String | 事件发生时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 仓位创建器

计算用户的模拟头寸或当前头寸的投资组合保证金信息，一次请求最多可添加200个虚拟仓位和200个虚拟虚拟资产


### 限速：2次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

POST /api/v5/account/position-builder


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 否 | 切换至账户模式3：跨币种保证金模式4：组合保证金模式 |
| inclRealPosAndEq | Boolean | 否 | 是否代入已有仓位和资产默认为true |
| lever | String | 否 | 跨币种下整体的全仓合约杠杆数量，默认为1。如果超过允许的杠杆倍数，按照最大的杠杆设置。适用于跨币种保证金模式 |
| simPos | Array of objects | 否 | 模拟仓位列表 |
| > instId | String | 是 | 交易产品ID，如BTC-USDT-SWAP适用于SWAP/FUTURES/OPTION |
| > pos | String | 是 | 持仓量 |
| > avgPx | String | 是 | 平均开仓价格 |
| > lever | String | 否 | 杠杆仅适用于在跨币种保证金模式下指定交易产品的杠杆。如果用户不传，则选择默认杠杆为1。 |
| simAsset | Array of objects | 否 | 模拟资产当inclRealPosAndEq为true，只考虑真实资产，会忽略虚拟资产 |
| > ccy | String | 是 | 币种，如BTC |
| > amt | String | 是 | 币种数量可以为负，代表减少币种资产 |
| greeksType | String | 否 | 希腊值类型BS：BS模型PA：币本位CASH：美元现金等价默认是BS |
| idxVol | String | 否 | 价格变动百分比。小数形式，范围 -0.99 ~ 1，以 0.01 为增量。默认值为 0 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| eq | String | 账户有效保证金 |
| totalMmr | String | 账户维持保证金，单位为USD |
| totalImr | String | 账户初始保证金占用，单位为USD |
| borrowMmr | String | 账户借币维持保证金，单位为USD |
| derivMmr | String | 账户衍生品维持保证金，单位为USD |
| marginRatio | String | 账户全仓维持保证金率 |
| upl | String | 账户浮动盈亏 |
| acctLever | String | 账户全仓杠杆 |
| ts | String | 账户信息的更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| assets | Array of objects | 资产信息 |
| > ccy | String | 币种，如BTC |
| > availEq | String | 币种权益 |
| > spotInUse | String | 现货对冲占用 |
| > borrowMmr | String | 借币维持保证金，单位为USD字段已废弃 |
| > borrowImr | String | 借币初始保证金，单位为USD |
| riskUnitData | Array of objects | Risk unit 相关信息适用于组合保证金模式 |
| > riskUnit | String | 账户内的 risk unit，如BTC |
| > mmrBf | String | 价格变动前 Risk unit 维度的维持保证金，单位为USD若用户没有传入idxVol，则返回 "" |
| > mmr | String | Risk unit 维度的维持保证金，单位为USD |
| > imrBf | String | 价格变动前 Risk unit 维度的初始保证金，单位为USD若用户没有传入idxVol，则返回 "" |
| > imr | String | Risk unit 维度的初始保证金，单位为USD |
| > upl | String | Risk unit 维度的浮动盈亏，单位为USD |
| > mr1 | String | 现货和波动率变化风险 (适用于所有衍生品，以及在现货对冲模式下的现货) |
| > mr2 | String | 时间价值风险 (仅适用于期权) |
| > mr3 | String | 波动率跨期风险 (仅适用于期权) |
| > mr4 | String | 基差风险 (适用于所有衍生品) |
| > mr5 | String | 利率风险 (仅适用于期权) |
| > mr6 | String | 极端市场波动风险 (适用于所有衍生品，以及在现货对冲模式下的现货) |
| > mr7 | String | 减仓成本 (适用于所有衍生品) |
| > mr8 | String | 借币维持保证金/初始保证金 |
| > mr9 | String | USDT-USDC-USD 对冲风险 |
| > mr1Scenarios | Object of objects | MR1 的压力测试场景分析 |
| >> volShockDown | Object | 波动率向下时，不同价格波动比率下的压力测试盈亏值为 {change:value, ...}change：价格波动比率（百分比），如0.01代表1%value：压力测试下的盈亏，单位为USD如 {"-0.15":"-2333.23", ...} |
| >> volSame | Object | 波动率不变时，不同价格波动比率下的压力测试盈亏值为 {change:value, ...}change：价格波动比率（百分比），如0.01代表1%value：压力测试下的盈亏，单位为USD如 {"-0.15":"-2333.23", ...} |
| >> volShockUp | Object | 波动率向上时，不同价格波动比率下的压力测试盈亏值为 {change:value, ...}change：价格波动比率（百分比），如0.01代表1%value：压力测试下的盈亏，单位为USD如 {"-0.15":"-2333.23", ...} |
| > mr1FinalResult | Object | MR1 最大亏损场景 |
| >> pnl | String | MR1 最大亏损压测盈亏，单位为USD |
| >> spotShock | String | MR1 最大亏损的价格波动（百分比），如0.01代表1% |
| >> volShock | String | MR1 最大亏损波动率趋势down：波动率向下unchange：波动率不变up：波动率向上 |
| > mr6FinalResult | Object | MR6 最大亏损场景 |
| >> pnl | String | MR6 最大亏损压测盈亏，单位为USD |
| >> spotShock | String | MR6 最大亏损的价格波动（百分比），如0.01代表1% |
| > delta | String | (Risk unit 维度) 合约价格随标的价格变动的比例当标的价格变动 x 时，合约价格变动约为此 Delta 数值乘以 x |
| > gamma | String | (Risk unit 维度) 标的价格对 Delta 值的影响程度当标的价格变动 x% 时，期权 Delta 值的变动约为此 Gamma 数值乘以 x% |
| > theta | String | (Risk unit 维度) 距离到期日时间缩短 1 天，该合约价格的变化量 |
| > vega | String | (Risk unit 维度) 标的波动率增加 1%，该合约价格的变化量 |
| > portfolios | Array of objects | 资产组合 |
| >> instId | String | 产品ID，如BTC-USDT-SWAP |
| >> instType | String | 产品类型SPOT：现货SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| >> amt | String | instType为SPOT，代表现货对冲占用instType为SWAP/FUTURES/OPTION，代表仓位数量。 |
| >> posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| >> avgPx | String | 平均开仓价格 |
| >> markPxBf | String | 价格变动前标记价格若用户没有传入idxVol，则返回 "" |
| >> markPx | String | 标记价格 |
| >> floatPnl | String | 浮动盈亏 |
| >> notionalUsd | String | 美金价值 |
| >> delta | String | instType为SPOT，代表资产数量。instType为SWAP/FUTURES/OPTION，代表(产品层面) 合约价格随标的价格变动的比例。 |
| >> gamma | String | (产品层面) 标的价格对 Delta 值的影响程度instType为SPOT，返回"" |
| >> theta | String | (产品层面) 距离到期日时间缩短 1 天，该合约价格的变化量instType为SPOT，返回"" |
| >> vega | String | (产品层面) 标的波动率增加 1%，该合约价格的变化量instType为SPOT，返回"" |
| >> isRealPos | Boolean | 是否为真实仓位instType为SWAP/FUTURES/OPTION，该字段有效，其他都默认返回false |
| positions | Array of objects | 仓位信息适用于跨币种保证金模式 |
| > instId | String | 产品ID，如BTC-USDT-SWAP |
| > instType | String | 产品类型SPOT：现货SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| > amt | String | instType为SPOT，代表现货对冲占用instType为SWAP/FUTURES/OPTION，代表仓位数量。 |
| > posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| > avgPx | String | 平均开仓价格 |
| > markPxBf | String | 价格变动前标记价格若用户没有传入idxVol，则返回 "" |
| > markPx | String | 标记价格 |
| > floatPnl | String | 浮动盈亏 |
| > imrBf | String | 价格变动前初始保证金 |
| > imr | String | 初始保证金，仅适用于全仓 |
| > mgnRatio | String | 维持保证金率 |
| > lever | String | 杠杆倍数 |
| > notionalUsd | String | 美金价值 |
| > isRealPos | Boolean | 是否为真实仓位instType为SWAP/FUTURES/OPTION，该字段有效，其他都默认返回false |



---

## 仓位创建器趋势图


### 限速：1次/5s


### 限速规则：User ID


### 权限：读取


### HTTP请求

POST /api/v5/account/position-builder-graph


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| inclRealPosAndEq | Boolean | 否 | 是否代入已有仓位和资产默认为true |
| simPos | Array of objects | 否 | 模拟仓位列表 |
| > instId | String | 是 | 交易产品ID，如BTC-USDT-SWAP适用于SWAP/FUTURES/OPTION |
| > pos | String | 是 | 持仓量 |
| > avgPx | String | 是 | 平均开仓价格 |
| > lever | String | 否 | 杠杆仅适用于在跨币种保证金模式下指定交易产品的杠杆。如果用户不传，则选择默认杠杆为1。 |
| simAsset | Array of objects | 否 | 模拟资产当inclRealPosAndEq为true，只考虑真实资产，会忽略虚拟资产 |
| > ccy | String | 是 | 币种，如BTC |
| > amt | String | 是 | 币种数量可以为负，代表减少币种资产 |
| type | String | 是 | 趋势图类型mmr |
| mmrConfig | Object | 是 | MMR配置 |
| > acctLv | String | 否 | 切换至账户模式3：跨币种保证金模式4：组合保证金模式 |
| > lever | String | 否 | 跨币种下整体的全仓合约杠杆数量，默认为1。如果超过允许的杠杆倍数，按照最大的杠杆设置。适用于跨币种保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| type | String | 趋势图类型mmr |
| mmrData | Array | MMR数据以shockFactor升序返回 |
| > shockFactor | String | 价格变动比例，数据范围 -1 到 1. |
| > mmr | String | 维持保证金 |
| > mmrRatio | String | 维持保证金率 |



---

## 设置现货对冲占用

用户自定义现货对冲占用数量，不代表实际现货对冲占用数量。仅适用于组合保证金模式。


### 限速：10次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-riskOffset-amt


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| clSpotInUseAmt | String | 是 | 用户自定义现货对冲数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种，如BTC |
| clSpotInUseAmt | String | 用户自定义现货对冲数量 |



---

## 查看账户Greeks

获取账户资产的greeks信息。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/greeks


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| deltaBS | String | 美金本位账户资产delta |
| deltaPA | String | 币本位账户资产delta |
| gammaBS | String | 美金本位账户资产gamma，仅适用于期权 |
| gammaPA | String | 币本位账户资产gamma，仅适用于期权 |
| thetaBS | String | 美金本位账户资产theta，仅适用于期权 |
| thetaPA | String | 币本位账户资产theta，仅适用于期权 |
| vegaBS | String | 美金本位账户资产vega，仅适用于期权 |
| vegaPA | String | 币本位账户资产vega，仅适用于期权 |
| ccy | String | 币种 |
| ts | String | 获取greeks的时间，Unix时间戳的毫秒数格式，如 1597026383085 |



---

## 获取组合保证金模式仓位限制

仅支持获取组合保证金模式下，交割、永续和期权的全仓仓位限制。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/position-tiers


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instFamily | String | 是 | 交易品种，如BTC-USDT，支持多个查询（不超过5个），instFamily之间半角逗号分隔 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| uly | String | 标的指数适用于交割/永续/期权 |
| instFamily | String | 交易品种适用于交割/永续/期权 |
| maxSz | String | 最大持仓量 |
| posType | String | 限仓类型，仅适用于组合保证金模式下的期权全仓。1：所有合约挂单 + 持仓张数，2：所有合约总挂单张数，3：所有合约总挂单单数，4：同方向合约挂单 + 持仓张数，5：单一合约总挂单单数，6：单一合约挂单 + 持仓张数，7：单笔挂单张数" |



---

## 开通期权交易


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/activate-option


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ts | String | 开通时间 |



---

## 设置自动借币

仅适用于跨币种保证金模式和组合保证金模式


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-auto-loan


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| autoLoan | Boolean | 否 | 是否自动借币有效值为true,false默认为true |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| autoLoan | Boolean | 是否自动借币 |



---

## 预设置账户模式切换

预设置账户模式切换的必要信息，若由组合保证金模式切换到合约模式/跨币种保证金模式，且存在全仓交割、永续仓位，则必须预设置lever，令所有仓位具有相同杠杆倍数。

若用户未按照规定进行设置，在预检查或设置账户模式时将接收到报错或提示信息。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/account-level-switch-preset


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式2: 合约模式3: 跨币种保证金模式4: 组合保证金模式 |
| lever | String | 可选 | 在组合保证金模式向合约模式/跨币种保证金模式切换，且用户有全仓仓位时，必须传入 |
| riskOffsetType | String | 可选 | 风险对冲模式1：现货对冲(USDT)2：现货对冲(币)3：衍生品对冲（未开启现货对冲）4：现货对冲(USDC)适用于合约模式/跨币种保证金模式向组合保证金模式切换（已弃用） |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| curAcctLv | String | 当前账户类型 |
| acctLv | String | 切换后的账户类型 |
| lever | String | 用户预设置的全仓合约仓位杠杆倍数 |
| riskOffsetType | String | 用户预设置的风险对冲模式（已弃用） |



---

## 预检查账户模式切换

获取账户模式切换预检查相关信息


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/set-account-switch-precheck


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式1: 现货模式2: 合约模式3: 跨币种保证金模式4: 组合保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| sCode | String | 校验码0：通过所有验证1：有不兼容信息3：未进行杠杆设置4：梯度档位或保证金校验未通过 |
| curAcctLv | String | 当前账户模式1: 现货模式2: 合约模式3: 跨币种保证金模式4: 组合保证金模式所有情况下均返回 |
| acctLv | String | 新账户模式1: 现货模式2: 合约模式3: 跨币种保证金模式4: 组合保证金模式所有情况下均返回 |
| riskOffsetType | String | 风险对冲模式1：现货对冲(USDT)2：现货对冲(币)3：衍生品对冲4：现货对冲(USDC)acctLv为4时返回，其余情况下返回""若用户有设置，则为用户的设置值；若没有设置，则为默认值（已弃用） |
| unmatchedInfoCheck | Array of objects | 包含不匹配信息对象的列表仅在sCode为1，有不兼容信息时返回，其他情况返回[] |
| >> type | String | 不匹配信息类型asset_validation：资产校验pending_orders：撮合挂单pending_algos：策略挂单，冰山、时间加权、定投等isolated_margin：杠杆逐仓一键借币及自主划转isolated_contract：合约逐仓自主划转contract_long_short：合约开平模式cross_margin：杠杆全仓开仓划转cross_option_buyer：期权全仓买方isolated_option：期权逐仓 （仅适用于简单账户）growth_fund：体验金仓位all_positions：所有仓位spot_lead_copy_only_simple_single：带单和自定义跟单员只能使用现货或合约模式stop_spot_custom：停止现货自定义跟单stop_futures_custom：停止合约自定义跟单lead_portfolio：身为带单员，您不能切换到组合保证金账户模式futures_smart_sync：您存在合约智能跟单，无法切换到现货模式repay_borrowings：存在借币compliance_restriction：合规，无法使用保证金交易相关服务compliance_kyc2：合规，无法使用保证金交易相关服务，如果您不是该地区居民，请进行KYC2身份认证 |
| >> totalAsset | String | 总资产仅在type为asset_validation时返回，其他情况都为"" |
| >> posList | Array of strings | 不匹配仓位列表，返回持仓ID在type为仓位相关枚举值时返回，其他情况都为[] |
| posList | Array of objects | 合约全仓仓位列表适用于curAcctLv为4，acctLv为2/3，且用户具有全仓合约仓位的情况在sCode为0/3/4的情况下返回 |
| > posId | String | 持仓ID |
| > lever | String | 切换后的全仓仓位杠杆倍数 |
| posTierCheck | Array of objects | 未满足梯度档位校验全仓仓位的列表仅在sCode为4时返回 |
| > instFamily | String | 交易品种 |
| > instType | String | 产品类型SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| > pos | String | 持仓量 |
| > lever | String | 杠杆倍数 |
| > maxSz | String | 若acctLv为2/3，目标账户模式为合约、跨币种，则为当前杠杆倍数下的最大持仓张数；若acctLv为4，目标账户模式为组合保证金，则为PM全仓最大持仓量上限 |
| mgnBf | Object | 切换账户模式前的保证金相关信息在sCode为0/4时返回，其他时候为null |
| > acctAvailEq | String | 美金层面可用保证金在curAcctLv为3/4时返回，其他情况返回"" |
| > mgnRatio | String | 美金层面维持保证金率在curAcctLv为3/4时返回，其他情况返回"" |
| > details | Array of objects | 各币种资产详细信息仅在curAcctLv为2时返回，其他情况返回[] |
| >> ccy | String | 币种 |
| >> availEq | String | 币种维度可用保证金 |
| >> mgnRatio | String | 币种维度全仓维持保证金率 |
| mgnAft | Object | 切换账户模式后的保证金相关信息在sCode为0/4时返回，其他时候为null |
| > acctAvailEq | String | 美金层面可用保证金在acctLv为3/4时返回，其他情况返回"" |
| > mgnRatio | String | 美金层面维持保证金率在acctLv为3/4时返回，其他情况返回"" |
| > details | Array of objects | 各币种资产详细信息仅在acctLv为2时返回，其他情况返回"" |
| >> ccy | String | 币种 |
| >> availEq | String | 币种维度可用保证金 |
| >> mgnRatio | String | 币种维度全仓维持保证金率 |



---

## 设置账户模式

账户模式的首次设置，需要在网页或手机app上进行。若用户计划在持有仓位的情况下切换账户模式，应该先调用预设置接口进行必要的预设置，再调用预检查接口获取不匹配信息、保证金校验等相关信息，最后调用账户模式切换接口进行账户模式切换。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-account-level


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式1: 现货模式2: 合约模式3: 跨币种保证金模式4: 组合保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| acctLv | String | 账户模式 |



---

## 设置质押币种


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-collateral-assets


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| type | String | 是 | 设置币种类型all：全部custom：自定义 |
| collateralEnabled | Boolean | 是 | 是否设置为质押币种true：设置为质押币false：取消质押币的设置 |
| ccyList | Array of strings | 可选 | 币种列表，如 ["BTC","ETH"]当type=custom,该字段必传。 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| type | String | 设置币种类型all：全部custom：自定义 |
| collateralEnabled | Boolean | 是否已设置为质押币种true：设置为质押币false：取消质押币的设置 |
| ccyList | Array of strings | 币种列表，如 ["BTC","ETH"] |



---

## 查看质押币种


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/collateral-assets


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种支持多币种查询（不超过20个），币种之间半角逗号分隔，如 "BTC,ETH" |
| collateralEnabled | Boolean | 否 | 是否为质押币 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种，如BTC |
| collateralEnabled | Boolean | 是否为质押币 |



---

## 重置 MMP 状态

一旦 MMP 被触发，可以使用该接口解冻。仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/mmp-reset


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 否 | 交易产品类型OPTION:期权默认为期权 |
| instFamily | String | 是 | 交易品种 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| result | Boolean | 重置结果true:将做市商保护状态重置为了 inactive 状态false：重置失败 |



---

## 设置 MMP

可以使用该接口进行 MMP 的配置。仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。


### 限速：2次/10s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/mmp-config


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instFamily | String | 是 | 交易品种 |
| timeInterval | String | 是 | 时间窗口 (毫秒)。"0" 代表停用 MMP |
| frozenInterval | String | 是 | 冻结时间长度 (毫秒)。"0" 代表一直冻结，直到调用 "重置 MMP 状态" 接口解冻 |
| qtyLimit | String | 是 | 成交数量的上限需大于 0 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |
| timeInterval | String | 时间窗口 (毫秒) |
| frozenInterval | String | 冻结时间长度 (毫秒) |
| qtyLimit | String | 成交张数的上限 |



---

## 查看 MMP 配置

可以使用该接口获取 MMP 的配置信息。仅适用于组合保证金账户模式下的期权订单，且有 MMP 权限。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/mmp-config


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instFamily | String | 否 | 交易品种 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |
| mmpFrozen | Boolean | 是否 MMP 被触发.true或者false |
| mmpFrozenUntil | String | 如果配置了frozenInterval且mmpFrozen = true，则为不再触发MMP时的时间窗口（单位为ms），否则为“” |
| timeInterval | String | 时间窗口 (毫秒) |
| frozenInterval | String | 冻结时间长度 (毫秒)。如果为"0"，代表一直冻结，直到调用 "重置 MMP 状态" 接口解冻，且mmpFrozenUntil为 ""。 |
| qtyLimit | String | 成交张数的上限 |



---

## 移仓

仅适用于交易等级大于等于VIP6的用户，仅能通过母账户的API Key调用。用户可通过我的手续费页面的手续费详情表格查看自己的交易等级。

支持同一母账户下的子账户间仓位划转。每个源账户每24小时最多可触发15次移仓请求，目标账户接受移仓不受次数限制。参考下文“注意事项”部分，以获取详情。


### 限速：1次/1s


### 限速规则：母账户 User ID


### HTTP请求

POST /api/v5/account/move-positions


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| fromAcct | String | 是 | 源账户名，使用"0"代表母账户 |
| toAcct | String | 是 | 目标账户名，使用"0"代表母账户 |
| legs | Array of Objects | 是 | 移仓仓位列表，每次最多支持30个仓位 |
| > from | Object | 是 | 源账户仓位 |
| >> posId | String | 是 | 源账户持仓ID |
| >> sz | String | 是 | 合约数量 |
| >> side | String | 是 | 源账户的交易方向buysell |
| > to | Object | 是 | 目标账户移仓配置 |
| >> tdMode | String | 否 | 目标账户的交易模式cross：全仓isolated：逐仓若未提供，tdMode会采用以下默认值：在合约模式或跨币种保证金模式下买入期权：isolated其他情况：cross |
| >> posSide | String | 否 | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式当目标账户处于买卖模式时，用户不需传入该参数，若传入，唯一有效值为net；当处于开平仓模式时，有效值为long，short，若未指定，目标账户将总是开仓 |
| >> ccy | String | 否 | 目标账户保证金币种仅适用于合约模式下的全仓杠杆仓位 |
| clientId | String | 是 | 客户自定义ID，字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| code | String | 结果代码，0表示成功 |
| msg | String | 错误信息，代码为0时，该字段为空 |
| blockTdId | String | 大宗交易ID |
| clientId | String | 客户自定义ID |
| state | String | 移仓状态，filledfailed |
| fromAcct | String | 源账户名 |
| toAcct | String | 目标账户名 |
| legs | Array | 移仓仓位列表 |
| > from | Object | 源账户仓位 |
| >> instId | String | 产品ID |
| >> posId | String | 持仓ID |
| >> px | String | 移仓价格，过去60分钟的标记价格TWAP |
| >> side | String | 源账户的交易方向buysell |
| >> sz | String | 合约数量 |
| >> sCode | String | 事件执行结果的code，0代表成功 |
| >> sMsg | String | 事件执行失败或成功时的msg |
| > to | Object | 目标账户移仓配置 |
| >> instId | String | 产品ID |
| >> side | String | 目标账户交易方向 |
| >> posSide | String | 目标账户持仓方向 |
| >> tdMode | String | 目标账户的交易模式 |
| >> px | String | 移仓价格，过去60分钟的标记价格TWAP |
| >> ccy | String | 保证金币种 |
| >> sCode | String | 事件执行结果的code，0代表成功 |
| >> sMsg | String | 事件执行失败或成功时的msg |
| ts | String | 移仓请求处理时间戳，Unix时间戳的毫秒数格式，如1597026383085 |



### 注意事项



| 移仓操作 | 账户A总计次数 | 账户B总计次数 | 账户C总计次数 | 账户D总计次数 |
|--------|--------|--------|--------|--------|
| 账户A到账户B | 1 | 0 | 0 | 0 |
| 账户B到账户C | 1 | 1 | 0 | 0 |
| 账户B到账户D | 1 | 2 | 0 | 0 |



---

## 获取移仓历史

仅适用于交易等级大于等于VIP6的用户，仅能通过母账户的API Key调用。用户可通过我的手续费页面的手续费详情表格查看自己的交易等级。

获取过去三天的移仓明细。


### 限速：2次/2s


### 限速规则：母账户 User ID


### HTTP请求

GET /api/v5/account/move-positions-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| blockTdId | String | 否 | 大宗交易ID |
| clientId | String | 否 | 客户自定义ID字母（区分大小写）与数字的组合，可以是纯字母、纯数字且长度要在1-32位之间 |
| beginTs | String | 否 | 用开始时间戳筛选执行时间，Unix时间戳的毫秒数格式，如1597026383085 |
| endTs | String | 否 | 用结束时间戳筛选执行时间，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 返回结果的数量，最大为100，默认100条 |
| state | String | 否 | 移仓状态，filledpending |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| clientId | String | 客户自定义ID |
| blockTdId | String | 大宗交易ID |
| state | String | 移仓状态，filledfailed |
| ts | String | 移仓请求处理时间戳，Unix时间戳的毫秒数格式，如1597026383085 |
| fromAcct | String | 源账户名 |
| toAcct | String | 目标账户名 |
| legs | Array | 移仓仓位列表 |
| > from | Object | 源账户仓位 |
| >> instId | String | 产品ID |
| >> posId | String | 持仓ID |
| >> px | String | 移仓价格，过去60分钟的标记价格TWAP |
| >> side | String | 源账户的交易方向buysell |
| >> sz | String | 合约数量 |
| > to | Object | 目标账户移仓配置 |
| >> instId | String | 产品ID |
| >> px | String | 移仓价格，过去60分钟的标记价格TWAP |
| >> side | String | 目标账户交易方向 |
| >> sz | String | 合约数量 |
| >> tdMode | String | 目标账户的交易模式 |
| >> posSide | String | 目标账户持仓方向 |
| >> ccy | String | 保证金币种 |



---

## 设置自动赚币

开启/关闭自动赚币


### 限速：2次/2s


### 限速规则：User ID


### HTTP请求

POST /api/v5/account/set-auto-earn


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| earnType | String | 否 | 自动赚币类型0: 自动赚币 (自动出借、自动质押)1: 自动赚币（USDG 赚币）默认值为0 |
| ccy | String | 是 | 币种 |
| action | String | 是 | 自动赚币操作类型turn_on: 开启自动赚币turn_off: 关闭自动赚币amend: 修改最低年化收益率，仅适用于 earnType0（已弃用） |
| apr | String | 可选 | 最低年化收益率（已弃用） |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| earnType | String | 自动赚币类型0: 自动赚币 (自动出借、自动质押)1: 自动赚币（USDG 赚币） |
| ccy | String | 币种 |
| action | Boolean | 自动赚币操作类型turn_onturn_offamend（已弃用） |
| apr | String | 最低年化收益率（已弃用） |



---

## 设置结算币种

仅适用于 USD 本位合约。


### 限速：20 次/2 秒


### 限速规则：User ID


### 权限：交易


### HTTP 请求

POST /api/v5/account/set-settle-currency


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| settleCcy | String | 是 | USD 本位合约结算币种 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| settleCcy | String | USD 本位合约结算币种 |



---

## 设置交易配置


### 限速：1次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-trading-config


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| type | String | Yes | 交易配置类型stgyType |
| stgyType | String | No | 账号策略类型0：普通策略模式1：delta 中性策略模式仅适用于type为stgyType |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| type | String | 交易配置类型 |
| stgyType | String | 账号策略类型 |



---

## 设置Delta中性预检查


### 限速：1次/2s


### 限速规则：User ID


### HTTP请求

GET /api/v5/account/precheck-set-delta-neutral


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| stgyType | String | Yes | 策略类型0：普通策略模式1：delta 中性策略模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| unmatchedInfoCheck | Array of objects | 包含不匹配信息对象的列表 |
| > type | String | 不匹配信息类型spot_mode：delta 中性策略模式不支持现货模式futures_mode：delta 中性策略模式不支持合约模式isolated_margin：delta 中性策略模式不支持逐仓杠杆仓位isolated_contract：delta 中性策略模式不支持逐仓合约仓位positions_options：delta 中性策略模式不支持期权仓位isolated_pending_orders：delta 中性策略模式不支持逐仓挂单pending_orders_options：delta 中性策略模式不支持期权挂单trading_bot：delta 中性策略模式不支持策略交易repay_borrowings：在转换后，在目前策略下的负债量超过母账户维度借币限额，请偿还负债后重试loan：不支持delta 中性策略模式使用活期借币delta_risk：Delta风险检查失败，降低delta后重试collateral_all：delta 中性策略模式下，所有币种必要被设置为质押币 |
| > deltaLever | String | Delta权益比率仅适用于type为delta_risk |
| > ordList | Array of strings | 不匹配订单列表，返回订单ID在type为isolated_pending_orders/pending_orders_options时适用 |
| > posList | Array of strings | 不匹配仓位列表，返回仓位ID在type为isolated_margin/isolated_contract/positions_options时适用 |



---
