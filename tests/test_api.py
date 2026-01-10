import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_all_problems():
    response = client.get("/api/problems")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_problem_by_id():
    response = client.get("/api/problems/two-sum")
    assert response.status_code == 200
    data = response.json()
    assert data["problem_id"] == "two-sum"
    assert "solutions" in data


def test_get_problem_by_id_not_found():
    response = client.get("/api/problems/nonexistent-problem")
    assert response.status_code == 404


def test_filter_problems_by_difficulty():
    response = client.get("/api/problems?difficulty=Easy")
    assert response.status_code == 200


def test_search_problems():
    response = client.get("/api/search?q=sum")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_problem_by_url():
    url = "https://leetcode.com/problems/two-sum/"
    response = client.get(f"/api/problems/by-url?url={url}")
    assert response.status_code == 200
    data = response.json()
    assert data["problem_id"] == "two-sum"


def test_get_problem_by_url_not_found():
    url = "https://leetcode.com/problems/fake/"
    response = client.get(f"/api/problems/by-url?url={url}")
    assert response.status_code == 404
