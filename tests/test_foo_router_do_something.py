from typing import NoReturn, Any

import pytest
from httpx import Response

from src.services.foo_service import FooService
from tests.conftest import client_generator


@pytest.mark.parametrize(
    "request_json",
    [
        {
            "text": "Что-то очень страшное",
            "outerContext": {
                "sex": "мужчина",
                "age": 20,
                "userId": "111",
                "sessionId": "1111",
                "clientId": "TestCase1",
            },
        },
        {
            "text": "что-то еще страшное",
            "outerContext": {
                "sex": "мужчина",
                "age": 20,
                "userId": "111",
                "sessionId": "111",
                "clientId": "TestCase1",
            },
        },
        {
            "text": "Новая сессия?",
            "outerContext": {
                "sex": "женщина",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
        {
            "text": "Что-то очень страшное в новой сессии",
            "outerContext": {
                "sex": "женщина",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
    ],
)
async def test_success(request_json: dict) -> None:
    with client_generator() as client:
        response: Response = client.post("/v1/do_something", json=request_json)
    assert response.status_code == 200
    response_dict: dict = response.json()
    assert response_dict["boo"] == request_json["text"]
    text: str = f"request.outer_context.user_id='{request_json['outerContext']['userId']}'"
    assert response_dict["some"]["foo"] == text
    text = f"request.outer_context.session_id='{request_json['outerContext']['sessionId']}'"
    assert response_dict["some"]["boo"] == text
    assert 0 <= response_dict["doo"] <= 10
    assert not not response_dict["uniqId"]


@pytest.mark.parametrize(
    "request_json",
    [
        {
            "outerContext": {
                "sex": "мужчина",
                "age": 20,
                "userId": "111",
                "sessionId": "1111",
                "clientId": "TestCase1",
            },
        },
        {
            "Text": "что-то еще страшное",
        },
        {
            "foo": "Новая сессия?",
            "outerContext": {
                "sex": "женщина",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
        {
            "text": "Что-то очень страшное в новой сессии",
            "outerContext": {
                "sex": "М",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
        {},
    ],
)
async def test_incorrect_request(request_json: dict) -> None:
    with client_generator() as client:
        response: Response = client.post("/v1/do_something", json=request_json)
    assert response.status_code == 422
    response_dict: dict = response.json()["detail"][0]
    assert not not response_dict["type"]
    assert len(response_dict["loc"]) > 0
    assert not not response_dict["msg"]


@pytest.mark.parametrize(
    "request_json",
    [
        {
            "text": "Что-то очень страшное",
            "outerContext": {
                "sex": "мужчина",
                "age": 20,
                "userId": "111",
                "sessionId": "1111",
                "clientId": "TestCase1",
            },
        },
        {
            "text": "что-то еще страшное",
            "outerContext": {
                "sex": "мужчина",
                "age": 20,
                "userId": "111",
                "sessionId": "111",
                "clientId": "TestCase1",
            },
        },
        {
            "text": "Новая сессия?",
            "outerContext": {
                "sex": "женщина",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
        {
            "text": "Что-то очень страшное в новой сессии",
            "outerContext": {
                "sex": "женщина",
                "age": 90,
                "userId": "222",
                "sessionId": "2222",
                "clientId": "TestCase2",
            },
        },
    ],
)
async def test_500_exception(monkeypatch, request_json: dict[str, Any]):
    def mocked_do_something(*args, **kwargs) -> NoReturn:
        raise IndexError("Oooops")

    monkeypatch.setattr(FooService, "do_something", value=mocked_do_something)
    with client_generator() as client:
        response: Response = client.post("/v1/do_something", json=request_json)
    assert response.status_code == 500
    resp_error: dict[str, str] = response.json()
    assert resp_error["name"] == "IndexError"
