from fastapi import APIRouter
from controller import camera_helper
from model.camera import Configuration

router = APIRouter(prefix="/settings")


@router.get("/")
async def get_camera_settings():
    settings = camera_helper.get_camera_settings()
    return settings


@router.patch("/")
async def configure_camera(configuration: Configuration = {}):
    configuration = configuration.dict(exclude_unset=True)

    if configuration:
        camera_helper.configure_camera(configuration)
    settings = camera_helper.get_camera_settings()
    return settings