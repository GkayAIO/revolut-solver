from storage.data import *

class personalSolver():

    def monitorThreeDs(self):

        headers = {
            'Host': 'api.revolut.com',
            'authorization': f'Basic {self.authToken}',
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
        }

        while True:

            time.sleep(self.monitorDelay)

            try:
                r = self.session.get("https://api.revolut.com/transaction/3ds", headers=headers)

                try:
                    
                    if "currency" in r.text:
                        Logger.normal("Found 3ds, solving...")
                        time.sleep(0.5)

                        try:
                            threeDsJson = json.loads(r.text)[0]

                            self.threeDsId = threeDsJson["id"]
                            self.threeDsCurrency = threeDsJson["currency"]
                            self.threeDsAmount = threeDsJson["amount"]
                            self.threeDsCardholderId = threeDsJson["cardholder_id"]

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
            'Host': 'api.revolut.com',
            'content-type': 'application/json',
            'authorization': f'Basic {self.authToken}',
            'accept': '*/*',
            'x-client-version': '8.81',
            'x-timezone': 'Europe/Berlin',
            'accept-language': 'en-GB;q=1, en;q=0.9',
            'user-agent': 'Revolut/com.revolut.revolut 8.81 16147 (iPhone; iOS 14.0.1; sp:AAS)',
            'x-device-id': self.deviceID,
            'x-device-model': 'iPhone10,3',
        }

        json_data = {
            'proceed': True,
            'cardholder_id': self.threeDsCardholderId,
            'id': self.threeDsId,
        }

        try:
            r = self.session.post("https://api.revolut.com/transaction/3ds", headers=headers, json=json_data)

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
        self.threeDsCardholderId = None
        self.threeDsMerchantName = None

        self.monitorThreeDs()
