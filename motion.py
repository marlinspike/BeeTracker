
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime

#Define some globals
move_sensor = MotionSensor(17)
red_led = LED(18)
camera = RCamera()
credentials: Credentials = Credentials()
device_client: IoTHubDeviceClient = IoTHubDeviceClient.create_from_connection_string(
    credentials.get_connection_string())

async def send_iot_message(message):
    print("Sending messagae...")
    await device_client.send_message(message)

def movement_detected():
    print("Movement Detected!")
    now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    red_led.on()
    camera.take_picture()
    asyncio.run(send_iot_message(f"{now} - Movement Detected!"))


def no_movement_detected():
    print("No movement...")
    red_led.off()
    

def destroy():
    move_sensor.stop()
    red_led.stop()
    GPIO.cleanup()                     # Release GPIO resource

def main_loop():
    while True:
        move_sensor.when_motion = movement_detected
        move_sensor.when_no_motion = no_movement_detected

def main():
    #device_client = IoTHubDeviceClient.create_from_connection_string(credentials.get_connection_string())
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


