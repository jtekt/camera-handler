import cv2
from threading import Thread
import time


class Camera(object):
    def __init__(self):
        self.stream_flag = False
        self.start_camera()
        self.start_stream()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)

    def stop_camera(self):
        self.cap.release()

    def get_frame(self):
        _, self.frame = self.cap.read()

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
