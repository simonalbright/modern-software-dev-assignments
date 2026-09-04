import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: 在这里填写你的系统提示词！
YOUR_SYSTEM_PROMPT = ""

USER_PROMPT = """
请将下列单词中的字母顺序反转。只输出反转后的单词，不要输出任何其他文字：

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """最多运行 NUM_RUNS_TIMES 次，若任一次输出与 EXPECTED_OUTPUT 一致则返回 True。

    命中时打印 "SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="qwen2.5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"期望输出：{EXPECTED_OUTPUT}")
            print(f"实际输出：{output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
