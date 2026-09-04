# 仓库任务清单

## 1) 启用 pre-commit 并修复仓库
- 安装钩子：`pre-commit install`
- 运行：`pre-commit run --all-files`
- 修复所有格式/lint 问题（black/ruff）

## 2) 为笔记增加搜索端点
- 使用 SQLAlchemy 过滤器新增/扩展 `GET /notes/search?q=...`（不区分大小写）
- 更新 `frontend/app.js` 使用该搜索查询
- 在 `backend/tests/test_notes.py` 中补充测试

## 3) 打通动作项流程
- 实现 `PUT /action-items/{id}/complete`（已有脚手架）
- 更新 UI 以反映完成状态（前端已接好），并扩展测试覆盖

## 4) 改进抽取逻辑
- 扩展 `backend/app/services/extract.py`，使其能解析类似 `#tag` 的标签并返回
- 为新的解析行为补充测试
-（可选）暴露 `POST /notes/{id}/extract`，把笔记转成动作项

## 5) 笔记 CRUD 增强
- 新增 `PUT /notes/{id}` 编辑笔记（标题/内容）
- 新增 `DELETE /notes/{id}` 删除笔记
- 更新 `frontend/app.js` 支持编辑/删除，并补充测试

## 6) 请求校验与错误处理
- 在 `schemas.py` 中加入简单校验规则（例如最小长度）
- 在合适的地方返回信息明确的 400/404 错误；为校验失败补充测试

## 7) 文档漂移检查（暂为手动）
- 创建/维护一份描述端点与请求体的 `API.md`
- 每次改动后，确认文档与实际的 OpenAPI（`/openapi.json`）一致
