# DeepSeek Trading Console 部署与运维指南

## 1. 总览
- **后端**: FastAPI + Uvicorn，位于 `src/api`
- **前端**: Vue3 + Vite 构建后的静态资源，位于 `frontend/dist`
- **存储**: SQLite (交易/日志)，JSON Token 仓库 (`data/user_tokens.json`)
- **日志**: `logs/app.log`（按天滚动）+ `logs/app.db`（结构化日志）
- **测试工具**: `pytest`、`pytest-benchmark`、`locust`

## 2. 部署前准备
1. **系统环境**
   - Python 3.10+
   - Node.js 20+（用于前端构建）
   - Git、curl、systemd (Linux)
2. **目录约定**
   ```
   /opt/deepseek-console
   ├── ds/                # 本仓库
   ├── venv/              # Python 虚拟环境
   └── frontend-dist/     # 前端构建产物
   ```
3. **账号与密钥**
   - 申请 OKX/Binance API Key、DeepSeek Key
   - 配置 `.env`（可参考 `.env.example`）

## 3. 后端部署步骤
1. **克隆与依赖安装**
   ```bash
   git clone <repo> ds
   cd ds
   python -m venv ../venv
   source ../venv/bin/activate
   pip install -r requirements.txt
   ```
2. **环境变量**
   - 复制 `.env.example` → `.env`
   - 配置交易参数、API Key、日志路径等
3. **数据库与目录**
   - 交易数据库: `data/daily_limits.db`
   - 日志数据库: `logs/app.db`
   - 运行 `python scripts/init_storage.py`（若需初始化）
4. **启动 FastAPI**
   ```bash
   uvicorn src.api.app:create_app \
     --factory --host 0.0.0.0 --port 8000 \
     --log-config logging.conf
   ```
5. **systemd 示例** (`/etc/systemd/system/deepseek-api.service`)
   ```ini
   [Unit]
   Description=DeepSeek Trading API
   After=network.target

   [Service]
   Type=simple
   WorkingDirectory=/opt/deepseek-console/ds
   EnvironmentFile=/opt/deepseek-console/ds/.env
   ExecStart=/opt/deepseek-console/venv/bin/uvicorn src.api.app:create_app --factory --host 0.0.0.0 --port 8000
   Restart=on-failure
   User=deepseek

   [Install]
   WantedBy=multi-user.target
   ```
6. **可选: 反向代理**
   - 使用 Nginx/Traefik 反代 `http://127.0.0.1:8000`
   - 启用 HTTPS（Let’s Encrypt）

## 4. 前端部署步骤
1. **构建**
   ```bash
   cd frontend
   npm install
   npm run build
   cp -r dist /opt/deepseek-console/frontend-dist
   ```
2. **Nginx 示例**
   ```nginx
   server {
     listen 80;
     server_name console.example.com;

     root /opt/deepseek-console/frontend-dist;
     index index.html;

     location / {
       try_files $uri $uri/ /index.html;
     }

     location /api/ {
       proxy_pass http://127.0.0.1:8000/api/;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
     }
   }
   ```
3. **缓存 & 版本号**
   - 利用 Vite 默认 hash 打包
   - 配置 CDN/Cache-Control 以提升加载性能

## 5. 运维监控
1. **健康检查**
   - `/api/status/summary` 返回引擎状态、日限额
   - 前端入口 `/dashboard` 监看实时概览
2. **日志**
   - 文件: `logs/app.log`（按天滚动）
   - SQLite: `logs/app.db`，可 `sqlite3` 查询
   - 可接入 Filebeat/Fluentd 将日志转发至 ELK/CloudWatch
3. **告警建议**
   - 监控 HTTP 5xx、响应时间、任务队列长度
   - 交易失败/限额触发可写入告警表，再推送通知

## 6. 备份与恢复
| 资源 | 路径 | 频率 | 方法 |
|------|------|------|------|
| 交易数据库 | `data/daily_limits.db` | 每日 | `sqlite3 .dump > backup.sql` |
| 日志数据库 | `logs/app.db` | 每日 | 同上 |
| Token 文件 | `data/user_tokens.json` | 每小时 | `rsync` / `cp` |
| 配置文件 | `.env`, `pyproject.toml`, `vite.config.ts` | 变更即备份 | Git / 对象存储 |

恢复步骤：
1. 停止后台服务
2. 恢复对应备份文件
3. 启动并执行健康检查

## 7. 测试与性能
1. **单元/集成测试**
   ```bash
   source ../venv/bin/activate
   pytest tests/test_api_integration.py -v
   ```
2. **性能基准** (`pytest-benchmark`)
   ```bash
   pytest tests/test_performance.py --benchmark-min-rounds=5
   ```
3. **压力测试** (Locust)
   ```bash
   locust -f tests/locustfile.py --host=http://localhost:8000
   # Web UI: http://localhost:8089 设置用户数/启动
   ```
4. **前端检查**
   - `npm run lint`（类型检查）
   - `npm run build`（产物验证）

## 8. 故障排查清单
| 场景 | 检查步骤 |
|------|----------|
| API 无响应 | Systemd 日志 → `journalctl -u deepseek-api`；检查端口冲突 |
| 响应慢 | 查看 `logs/app.db`/`app.log`；运行 `pytest tests/test_performance.py` 重测 |
| 日志未刷新 | 确认 `logs/` 权限；查看 `src/utils/logger.py` 配置 |
| SSE 502 | 当前 SSE 端点为占位返回 501，确认前端未启用实时模式或等待后续实现 |
| Token 失效 | 检查 `data/user_tokens.json` 状态，必要时重新生成 |

## 9. 未来扩展建议
- 引入 Redis / PostgreSQL 以支持多实例部署
- 使用 Docker/Kubernetes 统一部署
- 集成 Prometheus + Grafana 指标
- 完整实现 SSE 日志推送/订阅

> 如需进一步自动化（CI/CD、蓝绿发布等），可在此基础上扩展脚本与清单。祝部署顺利！
