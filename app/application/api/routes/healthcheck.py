from fastapi import APIRouter, status

from models.healthcheck import HealthCheck

router = APIRouter()


@router.get(
    "",
    tags=["healthcheck"],
    summary="Performed healthcheck",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_healthcheck() -> HealthCheck:
    return HealthCheck(status="OK")