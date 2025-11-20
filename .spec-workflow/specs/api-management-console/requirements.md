# Requirements Document

## Introduction

为 DeepSeek 加密货币交易机器人构建一套完整的 API 管理控制台系统，包含：
1. **OpenAPI 接口层**：基于 FastAPI 的 RESTful API，提供策略控制、参数管理、实时信号查询、日志查看等核心功能
2. **Web 管理控制台**：基于 Vue3 + Element Plus 的前端界面，提供仪表盘、策略管理、日志中心、用户权限管理等功能
3. **双轨存储架构**：支持轻量级（JSON + SQLite）和企业级（PostgreSQL/Redis）两种存储模式，可无缝切换

该系统将让运维人员能够实时监控交易机器人状态、动态调整策略参数、查看交易历史和系统日志，实现生产级运维管理能力。

## Alignment with Product Vision

本功能直接支持 DeepSeek 交易机器人的产品愿景：
- **生产级运维**：从命令行工具升级到 Web 控制台，满足生产环境监控和管理需求
- **风险控制增强**：通过实时日志查看和告警机制，及时发现和处理异常交易
- **用户体验提升**：可视化界面让非技术人员也能理解和监控交易策略
- **架构演进**：从单体式向模块化演进，为后续微服务化奠定基础

## Requirements

### Requirement 1: API 认证与授权管理

**User Story:** 作为系统管理员，我能够生成和管理用户访问令牌，以便为不同角色分配不同的操作权限。

#### Acceptance Criteria

1. WHEN 管理员请求创建新用户令牌 THEN 系统 SHALL 生成唯一的随机令牌并返回
2. IF 令牌创建请求包含权限范围 THEN 系统 SHALL 将权限信息与令牌关联存储
3. WHEN 用户携带令牌访问受保护接口 THEN 系统 SHALL 验证令牌有效性并返回对应角色权限
4. IF 令牌无效或已过期 THEN 系统 SHALL 返回 401 Unauthorized 错误
5. WHEN 管理员请求吊销令牌 THEN 系统 SHALL 立即失效该令牌并阻止后续使用

### Requirement 2: 策略启停控制

**User Story:** 作为管理员，我能够通过 API 远程启动或停止交易策略，以便在异常情况下快速响应。

#### Acceptance Criteria

1. WHEN 管理员调用策略启动接口 THEN 系统 SHALL 启动指定 ID 的交易策略并返回确认
2. IF 策略已在运行状态 THEN 系统 SHALL 返回错误提示并拒绝重复启动
3. WHEN 管理员调用策略停止接口 THEN 系统 SHALL 停止策略运行并释放相关资源
4. WHEN 策略状态发生变化 THEN 系统 SHALL 记录操作日志包含操作人、时间、策略 ID
5. WHEN 普通用户查询策略状态时 THEN 系统 SHALL 返回当前运行状态但不允许修改

### Requirement 3: 策略参数动态调整

**User Story:** 作为管理员，我能够在策略运行时动态调整参数，以便优化交易效果而无需重启服务。

#### Acceptance Criteria

1. WHEN 管理员提交参数更新请求 THEN 系统 SHALL 验证参数格式和范围的有效性
2. IF 参数验证通过 THEN 系统 SHALL 立即更新内存中的配置并持久化存储
3. WHEN 参数更新完成后 THEN 系统 SHALL 返回成功确认和更新后的参数列表
4. IF 参数格式无效 THEN 系统 SHALL 返回 400 Bad Request 及具体错误信息
5. WHEN 普通用户查询策略参数时 THEN 系统 SHALL 返回参数列表但不允许修改

### Requirement 4: 实时信号查询

**User Story:** 作为运维人员，我能够查询最近的交易信号，以便监控 AI 决策质量和策略表现。

#### Acceptance Criteria

1. WHEN 用户请求最新信号 THEN 系统 SHALL 返回最近 N 条交易信号（默认 30 条）
2. WHEN 用户指定时间范围 THEN 系统 SHALL 返回该范围内的所有信号记录
3. EACH 信号记录 SHALL 包含信号类型、信心度、生成时间、触发原因等关键信息
4. IF 用户指定策略 ID 过滤 THEN 系统 SHALL 只返回该策略产生的信号
5. WHEN 请求包含分页参数 THEN 系统 SHALL 支持分页返回结果并包含总数

### Requirement 5: 日志查看与过滤

**User Story:** 作为运维人员，我能够查看和过滤交易日志与系统日志，以便快速定位问题。

#### Acceptance Criteria

1. WHEN 用户查询日志 THEN 系统 SHALL 返回按时间倒序排列的日志列表
2. WHEN 用户指定日志级别过滤 THEN 系统 SHALL 只返回该级别及以上的日志
3. WHEN 用户指定关键字搜索 THEN 系统 SHALL 返回包含该关键字的日志
4. WHEN 用户指定时间范围 THEN 系统 SHALL 返回该时间范围内的日志
5. SYSTEM SHALL 支持通过 SSE 实时推送新日志到订阅客户端
6. EACH 日志记录 SHALL 包含时间戳、级别、模块、消息内容等字段

### Requirement 6: 仪表盘监控

**User Story:** 作为运维人员，我能够通过 Web 界面查看交易机器人的整体运行状态，以便及时发现异常。

#### Acceptance Criteria

1. WHEN 用户访问仪表盘页面 THEN 系统 SHALL 显示账户余额、持仓、日限额使用等核心指标
2. WHEN 仪表盘加载时 THEN 系统 SHALL 显示各策略的运行状态和最近信号
3. WHEN 策略状态发生变化 THEN 系统 SHALL 实时更新仪表盘显示（通过轮询或 SSE）
4. SYSTEM SHALL 显示告警信息（如果有）在仪表盘顶部
5. WHEN 用户点击查看详情 THEN 系统 SHALL 跳转到对应详细页面

### Requirement 7: 策略管理界面

**User Story:** 作为管理员，我能够在 Web 界面上查看策略详情、启停策略和修改参数，以便直观管理交易策略。

#### Acceptance Criteria

1. WHEN 用户访问策略管理页面 THEN 系统 SHALL 显示所有策略的列表及其当前状态
2. WHEN 管理员点击启动按钮 THEN 系统 SHALL 调用 API 启动策略并更新状态显示
3. WHEN 管理员点击停止按钮 THEN 系统 SHALL 调用 API 停止策略并更新状态显示
4. WHEN 管理员点击编辑参数 THEN 系统 SHALL 显示参数表单并支持修改
5. WHEN 管理员提交参数修改 THEN 系统 SHALL 调用 API 更新参数并反馈结果
6. SYSTEM SHALL 只向管理员显示启停和编辑按钮，普通用户只显示查看

### Requirement 8: 日志中心界面

**User Story:** 作为运维人员，我能够在 Web 界面上查看和过滤日志，以便快速定位问题。

#### Acceptance Criteria

1. WHEN 用户访问日志中心 THEN 系统 SHALL 显示最近的日志列表
2. SYSTEM SHALL 提供标签页切换系统日志和交易日志
3. WHEN 用户选择日志级别 THEN 系统 SHALL 过滤显示对应级别的日志
4. WHEN 用户输入关键字 THEN 系统 SHALL 实时过滤包含关键字的日志
5. WHEN 用户选择时间范围 THEN 系统 SHALL 只显示该范围内的日志
6. WHEN 用户点击日志记录 THEN 系统 SHALL 显示该日志的详细信息弹窗

### Requirement 9: 用户权限管理界面

**User Story:** 作为管理员，我能够在 Web 界面上生成和吊销普通用户访问令牌，以便管理访问权限。

#### Acceptance Criteria

1. WHEN 管理员访问用户管理页面 THEN 系统 SHALL 显示所有普通用户令牌的列表
2. EACH 令牌记录 SHALL 显示创建时间、最后使用时间、权限范围和状态
3. WHEN 管理员点击生成令牌按钮 THEN 系统 SHALL 显示创建表单
4. WHEN 管理员填写表单并提交 THEN 系统 SHALL 调用 API 生成新令牌并显示结果
5. WHEN 管理员点击吊销按钮 THEN 系统 SHALL 调用 API 吊销令牌并更新列表
6. SYSTEM SHALL 确认吊销操作防止误操作

## Non-Functional Requirements

### Code Architecture and Modularity
- **Single Responsibility Principle**: 每个 API 路由处理函数只处理单一职责（认证、策略控制、日志查询等）
- **Modular Design**: 存储层抽象（StorageProvider/TokenRepository），支持 lite/enterprise 双模式
- **Dependency Management**: FastAPI 依赖注入管理认证和存储实例，降低耦合
- **Clear Interfaces**: 定义清晰的 Pydantic 模型用于请求/响应，前后端契约明确

### Performance
- **Response Time**: API 接口响应时间不超过 200ms（复杂查询不超过 1s）
- **Concurrent Users**: 支持至少 10 个并发用户访问控制台
- **Data Loading**: 日志和信号查询支持分页，单次返回不超过 100 条记录
- **Realtime Update**: SSE 延迟不超过 5 秒，轮询间隔可配置（默认 5-10 秒）

### Security
- **Authentication**: 基于 Bearer Token 的认证机制，管理员 Token 从环境变量读取
- **Authorization**: 基于角色的访问控制（RBAC），区分管理员和普通用户权限
- **Token Management**: 普通用户 Token 支持设置有效期，过期自动失效
- **Input Validation**: 所有输入参数使用 Pydantic 模型验证，防止注入攻击
- **CORS**: 配置合理的跨域策略，限制外部非授权访问

### Reliability
- **Error Handling**: API 返回统一的错误格式（包含错误码、消息、详情）
- **Graceful Degradation**: 存储服务不可用时，API 应返回友好错误而非崩溃
- **Logging**: 所有关键操作记录审计日志（策略启停、参数修改、令牌生成等）
- **Health Check**: 提供 `/api/health` 接口用于监控系统健康状态

### Usability
- **API Documentation**: 自动生成 OpenAPI/Swagger 文档，方便前端开发和测试
- **Consistent Response Format**: 统一使用 `{ "data": ..., "message": "...", "code": 200 }` 格式
- **Meaningful Error Messages**: 错误信息清晰易懂，帮助用户定位问题
- **Console UI**: 基于 Element Plus 组件库，保持一致的用户体验
