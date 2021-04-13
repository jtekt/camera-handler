from fastapi import Header, Cookie, APIRouter
from controller.camera import Camera
from typing import Optional
from fastapi.responses import StreamingResponse, Response
from controller.logics import get_last_capture_boolean
import time

# Router
router = APIRouter(prefix="")

# Camera initialization
can = Camera()

# Initialization
frame = None
last_capture_time = None
fps = 1


@router.get("/")
def root():
    return dict(
        application_name="Camera handler",
        version="1.0.0",
        author="Maxime MOREILLON",
        camera_opened=can.cap.isOpened(),
    )


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