from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from controller.camera import Camera, get_camera_settings
from controller.logics import get_last_capture_boolean
import time

# App initialization
app = FastAPI()
frame = None
last_capture_time = None
fps = 1
# users = 0

# Camera initialization
can = Camera()


@app.get("/")
def root():
    return dict(
        application_name="Camera handler",
        version="1.0.0",
        author="Maxime MOREILLON",
        camera_opened=can.cap.isOpened(),
    )


@app.get("/frame")
async def frame():
    global frame, last_capture_time
    can.get_frame()
    frame = can.get_frame_in_byte()
    last_capture_time = time.time()
    return Response(content=frame, media_type="image/jpeg")


@app.get("/stream")
async def get_stream():
    return StreamingResponse(
        yield_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/camera/restart")
async def restart():
    try:
        can.stop_camera()
        can.start_camera()
        return {"message": "Camera has been restarted"}
    except Exception as e:
        return {"message": "Camera restart failed", "detail": str(e)}


@app.get("/camera/settings")
async def camera_settings():
    settings = get_camera_settings()
    return settings


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
