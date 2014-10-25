import requests

ACCESS_TOKEN = "9471cd3235687f1f20263f064997376cb7ec16493eb46a580293da5d0825fd30"
API_ROOT = "https://api.producthunt.com/v1/"

class ProductHunt:
    @staticmethod
    def getToday():
        headers = {
            'Content-Type': 'application/json',
            'Accept'      : 'application/json',
            'Authorization':'Bearer '+ACCESS_TOKEN
        }
        r = requests.get(API_ROOT + "posts", headers=headers)
        return r.json()['posts']