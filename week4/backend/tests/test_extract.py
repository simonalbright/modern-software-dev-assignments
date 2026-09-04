from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    这是一条普通笔记
    - TODO: 编写测试
    - 立刻上线!
    不可执行的一行
    """.strip()
    items = extract_action_items(text)
    assert "TODO: 编写测试" in items
    assert "立刻上线!" in items
