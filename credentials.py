import json

class Credentials:
    def __init__(self):
        self.credsFile = './creds.json'
        self.connection_string = ""
        self.device_id = ""
        self.read_credentials()

    def read_credentials(self):
        try:
            with open(self.credsFile) as cred_data:
                credentials = json.load(cred_data)
                self.connection_string = credentials['connection_string']
                self.device_id = credentials['device_id']
        except Exception as e:
            print(f"There was an error reading credentials from: {self.credsFile}")

    def __str__(self):
        return f"Connection_String: {self.connection_string}, Device_ID: {self.device_id}"

    def get_connection_string(self):
        return self.connection_string
    
    def get_device_id(self):
        return self.device_id