import cv2
from threading import Thread
import time
from controller import settings as settings_controller
import json
import os


class Camera(object):
    def __init__(self):

        # apply Initial configuration
        # TODO: Take initial configuration from env

        initial_settings_string = os.getenv('INITIAL_SETTINGS', '{ "exposure_auto" : 1, "white_balance_temperature_auto" : 0 }')
        initial_settings_dict = json.loads(initial_settings_string)
        settings_controller.configure_camera(initial_settings_dict)

        self.start()

    def start(self):
        self.cap = cv2.VideoCapture(0)

    def stop(self):
        self.cap.release()

    def get_frame(self):
        _, frame = self.cap.read()
        self.frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

    def get_frame_in_byte(self):
        return cv2.imencode(".jpeg", self.frame)[1].tobytes()

    def write_frame(self, name):
        # Currently unused
        with open(name, "wb") as f:
            f.write(self.frame_bytes)



def get_last_capture_boolean(frame, last_capture_time, fps):
    if not frame or not last_capture_time:
        return True
    if time.time() - last_capture_time >= fps:
        return True
    return False
