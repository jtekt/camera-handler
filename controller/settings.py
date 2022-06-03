import subprocess
import os


def get_camera_settings():

    command = "v4l2-ctl -d /dev/video0 -l"

    process = subprocess.run( command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )

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
