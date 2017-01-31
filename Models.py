from datetime import datetime


class UserModel:
    """
    Simple model to get user information
    """
    timestamp = datetime.now()
    creation_timestamp = "null"
    name = "unknown"
    email = "email@domain.com"
    registration_id = "some_id"
    external_code = "newUser"
    firebase_id = "firebase_id"
    email_path = "email_path"

    def __init__(self, data):
        try:
            self.timestamp = datetime.strptime(data[0], '%m/%d/%Y %H:%M:%S')
        except ValueError:
            print("Could not parse " + data[0])
        self.name = data[1].strip()
        self.email = data[2].strip()
        self.registration_id = data[3].strip()
        self.external_code = data[4].strip()
        self.firebase_id = data[5].strip()
        self.email_path = self.email.replace(".", "_").replace("@", "_")
        self.creation_timestamp = self.timestamp.strftime("%Y/%m/%d %H:%M:%S")
