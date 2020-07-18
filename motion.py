
import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient

#Define some globals
move_sensor = MotionSensor(17)
red_led = LED(18)
camera = RCamera()
credentials: Credentials = Credentials()
device_client: IoTHubDeviceClient = None


def movement_detected():
    print("Movement Detected!")
    camera.take_picture()
    red_led.on()

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

async def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(credentials.get_connection_string())
    await device_client.connect()


async def startup():
    await main()
    main_loop()

if __name__ == '__main__':     # Program entrance
    print('Starting...')
    try:
        asyncio.run(startup())

    except KeyboardInterrupt:  # Press ctrl-c to end the program.
        try:
            destroy()
        except: 
            pass


