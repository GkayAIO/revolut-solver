from storage.data import *
from revolut.x_device_id import gen_deviceid

class businessSessionGen():

    def init_login(self):
        
        Logger.normal("Starting Login...")

        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Basic YXBwOk44R3dTaW1yS0JMUFJQd1U=',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }
  
        json_data = {
            'email': self.email,
        }

        try:
            r = self.session.post("https://business-mobile.revolut.com/auth/verify", headers=headers, json=json_data)

            if r.status_code == 200:
                confirmUrl = input("Check your email and input the url: ")

                try:
                    signinBase64 = confirmUrl.split('SIGNIN&q=')[1].split('&isMagicLinkEmail')[0]
                    signinToken = base64.b64decode(signinBase64).decode('utf-8')
                    self.receivedCode = signinToken.split("|")[1]
                    return True

                except:
                    Logger.error("Error getting login token!")
                    time.sleep(self.errorDelay)
                    return False
            
            else:
                Logger.error("Error sending login email!")
                time.sleep(self.errorDelay)
                return False
        
        except:
            Logger.error("It looks like this email doesn't exist!")
            time.sleep(self.errorDelay)
            return False

    def confirmAccount(self):
        
        Logger.normal("Confirming account...")

        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Basic YXBwOk44R3dTaW1yS0JMUFJQd1U=',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }

        json_data = {
            'email': self.email,
            'code': self.receivedCode,
        }

        try:
            r = self.session.post("https://business-mobile.revolut.com/auth/confirm", headers=headers, json=json_data).json()

            try:
                accessToken = r["accessToken"]
                self.employeeID = r["employeeId"]
                authTokenBase64 = f"{str(self.employeeID)}:{str(accessToken)}"

                self.authToken = base64.b64encode(authTokenBase64.encode("utf-8")).decode('utf-8')
                return True

            except:
                Logger.error("Error getting auth token!")
                time.sleep(self.errorDelay)
                return False
            
        except:
            Logger.error("Error confirming your account!")
            time.sleep(self.errorDelay)
            return False

    def employeeAuth(self):
        
        Logger.normal("submitting password...")

        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'Basic {self.authToken}',
            'X-Verify-Password': self.password,
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }

        try:
            r = self.session.post("https://business-mobile.revolut.com/signin/auth", headers=headers, data={}).json()

            try:
                biometricAccessToken = r['biometricAccessToken']
                individualId = r['individualId']
                selfieAuthTokenBase64 = f"{str(individualId)}:{str(biometricAccessToken)}"

                self.selfieAuthToken = base64.b64encode(selfieAuthTokenBase64.encode("utf-8")).decode('utf-8')
                return True
            
            except:
                Logger.error("Error getting selfie auth token!")
                time.sleep(self.errorDelay)
                return False
            
        except:
            Logger.error(f"Error sending password request!")
            time.sleep(self.errorDelay)
            return False


    def selfiePost(self):
        
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
            'Host': 'business-mobile.revolut.com',
            'Accept': '*/*',
            'Authorization': f'Basic {self.selfieAuthToken}',
            'X-Verify-Password': self.password,
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }

        try:
            r = self.session.post("https://business-mobile.revolut.com/biometric/selfie/signin", headers=headers, file=file_payload).json()

            try:
                accessToken = r['accessToken']
                employeeID = r['employee']['id']
                authTokenBase64 = f"{str(employeeID)}:{str(accessToken)}"

                self.authTokenFinal = base64.b64encode(authTokenBase64.encode("utf-8")).decode('utf-8')
                return True

            except:
                Logger.error("Error getting auth token!")
                time.sleep(self.errorDelay)
                return False
            
        except:
            Logger.error("Error sending selfie file!")
            time.sleep(self.errorDelay)
            return False

    def saveData(self):
        userID = uuid.uuid4()
        with open(" CSV PATH HERE ", "a", newline="") as f:
            writer = csv.writer(f)
            data = [str(self.authTokenFinal), str(self.authToken), str(self.deviceID), str(self.employeeID), str(userID), str(self.email), str(self.profileName)]
            writer.writerow(data)
            f.close()

    def __init__(self) -> None:
        
        self.session = requests.Session()

        self.deviceID = gen_deviceid()
        self.authTokenFinal = None
        self.authToken = None
        self.employeeID = None
        self.receivedCode = None

        self.email = ""
        self.password = ""
        self.profileName = ""

        if self.init_login():
            if self.confirmAccount():
                if self.employeeAuth():
                    if self.selfiePost():
                        self.saveData()
                        Logger.success("Successfully generated session!")
