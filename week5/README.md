# 第 5 周

用于实验自主编码智能体的极简全栈起步应用。

- FastAPI 后端 + SQLite（SQLAlchemy）
- 静态前端（无需 Node 工具链）
- 极简测试（pytest）
- pre-commit（black + ruff）
- 用于练习智能体驱动工作流的任务清单

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

3) 运行应用（在 `week5/` 下）

```bash
cd week5 && make run
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
cd week5 && make test
```

## 格式化 / Lint

```bash
cd week5 && make format
cd week5 && make lint
```

## 配置

把 `.env.example` 复制为 `.env`（放在 `week5/` 下），即可覆盖数据库路径等默认配置。
