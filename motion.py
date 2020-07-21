
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime
from utils import CredentialInfo
from message_payload import MessagePayload
<<<<<<< HEAD
from tf_classify import TFClassify
import json
import time
import signal, os, sys
=======
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259

#Define some globals
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
<<<<<<< HEAD
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
=======
device_client: IoTHubDeviceClient = IoTHubDeviceClient.create_from_connection_string(
    credentials.get_credentail_info(CredentialInfo.connection_string))

async def send_iot_message(message=""):
    message = MessagePayload.from_credentials(credentials)
    print(f"Sending message to IoT Hub: {message.get_message()}")
    await device_client.send_message(message.get_message())
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259

def movement_detected():
    global start_time
    print("Movement Detected!")
<<<<<<< HEAD
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
=======
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    camera.take_picture("img/", credentials.get_credentail_info(CredentialInfo.device_id))
    asyncio.run(send_iot_message())
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259

#No-movement detected method
def no_movement_detected():
    print("No movement...")
    red_led.off()
    
#Clean up
def destroy():
<<<<<<< HEAD
    tfclassifier = None
    camera = None
    GPIO.cleanup()  # Release GPIO resource
    
=======
    move_sensor.stop()
    red_led.stop()
    GPIO.cleanup()                     # Release GPIO resource

>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259
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
<<<<<<< HEAD
    signal.signal(signal.SIGINT, signal_handler)
=======
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259
    main_loop()
    

if __name__ == '__main__':     # Program entrance
    print('Starting...')
    try:
        startup()
<<<<<<< HEAD
    except SystemExit:  # Press ctrl-c to end the program.
=======

    except KeyboardInterrupt:  # Press ctrl-c to end the program.
>>>>>>> 55d4a60401e6205dea10b4a1be59abcef2d92259
        try:
            destroy()
        except: 
            pass


