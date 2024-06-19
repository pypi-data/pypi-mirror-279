import requests
class BKKClient:
    def __init__(self,key: str, version = 3, appVersion = "0.0.1"):
        self.key = key
        self.version = version
        self.appVersion = appVersion
        print(self.key)
    def get_bubi(self, includeReferences):
        self.includeReferences = includeReferences
        r = requests.get(f"https://futar.bkk.hu/api/query/v1/ws/otp/api/where/bicycle-rental.json?key={self.key}&version={self.version}&appVersion={self.appVersion}&includeReferences={self.includeReferences}")
        return r.json()["currentTime"], r.json()["data"]
import BKKCLient
asd = BKKCLient("280e57e9-2271-410b-8df0-3e73d597920f", version = 3, appVersion = "0.0.1")
asd.get_bubi("true")