from storage.data import *
from revolut.x_device_id import gen_deviceid

class personalSessionGen():

    def init_login(self):
        
        Logger.normal("Starting Login...")

        headers = {
            'Host': 'api.revolut.com',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
        }
        json_data = {
            'password': self.password,
            'phone': self.phonenumber,
        }

        try:
            r = self.session.post("https://api.revolut.com/signin", headers=headers, json=json_data)
            if r.status_code == 400:
                Logger.error("Device outdated")
                return False
            else:
                self.confirm_url = input("Input the sms code: ")
                return True
        except:
            Logger.error("Invalid Information / Account blocked")
            return False

    def confirmAccount(self):
        
        Logger.normal("Confirming SMS code...")

        headers = {
            'Host': 'api.revolut.com',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
        }
        json_data = {
            'phone': self.phonenumber,
            'code': self.confirm_url,
            'password': self.password,
        }
        
        try:
            r = self.session.post("https://api.revolut.com/signin", headers=headers, json=json_data).json()
            try:
                userID = r["user"]["id"]
                accesscode = r["token"]["accessCode"]
                authToken64 = f"{str(userID)}:{str(accesscode)}"
                self.selfieAuthToken = base64.b64encode(authToken64.encode("utf-8")).decode("utf-8")
                return True
            except:
                Logger.error("Error getting authentication Token!")
                return False
        except:
            Logger.error("Error confirming your account!")
            return False

    def postSelfie(self):
        
        Logger.normal("Submitting selfie...")

        try:
            file = open(" PATH TO SELFIE ", "rb")
        except:
            Logger.error("Selfie path doesn't exist")
            return False
        
        file_payload = {
            'selfie': file,
        }
        headers = {
            'Host': 'api.revolut.com',
            'authorization': f'Basic {self.selfie_auth_token}', 
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'cache-control': 'no-cache',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
        }
        try:
            r = self.session.post("https://api.revolut.com/biometric-signin/selfie", headers=headers, files=file_payload).json()
            try:
                self.userID = r["id"]
                return True
            except:
                Logger.error("Error getting ID")
                return False
        except:
            Logger.error("Error logging in!")
            return False

    def confirmSelfie(self):
        
        headers = {
            'Host': 'api.revolut.com',
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'authorization': f'Basic {self.selfie_auth_token}',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
            'content-type': 'application/x-www-form-urlencoded',
        }

        try:
            r = self.session.post("f'https://api.revolut.com/biometric-signin/confirm/"+self.userID, headers=headers).json()
            try:
                accessCode = r["token"]["accessCode"]
                userID = r["user"]["id"]
                authToken64 = f"{str(userID)}:{str(accessCode)}"
                self.authToken = base64.b64encode(authToken64.encode("utf-8")).decode("utf-8")
                return True
            except:
                Logger.error("Error getting selfie confirmation Tokens")
                return False
        except:
            Logger.error("Error confirming Selfie!")
            return False

    def saveData(self):
        userID = uuid.uuid4()
        with open(" CSV PATH HERE ", "a", newline="") as f:
            writer = csv.writer(f)
            data = [str(userID), str(self.authToken), str(self.deviceID), str(self.email), str(self.profileName)]
            writer.writerow(data)
            f.close()

    def __init__(self) -> None:
        
        self.session = requests.Session()

        self.deviceID = gen_deviceid()
        self.phonenumber = ""
        self.password = ""
        self.email = ""
        self.profileName = ""

        if self.init_login():
            if self.confirmAccount():
                if self.postSelfie():
                    if self.confirmSelfie():
                        self.saveData()
                        Logger.success("Successfully generated session!")
