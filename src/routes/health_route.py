from fastapi import APIRouter
from loguru import logger

health_router = APIRouter(tags=["Health"])


@health_router.get(
    "/readiness",
    description="Эндпоинт у приложения, который будет говорить об успешном запуске и готов принимать трафик",
)
async def readiness() -> bool:
    logger.info("Readiness test success")
    return True


@health_router.get(
    "/liveness",
    description="Эндпоинт к которому будет ходить Kubernetes и проверять активность в процессе его "
    "работы, и если он перестанет корректно отвечать Kubernetes его перезапустит",
)
async def liveness() -> bool:
    logger.info("Liveness test success")
    return True
