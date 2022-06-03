import cv2
from threading import Thread
import time
from controller import settings as settings_controller



class Camera(object):
    def __init__(self):

        # apply Initial configuration
        # TODO: Take initial configuration from env
        cam_init_para = { "exposure_auto" : 1, "white_balance_temperature_auto" : 0 }
        settings_controller.configure_camera(cam_init_para)

        self.stream_flag = False
        self.start_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        self.cap.release()

    def get_frame(self):
        _, frame = self.cap.read()
        self.frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def get_frame_in_byte(self):
        return cv2.imencode(".jpeg", self.frame)[1].tobytes()

    def write_frame(self, name):
        with open(name, "wb") as f:
            f.write(self.frame_bytes)

    def start_stream(self):
        self.stream_flag = True
        self.t = Thread(target=self.stream)
        self.t.start()

    def stream(self):
        while self.stream_flag:
            self.get_frame()

    def stop_stream(self):
        self.stream_flag = False
        self.t.join()


def get_last_capture_boolean(frame, last_capture_time, fps):
    if not frame or not last_capture_time:
        return True
    if time.time() - last_capture_time >= fps:
        return True
    return False
