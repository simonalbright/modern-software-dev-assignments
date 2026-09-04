# 仓库任务清单

## 1) 前端迁移到 Vite + React（复杂）
- 在 `week5/frontend/`（或其子目录如 `week5/frontend/ui/`）中搭建一个 Vite + React 应用。
- 用构建产物替换现有静态资源，并由 FastAPI 托管：
  - 构建输出到 `week5/frontend/dist/`。
  - 更新 FastAPI 的静态目录挂载，使其托管 `dist`，并把根路径（`/`）指向 `dist` 中的 `index.html`。
- 在 React 中接通现有端点：
  - 笔记：列表、创建、删除、编辑。
  - 动作项：列表、创建、完成。
- 更新 `Makefile`，新增目标：`web-install`、`web-dev`、`web-build`，并确保 `make run` 会自动构建前端产物（或在文档中说明该流程）。
- 至少为两个组件补充组件/单元测试（React Testing Library），并在 `backend/tests` 中补充 API 兼容性的集成测试。

## 2) 带分页与排序的笔记搜索（中等）
- 实现 `GET /notes/search?q=...&page=1&page_size=10&sort=created_desc|title_asc`。
- 对标题/内容使用不区分大小写的匹配。
- 返回包含 `items`、`total`、`page`、`page_size` 的负载。
- 使用 SQLAlchemy 组合查询：过滤器、排序与分页。
- 在 React UI 中加入搜索框、结果数量与上一页/下一页分页控件。
- 在 `backend/tests/test_notes.py` 中补充查询边界与分页的测试。

## 3) 完整笔记 CRUD 与乐观 UI 更新（中等）
- 新增 `PUT /notes/{id}` 与 `DELETE /notes/{id}`。
- 前端采用乐观更新更新状态，同时处理出错时的回滚。
- 在 `schemas.py` 中校验请求体（合理的最小/最大长度）。
- 补充成功与校验失败的测试。

## 4) 动作项：过滤与批量完成（中等）
- 新增 `GET /action-items?completed=true|false`，按完成状态过滤。
- 新增 `POST /action-items/bulk-complete`，接收 ID 列表并在一个事务内批量标记完成。
- 前端加入过滤开关与批量操作 UI。
- 补充测试覆盖过滤、批量行为以及出错时的事务回滚。

## 5) 标签功能与多对多关系（复杂）
- 新增 `Tag` 模型与连接表 `note_tags`（`Note` 与 `Tag` 之间的多对多关系）。
- 端点：
  - `GET /tags`、`POST /tags`、`DELETE /tags/{id}`
  - `POST /notes/{id}/tags` 挂接标签、`DELETE /notes/{id}/tags/{tag_id}` 解除挂接
- 更新抽取逻辑（见下一任务），自动从 `#hashtags` 创建/挂接标签。
- 在 UI 中以标签 chip 的形式展示标签，并支持按标签过滤笔记。
- 补充模型关系与端点行为的测试。

## 6) 改进抽取逻辑与端点（中等）
- 扩展 `backend/app/services/extract.py`，使其能够解析：
  - `#hashtags` → 标签
  - `- [ ] 任务文本` → 动作项
- 新增 `POST /notes/{id}/extract`：
  - 返回结构化的抽取结果；当 `apply=true` 时，可选地把新的标签/动作项持久化。
- 补充抽取解析与 `apply=true` 持久化路径的测试。

## 7) 健壮的错误处理与统一响应结构（易-中等）
- 使用 Pydantic 模型补充校验（最小长度约束、非空字符串）。
- 添加全局异常处理器，返回一致的 JSON 结构：
  - `{ "ok": false, "error": { "code": "NOT_FOUND", "message": "..." } }`
  - 成功响应：`{ "ok": true, "data": ... }`
- 更新测试，对成功与失败两种场景都断言响应结构。

## 8) 所有列表端点分页（简单）
- 为 `GET /notes` 与 `GET /action-items` 增加 `page` 与 `page_size` 参数。
- 各自返回 `items` 与 `total`。
- 前端为列表加分页；补充边界测试（最后一页为空、page_size 过大等）。

## 9) 查询性能与索引（易-中等）
- 在合适的字段上添加 SQLite 索引（例如 `notes.title`、标签的连接表）。
- 验证查询计划得到改善，并通过灌入更大数据集的测试确保无回归。

## 10) 测试覆盖率提升（简单）
- 补充测试覆盖：
  - 每个端点的 400/404 场景
  - 批量操作的并发/事务行为
  - 前端的搜索、分页与乐观更新的集成测试（可用 mock 或轻量实现）

## 11) 部署到 Vercel（中等-复杂）
- 前端采用 Vite + React：
  - 添加 `package.json`，包含 `build` 与 `preview` 脚本，并配置 Vite 输出到 `frontend/dist`（或 `frontend/ui/dist`）。
  - 添加 `vercel.json`，把项目根目录设为 `week5/frontend`、`outputDirectory` 设为 `dist`。
  - 构建时注入 `VITE_API_BASE_URL` 指向 API。
- API 部署在 Vercel（方案 A，serverless FastAPI）：
  - 创建 `week5/api/index.py`，从 `backend/app/main.py` 导入 FastAPI 的 `app`。
  - 确保 Vercel 能拿到 Python 依赖（为函数使用 `pyproject.toml` 或 `requirements.txt`）。
  - 配置 CORS，允许 Vercel 前端的来源。
  - 更新 `vercel.json`，把 `/api/*` 路由到 Python 函数，其余路由交给 React 应用。
- API 部署在别处（方案 B）：
  - 把后端部署到 Fly.io 或 Render 之类的服务。
  - 让 Vercel 前端通过 `VITE_API_BASE_URL` 消费外部 API，并配置必要的改写/代理。
- 在 `README.md` 中附一份简短的部署指南：环境变量、构建命令与回滚方式。
