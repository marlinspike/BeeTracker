
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime
from utils import CredentialInfo

#Define some globals
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
device_client: IoTHubDeviceClient = IoTHubDeviceClient.create_from_connection_string(
    credentials.get_credentail_info(CredentialInfo.connection_string))

async def send_iot_message(message):
    print(f"Sending message to IoT Hub: {message}")
    await device_client.send_message(message)

def movement_detected():
    print("Movement Detected!")
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    camera.take_picture("img/", credentials.get_credentail_info(CredentialInfo.device_id))
    asyncio.run(send_iot_message(f"{now} - {credentials} - Movement Detected!"))

#No-movement detected method
def no_movement_detected():
    print("No movement...")
    red_led.off()
    
#Clean up
def destroy():
    move_sensor.stop()
    red_led.stop()
    GPIO.cleanup()                     # Release GPIO resource

#Main app loop.
def main_loop():
    while True:
        move_sensor.when_motion = movement_detected
        move_sensor.when_no_motion = no_movement_detected

def main():
    #device_client = IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
    asyncio.run(device_client.connect())


def startup():
    main()
    main_loop()

if __name__ == '__main__':     # Program entrance
    print('Starting...')
    try:
        startup()

    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        try:
            destroy()
        except: 
            pass


