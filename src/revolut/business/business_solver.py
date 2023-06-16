from storage.data import *

class businessSolver():

    def monitorThreeDs(self):
        
        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'Basic {self.authToken}',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }

        while True:

            time.sleep(self.monitorDelay)

            try:
                r = self.session.get("https://business-mobile.revolut.com/transaction/3ds", headers=headers)

                try:
                    
                    if "currency" in r.text:
                        Logger.normal("Found 3ds, solving...")
                        time.sleep(0.5)

                        try:
                            threeDsJson = json.loads(r.text)[0]

                            self.threeDsId = threeDsJson["id"]
                            self.threeDsCurrency = threeDsJson["currency"]
                            self.threeDsAmount = threeDsJson["amount"]
                            self.threeDsCardholderId = threeDsJson["id"]

                            try:
                                self.threeDsMerchantName = threeDsJson["merchant"]["name"]
                            except:
                                self.threeDsMerchantName = "Unknown"

                        except:
                            Logger.error("Error solving 3ds")
                            time.sleep(self.errorDelay)
                        
                        try:

                            self.acceptThreeDs()
                        
                        except:
                            Logger.error("Error in solve function")
                            time.sleep(self.errorDelay)
                    
                except:
                    pass

            except:
                Logger.error("Error sending 3ds request")
                time.sleep(self.errorDelay)

    def acceptThreeDs(self):
        
        headers = {
            'Host': 'business-mobile.revolut.com',
            'content-type': 'application/json',
            'Accept': '*/*',
            'Authorization': f'Basic {self.authToken}',
            'X-Client-Version': '3.58.1',
            'X-Timezone': 'Europe/Madrid',
            'Accept-Language': 'en-GB;q=1, en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'Revolut/com.revolut.business 3646 (iPhone; iOS 14.4.2; sp:AAS)',
            'X-device-id': self.deviceID,
            'X-device-model': 'iPhone9,3',
        }

        json_data = {
            'cardholder_id': self.threeDsCardholderId,
            'proceed': True,
            'id': self.threeDsCardholderId,
        }

        try:
            r = self.session.post("https://business-mobile.revolut.com/transaction/3ds", headers=headers, json=json_data)

            try:

                if r.status_code == 200 or r.status_code == 204:
                    Logger.success("Successfully solved 3ds!")
                
                else:
                    Logger.error(f"Error solving 3ds [{r.status_code}]")
                    time.sleep(self.errorDelay)
                
            except:
                Logger.error("Error getting response status code")
                time.sleep(self.errorDelay)
        
        except:
            Logger.error("Error sending solve request")
            time.sleep(self.errorDelay)
    
    def __init__(self) -> None:
        
        self.session = requests.Session()

        self.authToken = ""
        self.deviceID = ""
        
        self.monitorDelay = 5
        self.errorDelay = 10

        self.threeDsId = None
        self.threeDsCurrency = None
        self.threeDsAmount = None
        self.threeDsMerchantName = None
        self.threeDsCardholderId = None

        self.monitorThreeDs()
