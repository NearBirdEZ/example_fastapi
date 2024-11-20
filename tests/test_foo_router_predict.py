from typing import NoReturn, Any

import pytest
from httpx import Response

from src.services.foo_service import FooService
from tests.conftest import client_generator


@pytest.mark.parametrize(
    "request_json",
    [{"seed": i} for i in range(10)],
)
async def test_success(request_json: dict) -> None:
    with client_generator() as client:
        response: Response = client.post("/v1/predict", json=request_json)
    assert response.status_code == 200
    response_dict: dict = response.json()
    assert 1 >= response_dict["predictedNumber"] >= 0
    assert not not response_dict["uniqId"]


@pytest.mark.parametrize(
    "request_json",
    [{"seed": "Один"}, {"": 9}, {"Один": "seed"}, {}, {"foo": "boo"}],
)
async def test_incorrect_request(request_json: dict) -> None:
    with client_generator() as client:
        response: Response = client.post("/v1/predict", json=request_json)
    assert response.status_code == 422
    response_dict: dict = response.json()["detail"][0]
    assert not not response_dict["type"]
    assert len(response_dict["loc"]) > 0
    assert not not response_dict["msg"]


@pytest.mark.parametrize(
    "request_json",
    [{"seed": i} for i in range(10)],
)
async def test_500_exception(monkeypatch, request_json: dict[str, Any]):
    def mocked_predict(*args, **kwargs) -> NoReturn:
        raise IndexError("Oooops")

    monkeypatch.setattr(FooService, "predict", value=mocked_predict)
    with client_generator() as client:
        response: Response = client.post("/v1/predict", json=request_json)
    assert response.status_code == 500
    resp_error: dict[str, str] = response.json()
    assert resp_error["name"] == "IndexError"
