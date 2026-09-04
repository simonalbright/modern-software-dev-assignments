import os
import re
from typing import Callable, List, Tuple
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 1

SYSTEM_PROMPT = """
你是一个编码助手。只输出一个用 ```python 围起来的代码块，其中定义
函数 is_valid_password(password: str) -> bool。不要有任何说明文字或注释。
实现保持最简。
"""

# TODO: 在这里填写你的反思（Reflexion）提示词！
YOUR_REFLEXION_PROMPT = ""


# 用于评估生成代码的标准测试用例集
SPECIALS = set("!@#$%^&*()-_")
TEST_CASES: List[Tuple[str, bool]] = [
    ("Password1!", True),       # 合法
    ("password1!", False),      # 缺少大写字母
    ("Password!", False),       # 缺少数字
    ("Password1", False),       # 缺少特殊字符
]


def extract_code_block(text: str) -> str:
    m = re.findall(r"```python\n([\s\S]*?)```", text, flags=re.IGNORECASE)
    if m:
        return m[-1].strip()
    m = re.findall(r"```\n([\s\S]*?)```", text)
    if m:
        return m[-1].strip()
    return text.strip()


def load_function_from_code(code_str: str) -> Callable[[str], bool]:
    namespace: dict = {}
    exec(code_str, namespace)  # noqa: S102（练习场景：执行受控的模型生成代码）
    func = namespace.get("is_valid_password")
    if not callable(func):
        raise ValueError("生成的代码中未找到可调用的 is_valid_password")
    return func


def evaluate_function(func: Callable[[str], bool]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for pw, expected in TEST_CASES:
        try:
            result = bool(func(pw))
        except Exception as exc:
            failures.append(f"输入：{pw} → 抛出异常：{exc}")
            continue

        if result != expected:
            # 根据标准规则计算诊断信息
            reasons = []
            if len(pw) < 8:
                reasons.append("长度小于 8")
            if not any(c.islower() for c in pw):
                reasons.append("缺少小写字母")
            if not any(c.isupper() for c in pw):
                reasons.append("缺少大写字母")
            if not any(c.isdigit() for c in pw):
                reasons.append("缺少数字")
            if not any(c in SPECIALS for c in pw):
                reasons.append("缺少特殊字符")
            if any(c.isspace() for c in pw):
                reasons.append("包含空白字符")

            failures.append(
                f"输入：{pw} → 期望 {expected}，实际 {result}。未通过的检查：{', '.join(reasons) or '未知'}"
            )

    return (len(failures) == 0, failures)


def generate_initial_function(system_prompt: str) -> str:
    response = chat(
        model="qwen2.5",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "请立即给出实现。"},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def your_build_reflexion_context(prev_code: str, failures: List[str]) -> str:
    """TODO: 利用 prev_code 与 failures 构造反思步骤所需的用户消息。

    返回一个字符串，将作为用户消息与反思系统提示词一起发送。
    """
    return ""


def apply_reflexion(
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
    prev_code: str,
    failures: List[str],
) -> str:
    reflection_context = build_context(prev_code, failures)
    print(f"反思上下文：{reflection_context}，{reflexion_prompt}")
    response = chat(
        model="qwen2.5",
        messages=[
            {"role": "system", "content": reflexion_prompt},
            {"role": "user", "content": reflection_context},
        ],
        options={"temperature": 0.2},
    )
    return extract_code_block(response.message.content)


def run_reflexion_flow(
    system_prompt: str,
    reflexion_prompt: str,
    build_context: Callable[[str, List[str]], str],
) -> bool:
    # 1) 生成初始函数
    initial_code = generate_initial_function(system_prompt)
    print("初始代码：\n" + initial_code)
    func = load_function_from_code(initial_code)
    passed, failures = evaluate_function(func)
    if passed:
        print("SUCCESS（初始实现通过了全部测试）")
        return True
    else:
        print(f"失败（初始实现未通过部分测试）：{failures}")

    # 2) 单轮反思迭代
    improved_code = apply_reflexion(reflexion_prompt, build_context, initial_code, failures)
    print("\n改进后的代码：\n" + improved_code)
    improved_func = load_function_from_code(improved_code)
    passed2, failures2 = evaluate_function(improved_func)
    if passed2:
        print("SUCCESS")
        return True

    print("反思后仍有测试未通过：")
    for f in failures2:
        print("- " + f)
    return False


if __name__ == "__main__":
    run_reflexion_flow(SYSTEM_PROMPT, YOUR_REFLEXION_PROMPT, your_build_reflexion_context)
