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


async def hw_command(request):
    print('Received synchronous call to blink')
    response = MethodResponse.create_from_method_request(
        request, status=200, payload={'description': f'Blinking LED every {request.payload} seconds'}
    )
    await device_client.send_method_response(response)  # send response
    print(f'Blinking LED every {request.payload} seconds')

device_commands = {
    'hello_world': hw_command,
}




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


