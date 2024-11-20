from httpx import Response

from tests.conftest import client_generator


async def test_success_rediness():
    with client_generator() as client:
        response: Response = client.get("/health/readiness")
    assert response.status_code == 200


async def test_success_liveness():
    with client_generator() as client:
        response: Response = client.get("/health/liveness")
    assert response.status_code == 200
