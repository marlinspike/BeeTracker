import json
from datetime import datetime
from credentials import Credentials
from utils import CredentialInfo

#Represents the payload for a message sent to IoT Hub. This data can then be analyzed/aggregated as needed
class MessagePayload:

    def __init__(self):
        self.dict_store = {}
        self.dict_store["time_logged"] = now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.dict_store["latitude"] = ""
        self.dict_store["longitude"] = ""
        self.dict_store["owner_email"] = ""
        self.dict_store["device_id"] = ""


    #Returns a MessagePayload object with properties loaded from the creds object passed
    def from_credentials(credential_info: Credentials) -> 'MessagePayload':
        payload = MessagePayload()
        payload.dict_store["latitude"] = credential_info.get_credentail_info(CredentialInfo.latitude)
        payload.dict_store["longitude"] = credential_info.get_credentail_info(
            CredentialInfo.longitude)
        payload.dict_store["owner_email"] = credential_info.get_credentail_info(
            CredentialInfo.owner_email)
        payload.dict_store["device_id"] = credential_info.get_credentail_info(
            CredentialInfo.device_id)
        return payload


    #Returns a JSON representation of the Message Payload
    def get_message(self) -> str:
        return json.dumps(self.dict_store)