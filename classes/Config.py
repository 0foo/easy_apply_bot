import json


class Config:
    config_file="config.json"

    def __init__(self):
        # declare instance vars plus defaults
        self.required: list[str]  = []
        self.ignored: list[str] = []
        self.username: str = ""
        self.password: str = ""
        self.keywords: str = ""
        self.location: str = "United%20States"
        self.time_frame_seconds: str = "60480"
        self.proxy: str = ""
        self.easy_apply_bool: str = "true"

        config_file: str = "./config.json"
        config: str = self.get_config(self, config_file)
        
        if "required" in config:
            self.required =  config["required"].split(",")
        if "ignored" in config:
            self.ignored: list[str] =config["ignored"].split(",")
        if "username" in config:
            self.username: str = config["username"]
        if "password" in config:
            self.password: str = config["password"]
        if "keywords" in config:
            self.keywords: str = config["keywords"]
        if "location" in config:
            self.location: str = config["location"]
        if "time_frame_seconds" in config:
            self.time_frame_seconds: str = config["time_frame_seconds"]
        if "proxy" in config:
            self.proxy: str = config["proxy"]


    def get_config(self, config_file):
        data={}
        with open(config_file) as f:
            data = json.loads(f.read())
        return data
    



