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
        self.camera.resolution = (640,480)#(2592,1944)

    #Takes a photo and saves it to the path specified, with the device_id specified as a prefix
<<<<<<< HEAD
    #Returns: Picture name
    def take_picture(self, storage_location = "", device_id= "") -> str:
        filepath = Path(f"{storage_location}{device_id}_{uuid.uuid4().__str__()}{'.jpg'}").__str__()
        self.camera.capture(filepath)
        return filepath
=======
    def take_picture(self, storage_location = "", device_id= ""):
        filepath = Path(
            f"{storage_location}{device_id}_{uuid.uuid1().__str__()}{'.jpg'}").__str__()
        self.camera.capture(filepath)
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259
        #self.camera.capture('/var/www/html/' + uuid.uuid1().__str__() + '.jpg')
