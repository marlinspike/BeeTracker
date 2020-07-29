
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
import adafruit_vcnl4010
import time
import busio
import board
import Adafruit_VCNL40xx
import iot_events.iot_commands as iot_commands
from azure.storage.blob import ContainerClient


#Define some globals
move_sensor = MotionSensor(17)  #Motion Sensor control connected to GPIO pin 17
#red_led = LED(18)   #LED connected to GPIO pin 18
camera = RCamera()  #Camera connected to camera pins
credentials: Credentials = Credentials()
device_client: IoTCClient = None #IoTHubDeviceClient.create_from_connection_string(credentials.get_credentail_info(CredentialInfo.connection_string))
start_time = datetime.now()
tfclassifier = TFClassify()
log:logging.Logger = app_logger.get_logger()
#print(f"TensorFlow took {datetime.now() - start_time} seconds to load")
log.info(f"TensorFlow took {datetime.now() - start_time} seconds to load")
_USE_TEST_MODE = False
# Proxmity Sensor i2c
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vcnl4010.VCNL4010(i2c)
# List for calibration
motionSense=[]
percent = None
vcnl = Adafruit_VCNL40xx.VCNL4010()
_app_settings = AppSettings()
#These commands are sent by IoT Central to the device
_IoT_Commands = {
    'DownloadModel': iot_commands.iot_download_model,
    'UploadImages': iot_commands.iot_upload_images,
    'Blink': iot_commands.iot_blink
}


async def send_iot_message(message=""):
    await device_events.send_iot_message(device_client, message)


# Calibrate the proximity sensor
def calibratePSensor():
    print("Calibrating Proximity Sensor...")
    for i in range (3):
        proximity = sensor.proximity
        #proximity = vcnl.read_proximity()
        print("Proximity: {0}".format(proximity))
        motionSense.append(proximity)
        time.sleep(1)

    avg = sum(motionSense) / len(motionSense)
    print("Average Proximity: " + str(avg))
    # Increase average proximity by 2% as "motion"
    percent = avg + (avg * .02)
    print("Plus 2%: " + str(percent))
    return percent

async def movement_detected():
    global start_time, _USE_TEST_MODE
    log.info("Movement Detected!")
    #red_led.on()
    # Take a picture and save it to the folder specified; "" for current folder
    pic_folder = 'img/'
    device_id = credentials.get_credentail_info(CredentialInfo.device_id)
    picture_name = camera.take_picture(pic_folder, device_id, _USE_TEST_MODE)
    log.info("Took picture via device '%s': '%s'", device_id, picture_name)
    tfclassifier.reset()
    tfclassifier.addImage(picture_name)
    start_time = datetime.now()
    picture_classification = tfclassifier.doClassify()
    log.info(f"Image Classification took {datetime.now() - start_time} seconds")
    #Only send telemetry if we see one of the classifications we care about; else, delete the photo
    valid_labels = _app_settings.get_TFLabels() # Labels classified
    if ((picture_classification[0]['Prediction'] in valid_labels)): #["Honeybee", "Invader", "Male Bee"]):
        message = f"{picture_classification[0]}"
        #asyncio.run(send_iot_message(message))
        await send_iot_message(message)
    if ((picture_classification[0]['Confidence'] >1) and _USE_TEST_MODE == False):
        if os.path.exists(picture_name):
            os.remove(picture_name)

#No-movement detected method
async def no_movement_detected():
    log.info("No movement...")
    #red_led.off()

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
async def main_loop():
    global device_client
    global percent
    global proximity
    global _IoT_Commands
    device_client = await device_connect_service.connect_iotc_device()

    while True:
        try:
            proximity = vcnl.read_proximity()
            if proximity >= percent:
                await movement_detected()
            #method_request = await device_client.receive_method_request()
            #await _IoT_Commands[method_request.name](method_request, device_client, credentials)
        except Exception as e:  # Press ctrl-c to end the program.
            log.error("Exception in main_loop: {e}")
            break
    destroy()

async def main():
    global percent
    # Calibrate the proximity sensor
    percent = calibratePSensor()

    global device_client
    start_time = datetime.now()
    log.info(f"Ready! Starting took {datetime.now() - start_time} seconds")

#handles the CTRL-C signal
def signal_handler(signal, frame):
    destroy()
    sys.exit(0)

def startup():
    asyncio.run(main())
    signal.signal(signal.SIGINT, signal_handler)
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
            sys.exit(0)

