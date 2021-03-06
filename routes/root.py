from fastapi import Header, Cookie, APIRouter
from controller.camera import Camera, get_last_capture_boolean
from controller import settings as settings_controller
from validation.settings import Configuration
from typing import Optional
from fastapi.responses import StreamingResponse, Response
import time
import os

# Router
router = APIRouter(prefix="")

# Camera initialization
cam = Camera()

# Initialization
frame = None
last_capture_time = None
fps = 1.00 / float(os.getenv('FPS', 2.0)) # Not FPS, frequency


@router.get("/")
def root():
    return dict(
        application_name="Camera handler",
        version="1.0.3",
        author="Justin YEOH, Maxime MOREILLON, Bun KAN",
        camera_opened=cam.cap.isOpened(),
    )


@router.get("/start")
async def start_camera():
    try:
        if cam.cap.isOpened():
            return {"message": "Camera is already opened"}
        cam.start()
        return {"message": "Camera has been started"}
    except Exception as e:
        return {"message": "Camera start failed", "detail": str(e)}


@router.get("/stop")
async def stop_camera():
    try:
        cam.stop()
        return {"message": "Camera has been stopped"}
    except Exception as e:
        return {"message": "Camera stop failed", "detail": str(e)}


@router.get("/frame")
async def frame():
    global frame, last_capture_time
    cam.get_frame()
    frame = cam.get_frame_in_byte()
    last_capture_time = time.time()
    return Response(content=frame, media_type="image/jpeg")


@router.get("/stream")
async def get_stream():
    return StreamingResponse(
        yield_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def yield_stream():
    global frame, last_capture_time, fps

    # Get into looping
    try:
        while True:
            if get_last_capture_boolean(frame, last_capture_time, fps):
                cam.get_frame()
                frame = cam.get_frame_in_byte()
                last_capture_time = time.time()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    except:
        print("User Disconnected")


@router.get("/settings")
async def get_camera_settings():
    settings = settings_controller.get_camera_settings()
    return settings


@router.patch("/settings")
async def configure_camera(configuration: Configuration = {}):
    configuration = configuration.dict(exclude_unset=True)
    # print (configuration)
    if configuration:
        settings_controller.configure_camera(configuration)
    settings = settings_controller.get_camera_settings()
    return settings
