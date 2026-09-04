import os
import re
from typing import List, Callable
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

DATA_FILES: List[str] = [
    os.path.join(os.path.dirname(__file__), "data", "api_docs.txt"),
]


def load_corpus_from_files(paths: List[str]) -> List[str]:
    corpus: List[str] = []
    for p in paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    corpus.append(f.read())
            except Exception as exc:
                corpus.append(f"[load_error] {p}: {exc}")
        else:
            corpus.append(f"[missing_file] {p}")
    return corpus


# 从外部文件（简单的 API 文档）加载语料；若缺失，则回退为空列表
CORPUS: List[str] = load_corpus_from_files(DATA_FILES)

QUESTION = (
    "请编写一个 Python 函数 `fetch_user_name(user_id: str, api_key: str) -> str`，"
    "它调用文档中描述的 API 按 id 获取用户，并只返回该用户的姓名（字符串）。"
)


# TODO: 在这里填写你的系统提示词！
YOUR_SYSTEM_PROMPT = ""


# 针对该编码任务，通过检查关键代码片段（而非精确字符串比对）来验证结果
REQUIRED_SNIPPETS = [
    "def fetch_user_name(",
    "requests.get",
    "/users/",
    "X-API-Key",
    "return",
]


def YOUR_CONTEXT_PROVIDER(corpus: List[str]) -> List[str]:
    """TODO: 从 CORPUS 中选出与当前任务相关的文档子集并返回。

    例如，返回 [] 表示模拟"没有上下文"，或返回 [corpus[0]] 表示带上 API 文档。
    """
    return []


def make_user_prompt(question: str, context_docs: List[str]) -> str:
    if context_docs:
        context_block = "\n".join(f"- {d}" for d in context_docs)
    else:
        context_block = "(未提供上下文)"
    return (
        f"背景资料（只使用以下信息）：\n{context_block}\n\n"
        f"任务：{question}\n\n"
        "要求：\n"
        "- 使用文档中给出的 Base URL 与接口路径。\n"
        "- 发送文档中给出的认证请求头。\n"
        "- 对非 200 的响应抛出异常。\n"
        "- 只返回用户的姓名字符串。\n\n"
        "输出：一个用 ```python 围起来的代码块，包含该函数及必要的 import。\n"
    )


def extract_code_block(text: str) -> str:
    """提取最后一个 ```python 围起的代码块；若无则取任意围栏代码块，否则返回原文。"""
    # 先尝试 ```python ... ```
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    # 回退：任意围栏代码块
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def test_your_prompt(system_prompt: str, context_provider: Callable[[List[str]], List[str]]) -> bool:
    """最多运行 NUM_RUNS_TIMES 次，若任一次输出满足要求则返回 True。"""
    context_docs = context_provider(CORPUS)
    user_prompt = make_user_prompt(QUESTION, context_docs)

    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="qwen2.5:7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            options={"temperature": 0.0},
        )
        output_text = response.message.content
        code = extract_code_block(output_text)
        missing = [s for s in REQUIRED_SNIPPETS if s not in code]
        if not missing:
            print(output_text)
            print("SUCCESS")
            return True
        else:
            print("缺少以下必需代码片段：")
            for s in missing:
                print(f"  - {s}")
            print("生成的代码：\n" + code)
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT, YOUR_CONTEXT_PROVIDER)
