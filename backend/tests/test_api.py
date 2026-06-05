from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_script_returns_schema_payload() -> None:
    response = client.post(
        "/scripts/generate",
        json={
            "title": "迷雾之城",
            "content": "第一章：夜色沉沉，林晚攥着信件走向旧城区。"
            "第二章：她在巷口停下，听见脚步声逼近。"
            "第三章：一道人影从黑暗中现身，打破了沉默。",
            "adaptation_mode": "balanced",
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["meta"]["title"] == "迷雾之城"
    assert body["meta"]["adaptation_mode"] == "balanced"
    assert body["characters"][0]["id"] == "char_protagonist"
    assert body["scenes"][0]["beats"][1]["type"] == "dialogue"


def test_generate_yaml_returns_yaml_text() -> None:
    response = client.post(
        "/scripts/generate/yaml",
        json={
            "title": "迷雾之城",
            "content": "第一章：夜色沉沉，林晚攥着信件走向旧城区。"
            "第二章：她在巷口停下，听见脚步声逼近。"
            "第三章：一道人影从黑暗中现身，打破了沉默。",
            "adaptation_mode": "dramatic",
        },
    )

    assert response.status_code == 200
    assert "version: '1.0'" in response.text
    assert "adaptation_mode: dramatic" in response.text


def test_parse_novel_returns_chapter_segments() -> None:
    response = client.post(
        "/novels/parse",
        json={
            "content": (
                "第1章 雨夜来信\n"
                "林晚在雨里攥着那封匿名信，迟迟没有离开街口。\n"
                "她知道今晚一定会有人出现。\n"
                "第2章 巷口脚步\n"
                "旧城区的风很冷，脚步声从巷子深处逼近。\n"
                "她压低呼吸，慢慢后退半步。\n"
                "第3章 黑影现身\n"
                "一道身影从黑暗里走出，目光落在她手中的信上。\n"
                "沉默只持续了两秒，就被一句质问打破。"
            )
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["chapter_count"] == 3
    assert body["chapters"][0]["title"] == "第1章 雨夜来信"
    assert body["chapters"][1]["index"] == 2


def test_parse_novel_accepts_less_than_three_chapters() -> None:
    response = client.post(
        "/novels/parse",
        json={
            "content": (
                "第1章 雨夜来信\n"
                "林晚在雨里攥着那封匿名信，迟迟没有离开街口，她知道今晚不会太平。\n"
                "第2章 巷口脚步\n"
                "旧城区的风很冷，脚步声从巷子深处逼近，她本能地攥紧了手中的信。"
            )
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["chapter_count"] == 2
    assert body["chapters"][0]["title"] == "第1章 雨夜来信"


def test_parse_novel_falls_back_to_single_unnamed_chapter() -> None:
    response = client.post(
        "/novels/parse",
        json={
            "content": (
                "林晚在雨里攥着那封匿名信，迟迟没有离开街口。"
                "她知道今晚一定会有人出现，而她必须先一步看清真相。"
            )
        },
    )

    body = response.json()

    assert response.status_code == 200
    assert body["chapter_count"] == 1
    assert body["chapters"][0]["title"] == "未命名章节 1"
