from typing import NoReturn

import pytest

from httpx import Response

from src.configuration.config.config import config
from src.services.foo_service import FooService
from .conftest import client_generator


@pytest.mark.parametrize(
    "id_",
    [i for i in range(10)],
)
def test_try_luck_high_chance(monkeypatch, id_: int):
    monkeypatch.setattr(config, "chance", value=1)
    with client_generator() as client:
        response: Response = client.get("/v1/try_luck")
    assert response.status_code == 200
    assert "You are lucky ass" in response.text, f"Failed {id_=}"


@pytest.mark.parametrize(
    "id_",
    [i for i in range(10)],
)
def test_try_luck_low_chance(monkeypatch, id_: int):
    monkeypatch.setattr(config, "chance", value=0)
    with client_generator() as client:
        response: Response = client.get("/v1/try_luck")
    assert response.status_code == 418, f"Failed {id_=}"
    assert response.json()["description"] == "Бу, испугался? Да ты не бойся. You lose ha-ha-ha"


@pytest.mark.parametrize(
    "id_",
    [i for i in range(10)],
)
def test_500_exception(monkeypatch, id_: int):
    def mocked_try_luck(*args, **kwargs) -> NoReturn:
        raise IndexError("Oooops")

    monkeypatch.setattr(FooService, "try_luck", value=mocked_try_luck)
    with client_generator() as client:
        response: Response = client.get("/v1/try_luck")
    assert response.status_code == 500
    resp_error: dict[str, str] = response.json()
    assert resp_error["name"] == "IndexError"
