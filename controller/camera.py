import cv2
from threading import Thread
import time
import subprocess


class Camera(object):
    def __init__(self):
        self.stream_flag = False
        self.start_camera()

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


class CameraConfig(object):
    def get_camera_settings():

        command = "v4l2-ctl -d /dev/video0 -l"

        process = subprocess.run(
            command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        settings = {}

        for line in process.stdout.decode("utf-8").splitlines():
            key = line.split()[0]
            subproperties = line.split(": ")[1].split(" ")
            settings[key] = {}
            for property in subproperties:
                property_split = property.split("=")
                subkey = property_split[0]
                value = property_split[1]
                settings[key][subkey] = value

        return settings

    def configure_camera(args):

        command = "v4l2-ctl -d /dev/video0"

        for key in args:
            command = command + " -c {}={}".format(key, args[key])

        os.system(command)
