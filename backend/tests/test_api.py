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
