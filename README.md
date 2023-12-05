### LinkedIn Easy Apply Bot

* Still in super Alpha phase.
* This is a bot to assist with LinkedIn's application process
* Will update with more info and vid's soon.

# To Use
1. Put your info in the config.json file
2. Run gather_job_ids.py to scrape app listings and gather jobs pertaining to the search terms you put into config.json
3. Run job_apply_loop.py to start applying to the jobs you collected from the previous steps.


# Notes
* You can view all applied jobs by entering a python terminal and using the AppliedIds class total method.
* You can view all the collected unapplied jobs by doing the same thign but with JobIds class total method.
