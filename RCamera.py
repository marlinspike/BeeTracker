from picamera import PiCamera
import asyncio
import uuid
from pathlib import Path


class RCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.cam_setup()

    #Set up some basic stuff like image size and rotation
    def cam_setup(self):
        #_camera = PiCamera()
        self.camera.rotation = 0
        self.camera.resolution = (2592,1944)

    #Takes a photo and saves it to the path specified, with the device_id specified as a prefix
    def take_picture(self, storage_location = "", device_id= ""):
        filepath = Path(
            f"{storage_location}{device_id}_{uuid.uuid1().__str__()}{'.jpg'}").__str__()
        self.camera.capture(filepath)
        #self.camera.capture('/var/www/html/' + uuid.uuid1().__str__() + '.jpg')
