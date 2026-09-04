import os
import pytest

from ..app.services.extract import extract_action_items


def test_extract_bullets_and_checkboxes():
    text = """
    会议记录：
    - [ ] 初始化数据库
    * 实现 API 抽取接口
    1. 编写测试
    某段叙述性文字。
    """.strip()

    items = extract_action_items(text)
    assert "初始化数据库" in items
    assert "实现 API 抽取接口" in items
    assert "编写测试" in items
