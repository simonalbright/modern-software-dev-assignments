# 第 7 周

在前几周基础上略作增强的全栈起步应用，并对后端做了若干改进。

- FastAPI 后端 + SQLite（SQLAlchemy）
- 静态前端（无需 Node 工具链）
- 极简测试（pytest）
- pre-commit（black + ruff）
- 相比第 5 周的增强点：
  - 模型增加时间戳字段（`created_at`、`updated_at`）
  - 列表端点支持分页与排序
  - 可选过滤器（例如按完成状态过滤动作项）
  - 支持部分更新的 PATCH 端点

## 快速上手

1) 创建并激活虚拟环境，然后安装依赖

```bash
cd /path/to/your/project
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

2)（可选）安装 pre-commit 钩子

```bash
pre-commit install
```

3) 运行应用（在 `week7/` 下）

```bash
cd week7 && make run
```

打开 `http://localhost:8000` 访问前端，`http://localhost:8000/docs` 查看 API 文档。

## 目录结构

```
backend/                # FastAPI 应用
frontend/               # 由 FastAPI 托管的静态前端
data/                   # SQLite 数据库 + 种子数据
docs/                   # 供智能体驱动工作流使用的任务清单
```

## 测试

```bash
cd week7 && make test
```

## 格式化 / Lint

```bash
cd week7 && make format
cd week7 && make lint
```

## 配置

把 `.env.example` 复制为 `.env`（放在 `week7/` 下），即可覆盖数据库路径等默认配置。
