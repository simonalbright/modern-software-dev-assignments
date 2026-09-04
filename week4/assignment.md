# 第 4 周 —— 现实中的自主编码智能体

> ***建议在开始动手前通读本文件全文。***

本周的任务是：在本仓库的代码范围内，使用以下 **Claude Code** 功能中的任意组合，搭建**至少 2 个自动化工作流**：

- 自定义斜杠命令（放置在 `.claude/commands/*.md` 中）

- 用于仓库或上下文引导的 `CLAUDE.md` 文件

- Claude 子代理（SubAgents，即角色分工、协同工作的智能体）

- 集成到 Claude Code 中的 MCP 服务器

这些自动化应当切实改进某个开发工作流——例如让测试、文档、重构或数据处理相关的任务更顺畅。随后，你要用搭建好的自动化，去扩展 `week4/` 目录下的起步应用。


## 了解 Claude Code
为了深入理解 Claude Code 并探索可用的自动化方案，请阅读以下两份资料：

1. **Claude Code 最佳实践：** [anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)

2. **子代理概览：** [docs.anthropic.com/en/docs/claude-code/sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents)

## 探索起步应用
这是一个极简的全栈起步应用，定位是**"开发者指挥中心"**：
- FastAPI 后端 + SQLite（SQLAlchemy）
- 静态前端（无需 Node 工具链）
- 极简测试（pytest）
- pre-commit（black + ruff）
- 用于练习智能体驱动工作流的任务清单

请把这个应用当作你练习、搭建 Claude 自动化的试验场。

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

3) 运行应用（在 `week4/` 目录下）

```bash
make run
```

4) 打开 `http://localhost:8000` 访问前端，`http://localhost:8000/docs` 查看 API 文档。

5) 动手操作一下起步应用，熟悉它当前的功能与特性。


### 测试
运行测试（在 `week4/` 目录下）
```bash
make test
```

### 格式化 / Lint
```bash
make format
make lint
```

## 第一部分：搭建你的自动化（任选 2 个及以上）
现在你已经熟悉了起步应用，下一步就是搭建用于增强或扩展它的自动化。下面给出若干可选的自动化方向，你可以跨类别自由组合。

在搭建自动化的过程中，请在 `writeup.md` 中记录你的改动。*「你是如何用自动化增强起步应用的」* 这一节先留空——第二部分的作业会让你回头填写。

### A) Claude 自定义斜杠命令
斜杠命令是为重复性工作流设计的特性：把可复用的工作流写成 `.claude/commands/` 目录下的 Markdown 文件，Claude 会以 `/` 前缀暴露它们。


- 示例 1：带覆盖率统计的测试运行器
  - 名称：`tests.md`
  - 意图：运行 `pytest -q backend/tests --maxfail=1 -x`，若全部通过再运行覆盖率统计。
  - 输入：可选的 marker 或路径。
  - 输出：汇总失败项并给出下一步建议。
- 示例 2：文档同步
  - 名称：`docs-sync.md`
  - 意图：读取 `/openapi.json`，更新 `docs/API.md`，并列出路由的差异。
  - 输出：类似 diff 的汇总与 TODO 列表。
- 示例 3：重构工具
  - 名称：`refactor-module.md`
  - 意图：重命名模块（例如把 `services/extract.py` 改成 `services/parser.py`），更新相关 import，运行 lint 与测试。
  - 输出：改动文件清单与验证步骤。

>*Tips：让命令保持聚焦，善用 `$ARGUMENTS`，尽量采用幂等步骤；为提升可复现性，可考虑允许列表（allowlist）放行安全工具并使用无头（headless）模式。*

### B) `CLAUDE.md` 引导文件
开启对话时，`CLAUDE.md` 会被自动读取，让你提供仓库特定的指令、上下文或引导信息来影响 Claude 的行为。请在仓库根目录（可选：以及 `week4/` 的子目录中）创建 `CLAUDE.md` 来引导 Claude。

- 示例 1：代码导航与入口
  - 内容可包含：如何运行应用、路由位于哪里（`backend/app/routers`）、测试位于哪里、数据库种子数据如何写入。
- 示例 2：风格与安全护栏
  - 内容可包含：工具链约定（black/ruff）、允许运行的安全命令、应避免的命令、lint/测试门禁。
- 示例 3：工作流片段
  - 内容可包含："当被要求新增端点时，先写一个失败的测试，再实现功能，最后运行 pre-commit。"

> *Tips：像打磨提示词一样迭代 `CLAUDE.md`，保持简洁可执行，并把你期望 Claude 使用的自定义工具/脚本写进文档。*

### C) 子代理（角色专精）
子代理是为处理特定任务而配置的专用 AI 助手：它们拥有各自的系统提示词、工具与上下文。请设计两个或更多相互协作的代理，让每个代理负责某个工作流中一个独立环节。

- 示例 1：TestAgent + CodeAgent
  - 流程：TestAgent 为某改动编写/更新测试 → CodeAgent 实现代码以通过测试 → TestAgent 验证。
- 示例 2：DocsAgent + CodeAgent
  - 流程：CodeAgent 新增一个 API 路由 → DocsAgent 更新 `API.md` 与 `TASKS.md`，并与 `/openapi.json` 对照检查偏差。
- 示例 3：DBAgent + RefactorAgent
  - 流程：DBAgent 提出表结构改动（调整 `data/seed.sql`）→ RefactorAgent 同步更新 models/schemas/routers 并修复 lint 问题。

>*Tips：善用清单/草稿区，在不同角色之间重置上下文（`/clear`），相互独立的任务可以让代理并行运行。*

## 第二部分：让自动化真正跑起来
现在你已搭好 2 个以上自动化，来让它们发挥作用吧！在 `writeup.md` 的 *「你是如何用自动化增强起步应用的」* 一节中，描述你是如何利用每个自动化改进或扩展应用功能的。

例如：如果你实现了 `/generate-test-cases` 这个自定义斜杠命令，就说明你是如何借助它来与起步应用交互并完成测试的。


## 交付物
1) 两个或以上自动化，可包含：
   - `.claude/commands/*.md` 中的斜杠命令
   - `CLAUDE.md` 文件
   - 子代理的提示词/配置（记录清晰，如有文件/脚本也一并附上）

2) `week4/` 下的作业记录 `writeup.md`，需包含：
  - 设计灵感（例如引用最佳实践和/或子代理文档）
  - 每个自动化的设计：目标、输入/输出、步骤
  - 如何运行（准确命令）、预期输出、回滚/安全说明
  - 前后对比（即手动工作流 vs 自动化工作流）
  - 你是如何用自动化增强起步应用的



## 提交说明
1. 确保你已把全部改动推送到你的远程仓库，以备评分。
2. 按任课老师的要求完成提交（例如通过指定的作业提交平台）。
