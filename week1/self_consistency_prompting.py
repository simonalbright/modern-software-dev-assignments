import os
import re
from collections import Counter
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: 在这里填写你的系统提示词！尽量让多次运行的正确率接近 100%。
YOUR_SYSTEM_PROMPT = ""

USER_PROMPT = """
请解决下面的问题，并在最后一行以 "Answer: <数字>" 的格式给出最终答案。

亨利在 60 英里的骑行途中停了两次。他先骑了 20 英里后第一次停下，
第二次停车点距终点还有 15 英里。请问他的第一次与第二次停车点之间骑了多少英里？
"""

EXPECTED_OUTPUT = "Answer: 25"


def extract_final_answer(text: str) -> str:
    """从冗长的推理轨迹中提取最终的 "Answer: ..." 行。

    - 找到以 "Answer:" 开头（不区分大小写）的最后一行
    - 若存在数字，则规范化为 "Answer: <数字>" 的形式
    - 若未检测到数字，则回退为返回匹配到的原始内容
    """
    matches = re.findall(r"(?mi)^\s*answer\s*:\s*(.+)\s*$", text)
    if matches:
        value = matches[-1].strip()
        num_match = re.search(r"-?\d+(?:\.\d+)?", value.replace(",", ""))
        if num_match:
            return f"Answer: {num_match.group(0)}"
        return f"Answer: {value}"
    return text.strip()


def test_your_prompt(system_prompt: str) -> bool:
    """运行 NUM_RUNS_TIMES 次，对提取出的 "Answer: ..." 行做多数投票。

    若多数答案等于 EXPECTED_OUTPUT，则打印 "SUCCESS"。
    """
    answers: list[str] = []
    for idx in range(NUM_RUNS_TIMES):
        print(f"正在运行第 {idx + 1}/{NUM_RUNS_TIMES} 次测试")
        response = chat(
            model="qwen2.5:7b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 1},
        )
        output_text = response.message.content
        final_answer = extract_final_answer(output_text)
        print(f"第 {idx + 1} 次答案：{final_answer}")
        answers.append(final_answer.strip())

    if not answers:
        print("没有产生任何答案。")
        return False

    counts = Counter(answers)
    majority_answer, majority_count = counts.most_common(1)[0]
    print(f"多数答案：{majority_answer}（{majority_count}/{len(answers)}）")

    if majority_answer.strip() == EXPECTED_OUTPUT.strip():
        print("SUCCESS")
        return True

    # 当多数答案与期望不一致时，打印分布以便调试
    print(f"期望输出：{EXPECTED_OUTPUT}")
    print("答案分布：")
    for answer, count in counts.most_common():
        print(f"  {answer}: {count}")
    return False


if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)
