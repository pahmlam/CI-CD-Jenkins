import os
import sys

import pytest
from fastapi.testclient import TestClient


# Thêm thư mục src vào PYTHONPATH
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src")
)

from app import app, load_model


# Load model trước khi chạy test
load_model()

# Tạo test client
client = TestClient(app)


# ======================
# Tests
# ======================

def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data
    assert data["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict():
    test_input = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }

    response = client.post("/predict", json=test_input)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "class_name" in data
    assert "confidence" in data

    assert data["class_name"] in [
        "setosa",
        "versicolor",
        "virginica"
    ]

    assert 0 <= data["confidence"] <= 1


def test_predict_invalid_input():
    invalid_input = {
        "sepal_length": 5.1,
        "sepal_width": 3.5
        # thiếu petal_length và petal_width
    }

    response = client.post("/predict", json=invalid_input)

    # FastAPI sẽ trả lỗi validation
    assert response.status_code == 422


# ======================
# Run tests
# ======================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
