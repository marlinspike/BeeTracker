import json
from pathlib import Path
from utils import CredentialInfo

class AppSettings:
    def __init__(self):
        self.appsettings_file = 'appsettings.json'
        self.TFLabels = ""
        self.appsettings_dict = {}
        self.read_credentials()
        self.version = ""
        self.date_time = ""


    #Reads the credentials from the creds.json file
    def read_credentials(self):
        #filepath = Path(self.credsFile)
        try:
            with open(Path(self.appsettings_file)) as cred_data:
                appsettings = json.load(cred_data)
                self.appsettings_dict = appsettings
        except Exception as e:
            print(f"There was an error reading appsettings from: {self.appsettings_file}")


    def __str__(self) -> str:
        return f"{self.TFLabels}"

    #Get the specified credential info, using the Enum specified from the credentials.CredentialInfo class
    def get_TFLabels(self) -> str:
        return [label.strip() for label in self.appsettings_dict["TFLabels"].split(",")]

    def get_Version(self) -> str:
        return self.appsettings_dict["Version"]

    def get_DateTime(self) -> str:
        return self.appsettings_dict["Date_Time"]


if __name__ == '__main__':
    app = AppSettings()
    labels = AppSettings().get_TFLabels()
    dt = AppSettings().get_DateTime()
    ver = AppSettings().get_Version()
    #labels = [label.strip() for label in app.get_TFLabels().split(",")]
    print(labels)
    print(ver)
    print(dt)
