import requests, pdb
from time import sleep
from classes.Config import Config


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}



class Requests:

    def __init__(self):
        
        config = Config()

        self.proxies = {
            "http": f"{config.proxy}"
        }


    def get(self, page_url):

        # try normally
        # response = requests.get(page_url, headers=headers)

        # try with proxy
        # if response.status_code  != 200:
        response = requests.get(page_url, headers=headers, proxies=proxies)
        
        # try with proxy and back off
        if response.status_code  != 200:
            print("Request failed {response.status_code}. Trying 10 sets of 10 second backoff.")
            for i in range(10):
                print(i)
                sleep(10)
                response = requests.get(page_url, headers=headers, proxies=self.proxies)
                if response.status_code  == 200:
                    break

        # if STILL can't get a 200 blow up
        if response.status_code != 200:
            print("Requests Still Failed")
            pdb.set_trace()
            raise Exception("Can' get a successful request")
        
        return response