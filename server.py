from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from controller.camera import Camera
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
    return {"message": "This is the root"}


@app.get("/frame")
async def frame():
    global frame, last_capture_time
    frame = can.get_frame_in_byte()
    last_capture_time = time.time()
    return Response(content=frame, media_type="image/jpeg")


@app.get("/stream")
async def get_stream():
    return StreamingResponse(
        yield_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


@app.get("/restart")
async def restart():
    try:
        can.stop_camera()
        can.start_camera()
        return {"message": "Camera has been restarted"}
    except Exception as e:
        return {"message": "Camera restart failed", "detail": str(e)}


def yield_stream():
    global frame, last_capture_time, fps

    # Get into looping
    try:
        while True:
            if get_last_capture_boolean(frame, last_capture_time, fps):
                frame = can.get_frame_in_byte()
                last_capture_time = time.time()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    except:
        print("User Disconnected")
