# Bee Tracker
> An OpenHack codebase to support a Bee Health (mite) tracking IoT App

## Getting Started
### Installation of pre-requisites
Use the requirements.txt file to install required libraries, using the command: pip install -r requirements.txt

### Required hardware
- Raspberry Pi 0+
- Raspberry Pi PIR Motion Sensor
- Raspberry Pi Camera
- Some knowledge of how to use/configure a Raspberry Pi

### Azure Resources Required
- Azure IoT Hub: Your device will need to be enrolled, and it's connection string updated in the **creds.json** file discussed below
- Azure Storage: Optionally used to archive telemetry data from the device
- Azure Stream Analytics: Optionally used for telemetry analysis 

### Hardware wiring
The following wiring is required:
- LED light at GPIO 18
- Motion Sensor at GPIO 17
- Raspberry Pi Camera connected to the camera port

![alt text](https://raw.githubusercontent.com/marlinspike/beetracker/master/img/Raspberry_Pi_board_wiring.jpg)

### Configuring the Credentials file (creds.json)
This app needs a **creds.json** file to store certain required credential and status info. It's not contained in the repo for obvious reasons, but here's the structure you'll need:

```json
{
    "device_id" : "<device_id_here>",
    "latitude" : "<your_latitude_here>",
    "longitude" : "<your_longitude_here>",
    "owner_email" : "<your_email_here>",
    "blob_hostname" : "",
    "blob_container" : "img",
    "connection_string" : "<IoT_HUB_Connection_String>"
}
```
Save this in a file called **creds.json** in the root folder of the application.

## Running the app
Run the app using the command: python motion.py

