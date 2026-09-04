import os
import re
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: 在这里填写你的系统提示词！
YOUR_SYSTEM_PROMPT = ""


USER_PROMPT = """
请解决下面的问题，并在最后一行以 "Answer: <数字>" 的格式给出最终答案。

3^{12345} (mod 100) 等于多少？
"""


# 对于这个简单示例，我们只期望得到最终的数值答案
EXPECTED_OUTPUT = "Answer: 43"


def extract_final_answer(text: str) -> str:
    """从冗长的推理轨迹中提取最终的 "Answer: ..." 行。

    - 找到以 "Answer:" 开头（不区分大小写）的最后一行
    - 若存在数字，则规范化为 "Answer: <数字>" 的形式
    - 若未检测到数字，则回退为返回匹配到的原始内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        # 尽可能做数值归一化（支持整数/小数）
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """最多运行 NUM_RUNS_TIMES 次，若任一次输出与 EXPECTED_OUTPUT 一致则返回 True。

    命中时打印 "SUCCESS"。
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="qwen3.5",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.3},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        if final_answer.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"期望输出：{EXPECTED_OUTPUT}")
            print(f"实际输出：{final_answer}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
