# (c) Meta Platforms, Inc. and affiliates. Confidential and proprietary.

import sys

sys.path.insert(0, "fastapi/app")

from app.main import app  # Import FastAPI instance
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_status():
    response = client.get("/device/status")
    assert response.status_code == 200
    assert response.json() == {
        "batteryLevel": "85%",
        "connected": True,
        "currentMode": "AR",
    }


def test_post_device_files():
    data = {
        "files_to_copy": [
            "testsample.vrs",
        ]
    }
    response = client.post("/device/copy-files/", json=data)
    assert response.status_code == 201


def test_delete_device_files():
    data = {"files_to_delete": ["file1", "file2"]}
    response = client.request("DELETE", "/device/delete-files/", json=data)
    assert response.status_code == 204
