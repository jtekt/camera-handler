from fastapi import Header, Cookie, APIRouter
from controller.camera import Camera, get_last_capture_boolean
from typing import Optional
from fastapi.responses import StreamingResponse, Response
import time

# Router
router = APIRouter(prefix="")

# Camera initialization
can = Camera()

# Initialization
frame = None
last_capture_time = None
fps = 2


@router.get("/")
def root():
    return dict(
        application_name="Camera handler",
        version="1.0.0",
        author="Maxime MOREILLON",
        camera_opened=can.cap.isOpened(),
    )


@router.get("/start")
async def start_camera():
    try:
        if can.cap.isOpened():
            return {"message": "Camera is already opened"}
        can.start_camera()
        return {"message": "Camera has been started"}
    except Exception as e:
        return {"message": "Camera start failed", "detail": str(e)}


@router.get("/stop")
async def stop_camera():
    try:
        can.stop_camera()
        return {"message": "Camera has been stopped"}
    except Exception as e:
        return {"message": "Camera stop failed", "detail": str(e)}


@router.get("/frame")
async def frame():
    global frame, last_capture_time
    can.get_frame()
    frame = can.get_frame_in_byte()
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
                can.get_frame()
                frame = can.get_frame_in_byte()
                last_capture_time = time.time()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    except:
        print("User Disconnected")
