 #IoT Device Registration and Connection Service
import asyncio
import os
import json
import datetime
import random

from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from azure.iot.device import Message
from credentials import Credentials
credentials: Credentials = Credentials()

async def register_device():
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host = credentials.provisioning_host,
        registration_id = credentials.registration_id,
        id_scope = credentials.id_scope,
        symmetric_key = credentials.symmetric_key)

    registration_result = await provisioning_device_client.register()
    print(f'Registration result: {registration_result.status}')
    return registration_result

#Connects device to IoT Central
async def connect_device() -> IoTHubDeviceClient:
    device_client = None
    try:
        registration_result = await register_device()
        if registration_result.status == 'assigned':
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key = credentials.symmetric_key,
            hostname = registration_result.registration_state.assigned_hub,
            device_id = registration_result.registration_state.device_id,
        )
        # Connect the client.
        await device_client.connect()
        print('Device connected successfully')
    finally:
        return device_client
