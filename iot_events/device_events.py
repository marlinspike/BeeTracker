import RPi.GPIO as GPIO
from RCamera import RCamera
import app_logger
import logging
from credentials import Credentials
from utils import CredentialInfo
from gpiozero import MotionSensor, LED
from tf_classify import TFClassify
from datetime import datetime
import sys, json, asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from iotc.aio import IoTCClient
from iotc import IOTCConnectType, IOTCLogLevel, IOTCEvents

log: logging.Logger = app_logger.get_logger()


            
async def send_iot_message(device_client: IoTCClient, message=""):
    global log
    if message == "":
        message = MessagePayload.from_credentials(credentials)
        jsonified_message = message.get_message()
        message = jsonified_message
    log.info(f"Sending message to IoT Hub: {message}")
    #await device_client.send_message(message)
    if device_client.connected:
        await device_client.send_message(message)
        #await device_client.send_telemetry(message)


async def on_props(propName, propValue):
    print(propValue)
    return True


async def on_commands(command, ack):
    print(command.name)
    await ack(command.name, 'Command received', command.request_id)


async def on_enqueued_commands(command_name, command_data):
    print(command_name)
    print(command_data)
