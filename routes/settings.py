from fastapi import APIRouter
from controller import settings as settings_controller
from validation.settings import Configuration

router = APIRouter(prefix="/settings")


@router.get("/")
async def get_camera_settings():
    settings = settings_controller.get_camera_settings()
    return settings


@router.patch("/")
async def configure_camera(configuration: Configuration = {}):
    configuration = configuration.dict(exclude_unset=True)

    if configuration:
        settings_controller.configure_camera(configuration)
    settings = settings_controller.get_camera_settings()
    return settings