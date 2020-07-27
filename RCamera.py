from picamera import PiCamera
import asyncio
import uuid
from pathlib import Path
from os import listdir
from os.path import isfile, join
import random

class RCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.cam_setup()

    #Set up some basic stuff like image size and rotation
    def cam_setup(self):
        #_camera = PiCamera()
        self.camera.rotation = 0
        self.camera.resolution = (640,480)#(2592,1944)

    def get_demo_pics(self) -> []:
        return [f for f in listdir("img_test/") if isfile(join("img_test/", f))]


    #Takes a photo and saves it to the path specified, with the device_id specified as a prefix
    #Returns: Picture name
    #use_demo_pics: Set to TRUE and this will simply return a filepath to a random picture in the img_test folder
    def take_picture(self, storage_location="", device_id="", use_demo_pics=False) -> str:
        filepath = ""
        if use_demo_pics:
            #"img/"
            filepath = Path(f"img_test/{random.choice(self.get_demo_pics())}").__str__()
        else:
            filepath = Path(f"{storage_location}{device_id}_{uuid.uuid4().__str__()}{'.jpg'}").__str__()
            self.camera.capture(filepath)
        
        return filepath



