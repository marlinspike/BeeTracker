
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime
from utils import CredentialInfo
from message_payload import MessagePayload
from tf_classify import TFClassify
import json
import time
import signal, os, sys


#Define some globals
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
device_client: IoTHubDeviceClient = IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
start_time = time.time()
tfclassifier = TFClassify()
print(f"TensorFlow took {time.time() - start_time} seconds to load")

async def send_iot_message(message=""):
    if message == "":
        message = MessagePayload.from_credentials(credentials)
        jsonified_message = message.get_message()
        message = jsonified_message
    print(f"Sending message to IoT Hub: {message}")
    await device_client.send_message(message)

def movement_detected():
    global start_time
    print("Movement Detected!")
    red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    picture_name = camera.take_picture("img/", credentials.get_credentail_info(CredentialInfo.device_id))
    tfclassifier.reset()
    tfclassifier.addImage(picture_name)
    start_time = time.time()
    picture_classification = tfclassifier.doClassify()
    print(f"Image Classification took {time.time() - start_time} seconds")
    message = f"{json.dumps(picture_classification[0])}"
    asyncio.run(send_iot_message(message))


#No-movement detected method
def no_movement_detected():
    print("No movement...")
    red_led.off()
    
#Clean up
def destroy():
    tfclassifier = None
    camera = None
    GPIO.cleanup()  # Release GPIO resource
    
#Main app loop.
def main_loop():
    while True:
        try:
            move_sensor.when_motion = movement_detected
            move_sensor.when_no_motion = no_movement_detected
        except Exception:  # Press ctrl-c to end the program.
            destroy()

def main():
    #device_client = IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
    asyncio.run(device_client.connect())

#handles the CTRL-C signal
def signal_handler(signal, frame):
    destroy()
    sys.exit(0)

def startup():
    main()
    signal.signal(signal.SIGINT, signal_handler)
    main_loop()
    

if __name__ == '__main__':     # Program entrance
    print('Starting...')
    try:
        startup()
    except SystemExit:  # Press ctrl-c to end the program.
        try:
            destroy()
        except: 
            pass


