import time


def get_last_capture_boolean(frame, last_capture_time, fps):
    if not frame or not last_capture_time:
        return True
    if time.time() - last_capture_time >= fps:
        return True
    return False