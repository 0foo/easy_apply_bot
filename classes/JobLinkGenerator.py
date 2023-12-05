from urllib.parse import quote
from Config import Config

class JobLinkGenerator:
 
    def __init__(self, config={}):
        self.config = Config()
        self.page_number=1
        

    def get_link(self):
        base = "https://www.linkedin.com/jobs/search/"
        easy_apply=f"f_AL={quote(self.config.easy_apply_bool)}"
        time_frame_seconds=f"f_TPR={self.config.time_frame_seconds}"
        page_number=f"start={self.page_number}"
        keywords=f"keywords={quote(self.config.keywords)}"
        location=f"location={quote(self.config.location)}"

        return f"{base}?{easy_apply}&{time_frame_seconds}&{keywords}&{location}&{page_number}"