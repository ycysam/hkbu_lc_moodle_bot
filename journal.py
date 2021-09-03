import datetime
from moodle import Moodle
from activity import Activity
from functions import get_element_by_xpath, html_quote_escape
from selenium.webdriver.common.action_chains import ActionChains

class Journal(Activity):
    def __init__(self, journal_name, journal_question):
        self.driver = Moodle.driver
        self.journal_name = journal_name
        self.journal_question = journal_question
        self.add_activity("Journal")
    
    def add_journal(self):
        get_element_by_xpath(self.driver, 2, "//*[@id='id_name']").send_keys(self.journal_name) # Set the journal name
        summary_box = get_element_by_xpath(self.driver, 2, "//div[@id='id_introeditoreditable']/p")
        ActionChains(self.driver).move_to_element(summary_box).click().pause(1).perform()
        self.driver.execute_script("arguments[0].innerHTML=\"{}\"".format(html_quote_escape(self.journal_question)), summary_box)
        self.add_restricted_date(self.activity_ava_start_date, 'from')
        self.add_restricted_date(self.activity_ava_end_date, 'until')
        get_element_by_xpath(self.driver, 1, "//*[@id='id_submitbutton2']").click() # Save and return to course
        print("<journal added>")