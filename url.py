from activity import Activity
from functions import get_element_by_xpath

class Url(Activity):
    def __init__(self, url_name, url):
        super().__init__()
        self.url_name = url_name
        self.url = url
        self.add_activity("URL")
    
    def add_url(self):
        get_element_by_xpath(self.driver, 1, "//*[@id='id_name']").send_keys(self.url_name) # Set URL name
        get_element_by_xpath(self.driver, 1, "//*[@id='id_externalurl']").send_keys(self.url) # Set the URL
        self.add_restricted_date(self.activity_ava_start_date, 'from')
        self.add_restricted_date(self.activity_ava_end_date, 'until')
        get_element_by_xpath(self.driver, 1, "//*[@id='id_submitbutton2']").click() # Save the URL and return to course page
        print("<url added>")
