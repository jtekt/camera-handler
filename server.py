from fastapi import FastAPI
from fastapi.responses import StreamingResponse, Response
from controller.camera import Camera
from uvicorn.main import Server


app = FastAPI()
can = Camera()
users = 0

@app.get("/")
def root():
    return {"message": "This is the root"}


@app.get("/frame")
async def frame():
    global can
    # print(f"Current stream flag: {can.stream_flag}")
    # if can.stream_flag:
    #     frame = can.get_frame_to_byte()
    # else:
    #     can.get_frame()
    #     frame = can.get_frame_to_byte()
    frame = can.get_frame_to_byte()
    return Response(content=frame, media_type="image/jpeg")


@app.get("/stream")
async def get_stream():
    return StreamingResponse(
        yield_stream(), media_type="multipart/x-mixed-replace; boundary=frame"
    )


def yield_stream():
    # # Users management
    # global users
    # users += 1
    # if users == 1:
    #     print("Starting stream")
    #     can.start_stream()

    # Get into looping
    try:
        while True:
            frame = can.get_frame_to_byte()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")
    except:
        # # Users management
        # users -= 1
        # if users == 0:
        #     print("Stopping stream")
        #     can.stop_stream()
        print("User Disconnected")
