import requests, pdb
from time import sleep
from classes.Config import Config


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}


class Requests:

    def __init__(self):
        
        config = Config()

        self.proxies = None
        if config.proxy:
            self.proxies = {
                "http": f"{config.proxy}"
            }


    def get(self, page_url):

        response = self.req(page_url)

        # try with back off
        if response.status_code  != 200:
            print("Request failed {response.status_code}. Trying 10 sets of 10 second backoff.")
            for i in range(10):
                print(i)
                sleep(10)
                response = self.req(page_url)
                if response.status_code  == 200:
                    break

        # if STILL can't get a 200 blow up
        if response.status_code != 200:
            print("Requests Still Failed")
            pdb.set_trace()
            raise Exception("Can' get a successful request")
        
        return response
    
    def req(self, page_url):
        if self.proxies:
            return requests.get(page_url, headers=headers, proxies=self.proxies)
        else:
            return equests.get(page_url, headers=headers)

        