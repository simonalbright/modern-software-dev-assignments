def test_create_and_list_notes(client):
    payload = {"title": "测试笔记", "content": "你好，世界"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "测试笔记"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "你好"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1
