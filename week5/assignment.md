# 第 5 周 —— 基于 Warp 的智能体开发

把 `week5/` 中的应用当作你的试验场。本周与上一周的作业思路一致，但重点转向 Warp 智能体开发环境与多智能体工作流。

## 了解 Warp
- Warp 智能体开发环境（Agentic Development Environment）：[warp.dev](https://www.warp.dev/)
- [Warp University](https://www.warp.dev/university?slug=university)


## 探索起步应用
极简全栈起步应用。
- FastAPI 后端 + SQLite（SQLAlchemy）
- 静态前端（无需 Node 工具链）
- 极简测试（pytest）
- pre-commit（black + ruff）
- 用于练习智能体驱动工作流的任务清单

请把这个应用当作你练习、搭建 Warp 自动化的试验场。

### 目录结构

```
backend/                # FastAPI 应用
frontend/               # 由 FastAPI 托管的静态前端
data/                   # SQLite 数据库 + 种子数据
docs/                   # 供智能体驱动工作流使用的任务清单
```

### 快速上手

1) 激活你的 Conda 环境。

```bash
conda activate modern-sw-dev
```

2)（可选）安装 pre-commit 钩子

```bash
pre-commit install
```

3) 运行应用（在 `week5/` 目录下）

```bash
make run
```

4) 打开 `http://localhost:8000` 访问前端，`http://localhost:8000/docs` 查看 API 文档。

5) 动手操作一下起步应用，熟悉它当前的功能与特性。


### 测试
运行测试（在 `week5/` 目录下）
```bash
make test
```

### 格式化 / Lint
```bash
make format
make lint
```

## 第一部分：搭建你的自动化（任选 2 个及以上）
从 `week5/docs/TASKS.md` 中选择要完成的任务。你的实现必须从以下两个角度使用 Warp（详见下文）：

- A) 使用 Warp Drive 的功能——例如已保存的提示词、规则或 MCP 服务器。
- B) 在 Warp 内组织多智能体工作流。

请把改动范围限定在 `week5/` 内的后端、前端、逻辑或测试上。
对每个选定的任务，请标注其难度等级。


### A) Warp Drive：保存的提示词、规则、MCP 服务器（必选：至少一种）
创建一条或多条可共享的 Warp Drive 提示词、规则或 MCP 服务器集成，使其契合本仓库。示例方向：
- 带覆盖率与 flaky 测试重跑的测试运行器
- 文档同步：从 `/openapi.json` 生成/更新 `docs/API.md`，并列出路由差异
- 重构工具：重命名模块、更新 import、运行 lint/测试
- 发布助手：升级版本号、运行检查、准备变更日志片段
- 集成 Git MCP 服务器，让 Warp 自主完成 Git 操作（创建分支、提交、PR 说明等）

>*Tips：让工作流保持聚焦、支持传参、尽量幂等，并优先使用无头/非交互式步骤。*

### B) Warp 中的多智能体工作流（必选：至少一种）
运行一个多智能体会话：让不同 Warp 标签页中的独立智能体并发处理相互独立的任务。
- 在多个 Warp 标签页中，用并发的智能体执行多个来自 `TASKS.md` 的相互独立任务。挑战：你能让多少个智能体同时工作？

>*Tips：[git worktree](https://git-scm.com/docs/git-worktree) 在这里可能很有用，可以避免多个智能体互相覆盖改动。*


## 第二部分：让自动化真正跑起来
现在你已搭好 2 个以上自动化，来让它们发挥作用吧！在 `writeup.md` 的 *「你是如何用自动化（它解决/加速了哪个痛点）」* 一节中，描述你是如何借助每个自动化改进某个工作流的。

## 范围与约束
请严格在 `week5/` 内作业（后端、前端、逻辑、测试）。除非自动化明确要求改动其他周次并记录原因，否则不要改动其他周。


## 交付物
1) 两个或以上 Warp 自动化，可包含：
   - Warp Drive 工作流/规则（分享链接和/或导出的定义），以及任何辅助脚本
   - 用于协调多个智能体的补充提示词/剧本（playbooks）

2) `week5/` 下的作业记录 `writeup.md`，需包含：
   - 每个自动化的设计：目标、输入/输出、步骤
   - 前后对比（即手动工作流 vs 自动化工作流）
   - 每个任务使用的自主级别（用了哪些代码权限、为什么，以及你是如何监督的）
   -（如适用）多智能体笔记：角色、协调策略、并发的收益/风险/失败
   - 你是如何用这个自动化的（它解决/加速了哪个痛点）



## 提交说明
1. 确保你已把全部改动推送到你的远程仓库，以备评分。
2. 按任课老师的要求完成提交（例如通过指定的作业提交平台）。
