import json
from pathlib import Path
from utils import CredentialInfo

class Credentials:
    def __init__(self):
        self.credsFile = 'creds.json'
        self.connection_string = ""
        self.device_id = ""
        self.latitude = ""
        self.longitude = ""
        self.owner_email = ""
        self.credential_dict = []
        self.read_credentials()

    #Reads the credentials from the creds.json file
    def read_credentials(self):
        filepath = Path(self.credsFile)
        try:
            with open(filepath) as cred_data:
                credentials = json.load(cred_data)
                self.connection_string = credentials['connection_string']
                self.device_id = credentials['device_id']
                self.longitude = credentials['longitude']
                self.latitude = credentials['latitude']
                self.owner_email = credentials['owner_email']
                self.credential_dict = credentials
        except Exception as e:
            print(f"There was an error reading credentials from: {self.credsFile}")

    def __str__(self) -> str:
        return f"Latigude: {self.latitude}, Longitude: {self.longitude}, Owner_Email: {self.owner_email}, Device_ID: {self.device_id}"

    #Get the specified credential info, using the Enum specified from the credentials.CredentialInfo class
    def get_credentail_info(self, credential_info:CredentialInfo) -> str:
        return self.credential_dict[credential_info]
