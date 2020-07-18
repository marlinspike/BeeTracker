from picamera import PiCamera
import asyncio

class RCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.cam_setup()

    def cam_setup(self):
        #_camera = PiCamera()
        self.camera.rotation = 0
        self.camera.resolution = (2592,1944)

    def take_picture(self):
        self.camera.capture('/var/www/html/img.jpg')
