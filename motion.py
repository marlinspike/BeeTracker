
import os
import signal
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
import app_logger
import sys, json, logging
import device_connect_service

#Define some globals
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
device_client: IoTHubDeviceClient = None #IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
start_time = datetime.now()
tfclassifier = TFClassify()
log:logging.Logger = app_logger.get_logger()
#print(f"TensorFlow took {datetime.now() - start_time} seconds to load")
log.info(f"TensorFlow took {datetime.now() - start_time} seconds to load")

async def send_iot_message(message=""):
    if message == "":
        message = MessagePayload.from_credentials(credentials)
        jsonified_message = message.get_message()
        message = jsonified_message
    log.info(f"Sending message to IoT Hub: {message}")
    await device_client.send_message(message)
    device_client.sent

def movement_detected():
    global start_time
    log.info("Movement Detected!")
    red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    picture_name = camera.take_picture("img/", credentials.get_credentail_info(CredentialInfo.device_id))
    tfclassifier.reset()
    tfclassifier.addImage(picture_name)
    start_time = datetime.now()
    picture_classification = tfclassifier.doClassify()
    log.info(f"Image Classification took {datetime.now() - start_time} seconds")
    #Only send telemetry if we see one of the classifications we care about; else, delete the photo
    if (picture_classification[0]['prediction'] in ["Honeybee", "Invader", "Male Bee"]):
        message = f"{json.dumps(picture_classification[0])}"
        asyncio.run(send_iot_message(message))
    else:
        if os.path.exists(picture_name):
            os.remove(picture_name)

#No-movement detected method
def no_movement_detected():
    log.info("No movement...")
    red_led.off()
    
#Clean up
def destroy():
    try:
        tfclassifier = None
        camera = None
        GPIO.cleanup()  # Release GPIO resource
    except Exception as e:
        log.info(f"Exiting..")
        sys.exit(0)
    
#Main app loop.
def main_loop():
    while True:
        try:
            move_sensor.when_motion = movement_detected
            move_sensor.when_no_motion = no_movement_detected
        except Exception:  # Press ctrl-c to end the program.
            destroy()

async def main():
    global device_client
    #device_client = IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
    start_time = datetime.now()
    device_client = await device_connect_service.connect_device()
    #asyncio.run(device_client.connect())
    log.info(f"Starting took {datetime.now() - start_time} seconds")
    log.info(f"Ready!")

#handles the CTRL-C signal
def signal_handler(signal, frame):
    destroy()
    sys.exit(0)

def startup():
    asyncio.run(main())
    signal.signal(signal.SIGINT, signal_handler)
    main_loop()
    

if __name__ == '__main__':     # Program entrance
    log.info('Starting...')
    try:
        startup()
    except SystemExit:  # Press ctrl-c to end the program.
        try:
            destroy()
        except: 
            pass


