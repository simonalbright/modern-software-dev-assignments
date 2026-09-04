# 现代软件开发实践（中文教学版）

本仓库是一套面向软件工程课程的渐进式实验材料，覆盖大型语言模型（LLM）提示工程、后端 API 开发、测试、自动化、代码质量与 MCP 集成等主题。材料仅供内部课堂教学使用，请勿对外发布或用于商业用途。

## 仓库结构

- `week1/` —— LLM 提示工程：K-shot、思维链（Chain-of-Thought）、工具调用、自一致性、RAG、Reflexion
- `week2/` —— 基于 FastAPI + SQLite 搭建"笔记 + 待办事项"应用，并接入本地 LLM 做动作项抽取
- `week3/` —— 基于 MCP（Model Context Protocol）构建工具服务器
- `week4/` —— 在应用仓库中搭建 AI 编码自动化工作流（自定义斜杠命令、上下文指导文件、子代理、MCP 集成）
- `week5/` ~ `week7/` —— 在此前基础上逐周增强后端、测试与前端（含数据库迁移、安全检索、CI 代码质量门禁等）
- `week8/` —— 项目收尾与总结

## 环境准备

以下步骤基于 Python 3.12。

1. 安装 Anaconda
   - 下载并安装：[Anaconda Individual Edition](https://www.anaconda.com/download)
   - 重新打开终端，使 `conda` 进入 `PATH`。

2. 创建并激活 Conda 环境（Python 3.12）
   ```bash
   conda create -n modern-sw-dev python=3.12 -y
   conda activate modern-sw-dev
   ```

3. 安装 Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. 在激活的 Conda 环境中用 Poetry 安装项目依赖
   在仓库根目录执行：
   ```bash
   poetry install --no-interaction
   ```

## 模型说明

本材料中的提示工程与 LLM 相关实验通过 [Ollama](https://ollama.com/) 在本地运行 **Qwen2.5**（Instruct 版）。模型按各练习原规模对标选用：

| 适用练习 | 对标原模型 | 现用模型 |
|---|---|---|
| 多数提示技巧 | Llama 3.1 8B | Qwen2.5-7B-Instruct |
| K-shot 提示 | Mistral-Nemo 12B | Qwen2.5-14B-Instruct |

建议以**完整模型名**拉取，再为其建立**别名**，练习与代码即可用短别名（`qwen2.5:7b` / `qwen2.5:14b`）直接调用：

```bash
# 1) 以完整模型名拉取
ollama pull qwen2.5:7b-instruct
ollama pull qwen2.5:14b-instruct

# 2) 建立别名
ollama cp qwen2.5:7b-instruct qwen2.5:7b
ollama cp qwen2.5:14b-instruct qwen2.5:14b
```

各周实验的具体运行方式见对应目录下的说明文档。
