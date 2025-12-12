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
| > collateralRestrict | String | 平台维度的质押借币限制truefalse（已弃用，请使用colRes） |
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


---

## 设置持仓模式

设置持仓模式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-position-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| posMode | String | 是 | 持仓方式long_short_mode：开平仓模式net_mode：买卖模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| posMode | String | 持仓方式 |



---

## 设置杠杆倍数

设置产品杠杆倍数。


### 限速：20次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-leverage


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 否 | 产品ID，如BTC-USDT如币币、交割、永续、期权，仅适用于单币现货、单币杠杆、交割、永续、期权 |
| ccy | String | 否 | 保证金币种，如BTC仅适用于MARGIN杠杆类 |
| lever | String | 是 | 杠杆倍数，0.01-125之间的数字 |
| mgnMode | String | 是 | 保证金模式cross：全仓isolated：逐仓 |
| posSide | String | 否 | 持仓方向long：开平仓模式开多short：开平仓模式开空仅适用于交割/永续 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| ccy | String | 保证金币种 |
| lever | String | 杠杆倍数 |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| posSide | String | 持仓方向 |



---

## 获取最大可下单数量

获取当前账户下特定产品的最大可买入/卖出数量。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-size


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| tdMode | String | 是 | 交易模式cash：非保证金cross：全仓isolated：逐仓 |
| ccy | String | 否 | 保证金币种，如BTC仅适用于单币保证金模式下的逐仓 |
| px | String | 否 | 委托价格，如100.1若不填，以市价计算最大可买/卖量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| maxBuy | String | 最大可买入数量 |
| maxSell | String | 最大可卖出数量 |



---

## 获取最大可用余额/保证金

获取账户最大可用余额/保证金。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-avail-size


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| tdMode | String | 是 | 交易模式cash：非保证金cross：全仓isolated：逐仓 |
| ccy | String | 否 | 保证金币种，如BTC仅适用于单币保证金模式下的逐仓 |
| reduceOnly | String | 否 | 是否只减仓false：不强制true：强制仅适用于交割/永续 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| availBuy | String | 可买入数量 |
| availSell | String | 可卖出数量 |



---

## 调整保证金

增加或减少保证金。


### 限速：20次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/position/margin-balance


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| posSide | String | 是 | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| type | String | 是 | 增减类型add：增加reduce：减少 |
| amt | String | 是 | 调整保证金数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| posSide | String | 持仓方向 |
| type | String | 增减类型add：增加reduce：减少 |
| amt | String | 调整保证金数量 |



---

## 获取杠杆倍数

获取产品杠杆倍数。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/leverage-info


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 否 | 产品ID，如BTC-USDT支持多个instId查询（不超过20个），半角逗号分隔 |
| mgnMode | String | 是 | 保证金模式cross：全仓isolated：逐仓 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| posSide | String | 持仓方向long：开平仓模式开多short：开平仓模式开空net：买卖模式 |
| lever | String | 杠杆倍数 |
| maxLever | String | 最大杠杆倍数 |



---

## 获取杠杆倍数预估信息

获取杠杆倍数预估信息。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/adjust-leverage-info


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| mgnMode | String | 是 | 保证金模式cross：全仓isolated：逐仓 |
| lever | String | 是 | 预估的杠杆倍数 |
| posSide | String | 否 | 持仓方向long：开多short：开空仅适用于交割/永续 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| posSide | String | 持仓方向long：开多short：开空仅适用于交割/永续 |
| lever | String | 预估的杠杆倍数 |
| maxLever | String | 调整后的最大杠杆倍数 |
| loanAlloc | String | 预期分配的借币量 |



---

## 获取交易产品最大可借

获取产品在交易模式下的最大可借。


### 限速：20次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-loan


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| mgnMode | String | 是 | 保证金模式cross：全仓isolated：逐仓 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| mgnMode | String | 保证金模式cross：全仓isolated：逐仓 |
| ccy | String | 币种 |
| maxLoan | String | 最大可借 |



---

## 获取当前账户交易手续费费率

获取账户当前交易手续费费率。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/trade-fee


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |
| instId | String | 否 | 产品ID，如BTC-USDT-SWAP |
| uly | String | 否 | 标的指数，如BTC-USD仅适用于交割/永续/期权 |
| instFamily | String | 否 | 交易品种，如BTC-USD仅适用于交割/永续/期权 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| category | String | 费率档位 |
| instType | String | 产品类型 |
| instFamily | String | 交易品种 |
| uly | String | 标的指数 |
| instId | String | 产品ID |
| taker | String | 吃单手续费率 |
| maker | String | 挂单手续费率 |
| takerU | String | USDT本位吃单手续费率 |
| makerU | String | USDT本位挂单手续费率 |
| takerG | String | 挂单吃单手续费率 |
| makerG | String | 挂单挂单手续费率 |
| takerU | String | USDT本位吃单手续费率 |
| makerU | String | USDT本位挂单手续费率 |



---

## 获取计息记录

获取计息记录。


### 限速：2次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/interest-accrued


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| type | String | 否 | 计息类型1：市场借币计息2：尊享借币计息3：平台借币计息 |
| ccy | String | 否 | 币种，如BTC |
| after | String | 否 | 请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| before | String | 否 | 请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| ccy | String | 币种 |
| interest | String | 计息数量 |
| interestRate | String | 利率 |
| liability | String | 负债总额 |
| ts | String | 计息时间，Unix时间戳的毫秒数格式，如1597026383085 |
| type | String | 计息类型1：市场借币计息2：尊享借币计息3：平台借币计息 |



---

## 获取用户当前市场借币利率

获取用户当前市场借币利率。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/interest-rate


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| interestRate | String | 利率 |



---

## 设置手续费计价方式

设置手续费计价方式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-fee-currency


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| feeType | String | 是 | 手续费类型0：手续费以获取币种收取1：手续费以计价币种收取 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| feeType | String | 手续费类型0：手续费以获取币种收取1：手续费以计价币种收取 |



---

## 期权greeks的PA/BS切换

切换期权greeks展示方式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-greeks


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| greeksType | String | 是 | 当前希腊字母展示方式PA：币本位BS：美元本位 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| greeksType | String | 当前希腊字母展示方式PA：币本位BS：美元本位 |



---

## 逐仓交易设置

设置逐仓交易模式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-isolated-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| isoMode | String | 是 | 逐仓保证金划转模式automatic：开仓自动划转autonomy：自主划转 |
| type | String | 是 | 适用产品类型MARGIN：币币杠杆SWAP：永续合约FUTURES：交割合约OPTION：期权 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| isoMode | String | 逐仓保证金划转模式automatic：开仓自动划转autonomy：自主划转 |
| type | String | 适用产品类型 |



---

## 查看账户最大可转余额

查看账户最大可转余额。


### 限速：2次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/max-withdrawal


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| instId | String | 否 | 产品ID，如BTC-USDT |
| mgnMode | String | 否 | 保证金模式cross：全仓isolated：逐仓 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| maxWd | String | 最大可转余额 |



---

## 查看账户特定风险状态

查看账户特定风险状态。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/risk-state


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| riskState | String | 账户风险状态normal：正常liquidation：爆仓中 |
| ts | String | 风险状态更新时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 获取借币利率与限额

获取借币利率与限额。


### 限速：2次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/borrow-interest-and-limit


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC支持多币种查询（不超过20个），币种之间半角逗号分隔 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| interestRate | String | 利率 |
| maxBorrowAmount | String | 最大借币数量 |



---

## 手动借/还币

手动借币或还币。


### 限速：20次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/borrow-repay


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| side | String | 是 | 操作类型borrow：借币repay：还币 |
| amt | String | 是 | 借/还币数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| side | String | 操作类型borrow：借币repay：还币 |
| amt | String | 借/还币数量 |
| ts | String | 操作时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 设置自动还币

设置自动还币。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-auto-repay


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| autoRepay | String | 是 | 自动还币状态true：开启false：关闭 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| autoRepay | String | 自动还币状态true：开启false：关闭 |



---

## 获取借/还币历史

获取借/还币历史。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/borrow-repay-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 否 | 币种，如BTC |
| after | String | 否 | 请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| before | String | 否 | 请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| side | String | 操作类型borrow：借币repay：还币 |
| amt | String | 借/还币数量 |
| ts | String | 操作时间，Unix时间戳的毫秒数格式，如1597026383085 |



---

## 仓位创建器

仓位创建器。


### 限速：1次/s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/position-builder


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| posAmt | String | 是 | 持仓数量 |
| liqPx | String | 是 | 预估强平价 |
| posSide | String | 是 | 持仓方向long：开多short：开空 |
| ordPx | String | 是 | 委托价格 |
| sz | String | 是 | 委托数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| posAmt | String | 持仓数量 |
| liqPx | String | 预估强平价 |
| posSide | String | 持仓方向 |
| ordPx | String | 委托价格 |
| sz | String | 委托数量 |



---

## 仓位创建器趋势图

仓位创建器趋势图。


### 限速：1次/s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/position-builder-trend


### 请求参数

无


### 返回参数

返回仓位创建器趋势图数据


---

## 设置现货对冲占用

设置现货对冲占用。


### 限速：1次/s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-risk-offset-amt


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| setOffsetAmt | String | 是 | 设置的现货对冲占用数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| setOffsetAmt | String | 设置的现货对冲占用数量 |



---

## 查看账户Greeks

查看账户Greeks。


### 限速：10次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/greeks


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ts | String | 数据更新时间，Unix时间戳的毫秒数格式，如1597026383085 |
| delta | String | Delta |
| gamma | String | Gamma |
| theta | String | Theta |
| vega | String | Vega |



---

## 获取组合保证金模式仓位限制

获取组合保证金模式仓位限制。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/position-tiers


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instType | String | 是 | 产品类型SWAP：永续合约FUTURES：交割合约 |
| uly | String | 否 | 标的指数，如BTC-USD |
| instFamily | String | 否 | 交易品种，如BTC-USD |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |
| posTier | String | 仓位档位 |
| maxSz | String | 最大持仓量 |
| mmr | String | 维持保证金率 |
| imr | String | 初始保证金率 |



---

## 开通期权交易

开通期权交易。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/activate-option


### 请求参数

无


### 返回参数

开通期权交易成功


---

## 设置自动借币

设置自动借币。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-auto-loan


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| autoLoan | String | 是 | 自动借币状态true：开启false：关闭 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| autoLoan | String | 自动借币状态true：开启false：关闭 |



---

## 预设置账户模式切换

预设置账户模式切换。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/pre-set-account-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| acctLv | String | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |



---

## 预检查账户模式切换

预检查账户模式切换。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/pre-check-account-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| acctLv | String | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |
| checkPassed | String | 预检查结果true：通过false：不通过 |



---

## 设置账户模式

设置账户模式。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-account-mode


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| acctLv | String | 是 | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| acctLv | String | 账户模式1：现货模式2：合约模式3：跨币种保证金模式4：组合保证金模式 |



---

## 设置质押币种

设置质押币种。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-collateral


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| isCollateral | String | 是 | 是否质押true：质押false：非质押 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| isCollateral | String | 是否质押true：质押false：非质押 |



---

## 查看质押币种

查看质押币种。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/collateral


### 请求参数

无


### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| isCollateral | String | 是否质押true：质押false：非质押 |



---

## 重置 MMP 状态

重置MMP状态。


### 限速：1次/s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/reset-mmp


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instFamily | String | 是 | 交易品种，如BTC-USDT |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |



---

## 设置 MMP

设置MMP。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-mmp


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instFamily | String | 是 | 交易品种，如BTC-USDT |
| timeInterval | String | 是 | 间隔时间，单位秒 |
| frozenInterval | String | 是 | 冻结时间，单位秒 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |
| timeInterval | String | 间隔时间 |
| frozenInterval | String | 冻结时间 |



---

## 查看 MMP 配置

查看MMP配置。


### 限速：5次/2s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/mmp-config


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instFamily | String | 是 | 交易品种，如BTC-USDT |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instFamily | String | 交易品种 |
| timeInterval | String | 间隔时间 |
| frozenInterval | String | 冻结时间 |
| mmpFrozen | String | MMP冻结状态 |



---

## 移仓

移仓。


### 限速：1次/s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/move-position


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| fromInstId | String | 是 | 源产品ID，如BTC-USDT |
| toInstId | String | 是 | 目标产品ID，如ETH-USDT |
| ccy | String | 是 | 币种，如BTC |
| amt | String | 是 | 移仓数量 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| fromInstId | String | 源产品ID |
| toInstId | String | 目标产品ID |
| ccy | String | 币种 |
| amt | String | 移仓数量 |



---

## 获取移仓历史

获取移仓历史。


### 限速：1次/s


### 限速规则：User ID


### 权限：读取


### HTTP请求

GET /api/v5/account/move-position-history


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| fromInstId | String | 否 | 源产品ID，如BTC-USDT |
| toInstId | String | 否 | 目标产品ID，如ETH-USDT |
| ccy | String | 否 | 币种，如BTC |
| after | String | 否 | 请求此时间戳之前（更旧的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| before | String | 否 | 请求此时间戳之后（更新的数据）的分页内容，Unix时间戳的毫秒数格式，如1597026383085 |
| limit | String | 否 | 分页返回的结果集数量，最大为100，不填默认返回100条 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| fromInstId | String | 源产品ID |
| toInstId | String | 目标产品ID |
| ccy | String | 币种 |
| amt | String | 移仓数量 |
| ts | String | 移仓时间，Unix时间戳的毫秒数格式，如1597026383085 |
| status | String | 移仓状态 |



---

## 设置自动赚币

设置自动赚币。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-auto-earn


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| autoEarn | String | 是 | 自动赚币状态true：开启false：关闭 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| autoEarn | String | 自动赚币状态true：开启false：关闭 |



---

## 设置结算币种

设置结算币种。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/settle-currency


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| ccy | String | 是 | 币种，如BTC |
| settleCurrency | String | 是 | 结算币种，如USDT |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| ccy | String | 币种 |
| settleCurrency | String | 结算币种 |



---

## 设置交易配置

设置交易配置。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/set-trading-config


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| config | String | 是 | 交易配置 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| config | String | 交易配置 |



---

## 设置Delta中性预检查

设置Delta中性预检查。


### 限速：5次/2s


### 限速规则：User ID


### 权限：交易


### HTTP请求

POST /api/v5/account/pre-set-delta-neutral


### 请求参数



| 参数名 | 类型 | 是否必须 | 描述 |
|--------|--------|--------|--------|
| instId | String | 是 | 产品ID，如BTC-USDT |
| delta | String | 是 | Delta值 |



### 返回参数



| 参数名 | 类型 | 描述 |
|--------|--------|--------|
| instId | String | 产品ID |
| delta | String | Delta值 |