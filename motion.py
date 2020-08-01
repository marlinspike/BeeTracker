import RPi.GPIO as GPIO
from gpiozero import MotionSensor, LED
from RCamera import RCamera
from credentials import Credentials
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime
from utils import CredentialInfo
from message_payload import MessagePayload
from tf_classify import TFClassify
import sys, json, logging, argparse, app_logger, asyncio, signal, os
import device_connect_service
from iotc.aio import IoTCClient
from iotc import IOTCConnectType, IOTCLogLevel, IOTCEvents
import iot_events.device_events as device_events
from app_settings import AppSettings
import iot_events.iot_commands as iot_commands

#Define some globals
GPIO.setmode(GPIO.BCM)
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
device_client: IoTCClient = None #IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
start_time = datetime.now()
tfclassifier = TFClassify()
log:logging.Logger = app_logger.get_logger()
#print(f"TensorFlow took {datetime.now() - start_time} seconds to load")
log.info(f"TensorFlow took {datetime.now() - start_time} seconds to load")
_app_settings = AppSettings()
_USE_TEST_MODE = False
#These commands are sent by IoT Central to the device

_IoT_Commands = {
    'DownloadModel': iot_commands.iot_download_model,
    'UploadImages': iot_commands.iot_upload_images,
    'Blink': iot_commands.iot_blink
}

async def send_iot_message(message=""):
    await device_events.send_iot_message(device_client, message)

def movement_detected():
    global start_time, _USE_TEST_MODE
    log.info("Movement Detected!")
    red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    picture_name = camera.take_picture("img/", credentials.get_credentail_info(CredentialInfo.device_id), _USE_TEST_MODE)
    tfclassifier.reset()
    tfclassifier.addImage(picture_name)
    start_time = datetime.now()
    picture_classification = tfclassifier.doClassify()
    log.info(f"Image Classification took {datetime.now() - start_time} seconds")
    #Only send telemetry if we see one of the classifications we care about; else, delete the photo
    valid_labels = _app_settings.get_TFLabels() # Labels classified
    if ((picture_classification[0]['Prediction'] in valid_labels)): #["Honeybee", "Invader", "Male Bee"]):
        message = f"{picture_classification[0]}"
        asyncio.run(send_iot_message(message))
    if ((picture_classification[0]['Confidence'] > 0.60) and _USE_TEST_MODE == False):
        if os.path.exists(picture_name):
            os.remove(picture_name)

#No-movement detected method
def no_movement_detected():
    log.info("No movement...")
    red_led.off()
    

#Main app loop.
async def main_loop():
    global _IoT_Commands
    global device_client

    try:
        device_client = await device_connect_service.connect_iotc_device()
        move_sensor.when_motion = movement_detected
        move_sensor.when_no_motion = no_movement_detected
    except Exception as e:
        pass

    while True:
        try:
            method_request = await device_client.receive_method_request()
            await _IoT_Commands[method_request.name](method_request, device_client, credentials)
        except KeyboardInterrupt as kbi:
            GPIO.cleanup()
            sys.exit(0)           
        except Exception as e:  # Press ctrl-c to end the program.
            log.error("Exception in main_loop: {e}")
            GPIO.cleanup()
            sys.exit(0)
    try:
        destroy()
    except Exception as e:
        pass


def startup():
    asyncio.run(main_loop())
    
if __name__ == '__main__':  
    log.info('Starting...')
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', required=False)
    args = parser.parse_args()
    _USE_TEST_MODE = args.test
    if (_USE_TEST_MODE):
        log.info("Starting in TEST Mode")

    try:
        startup()
    except SystemExit: 
        try:
            destroy()
        finally:
            GPIO.cleanup()
            sys.exit(0)



