# 第 2 周 —— 动作项提取器

本周我们将在极简 FastAPI + SQLite 应用的基础上做扩展：把自由格式的笔记转换为条理清晰的待办动作项。

***建议在开始动手前通读本文件全文。***

提示：预览本 Markdown 文件
- Mac：按下 `Command (⌘) + Shift + V`
- Windows/Linux：按下 `Ctrl + Shift + V`

## 开始之前

### 配置 Cursor
请按以下步骤安装 Cursor 并打开你的项目：
1. 下载并安装 Cursor：https://cursor.com/download
2. 若要启用 Cursor 命令行工具：打开 Cursor，在 Mac 上按 `Command (⌘) + Shift + P`（非 Mac 用户按 `Ctrl + Shift + P`）打开命令面板，输入：`Shell Command: Install 'cursor' command`，选中该项并回车。
3. 打开一个新的终端窗口，进入项目根目录并运行：`cursor .`

### 当前应用
按以下步骤启动现有的起步应用：
1. 激活你的 Conda 环境。
```
conda activate modern-sw-dev 
```
2. 在项目根目录启动服务：
```
poetry run uvicorn week2.app.main:app --reload
```
3. 打开浏览器访问 http://127.0.0.1:8000/。
4. 熟悉当前应用的状态，确认你可以成功输入笔记并生成提取出的动作项清单。

## 练习任务
每一项练习都请使用 Cursor 协助你在现有动作项提取器应用上实现对应的改进。

在完成作业的过程中，请用 `writeup.md` 记录进度。务必包含你使用的提示词，以及你或 Cursor 所做的改动。我们将根据这份记录的完整程度评分。请同时在代码中加入注释，说明你的改动。

### 任务 1：搭建新功能骨架

分析 `week2/app/services/extract.py` 中现有的 `extract_action_items()` 函数——它目前基于预定义的启发式规则完成动作项提取。

你的任务是实现一个**由 LLM 驱动**的替代函数 `extract_action_items_llm()`：通过 Ollama 调用本地大语言模型来完成动作项提取。

一些小提示：
- 若要生成结构化输出（即 JSON 字符串数组），可参考这篇文档：https://ollama.com/blog/structured-outputs
- 查看可用的 Ollama 模型：https://ollama.com/library。注意：模型越大资源占用越高，先从小模型开始。拉取并运行模型的命令：`ollama pull qwen3.5`，然后执行 `ollama run qwen3.5`。本课程实验统一使用 qwen3.5。

### 任务 2：编写单元测试

在 `week2/tests/test_extract.py` 中为 `extract_action_items_llm()` 编写单元测试，覆盖多种输入（例如：项目符号列表、带关键词前缀的行、空输入）。

### 任务 3：为可读性重构现有代码

对后端代码执行一次重构，重点关注：定义清晰的 API 契约 / schema、数据库层清理、应用生命周期与配置、错误处理。

### 任务 4：使用代理模式（Agentic Mode）自动化小任务

1. 将 LLM 驱动的抽取集成为一个新端点。更新前端，增加一个「LLM 提取」按钮，点击后通过新端点触发抽取流程。

2. 新增一个用于获取全部笔记的端点。更新前端，增加一个「笔记列表」按钮，点击后拉取并展示所有笔记。

### 任务 5：由代码库生成 README

***学习目标：***
*学习如何让 AI 审视代码库并自动产出文档，体会 Cursor 解析代码上下文、将其转化为可读文档的能力。*

使用 Cursor 分析当前代码库并生成一份结构良好的 `README.md` 文件。README 至少应包含：
- 项目简介
- 如何搭建并运行项目
- API 端点及其功能
- 如何运行测试套件

## 交付物
按照说明填写 `week2/writeup.md`。确保你的所有改动都已在代码库中通过注释记录下来。

## 评分标准（共 100 分）
- 第 1-5 部分各 20 分（其中生成的代码 10 分、提示词 10 分）。
