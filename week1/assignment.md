# 第 1 周 —— 提示工程技巧

本周你将通过为若干具体任务编写提示词，来练习多种提示工程技巧。每项任务的说明位于其对应源文件的顶部。

## 安装
请先完成仓库根目录 `README.md` 中描述的安装步骤。

## Ollama 安装
我们将使用 [Ollama](https://ollama.com/) 在你的机器上本地运行主流 LLM。可通过以下任一方式安装：

- macOS（Homebrew）：
  ```bash
  brew install --cask ollama 
  ollama serve
  ```

- Linux（推荐）：
  ```bash
  curl -fsSL https://ollama.com/install.sh | sh
  ```

- Windows：
  从 [ollama.com/download](https://ollama.com/download) 下载并运行安装程序。

验证安装：
```bash
ollama -v
```

运行测试脚本之前，请先拉取所需的模型。该操作只需执行一次（除非你之后删除了模型）：
```bash
ollama pull qwen3.5
```

## 技巧与源文件
- K-shot 提示（少样本示例）—— `week1/k_shot_prompting.py`
- 思维链（Chain-of-Thought）—— `week1/chain_of_thought.py`
- 工具调用（Tool calling）—— `week1/tool_calling.py`
- 自一致性提示（Self-consistency）—— `week1/self_consistency_prompting.py`
- RAG（检索增强生成，Retrieval-Augmented Generation）—— `week1/rag.py`
- Reflexion（反思式自我改进）—— `week1/reflexion.py`

## 交付物
- 阅读每个文件顶部的任务说明。
- 设计并运行提示词（找到代码中所有标注 `TODO` 的位置）。这应当是你唯一需要改动的地方（即不要改动模型）。
- 迭代改进结果，直到测试脚本通过为止。
- 保存每种技巧的最终提示词与输出。
- 提交内容中需包含每个提示技巧文件的完整代码。***请再次确认所有 `TODO` 均已填写完成。***

## 评分标准（共 60 分）
- 6 种提示技巧，每种完成即可得 10 分
