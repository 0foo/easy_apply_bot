from urllib.parse import quote

class JobLinkGenerator:
    location="United%20States"
    keywords="system administrator"
    easy_apply_bool="true"
    time_frame_seconds=604800 # one week
    page_number=1

    def get_link(self):
        base = "https://www.linkedin.com/jobs/search/"
        easy_apply=f"f_AL={quote(self.easy_apply_bool)}"
        time_frame_seconds=f"f_TPR={self.time_frame_seconds}"
        page_number=f"start={self.page_number}"
        keywords=f"keywords={quote(self.keywords)}"
        location=f"location={quote(self.location)}"

        return f"{base}?{easy_apply}&{time_frame_seconds}&{keywords}&{location}&{page_number}"