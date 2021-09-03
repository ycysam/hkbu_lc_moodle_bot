import datetime
from activity import Activity
from file import File
from functions import get_element_by_xpath, html_quote_escape
from selenium.webdriver.common.action_chains import ActionChains

class Assignment(Activity):
    def __init__(self, assignment_name, assignment_instruction, start_date, end_date, max_file_size, file_type):
        super().__init__()
        self.assignment_name = assignment_name
        self.assignment_instruction = assignment_instruction
        if isinstance(start_date, datetime.datetime):
            self.assignment_submission_start_date = start_date
        if isinstance(end_date, datetime.datetime):
            self.assignment_submission_end_date = end_date
        self.max_file_size = max_file_size
        self.file_type = file_type
        self.assignment_files = [] #list of file object
        self.add_activity("//label[@for='item_assign']")
    
    def add_assignment(self):
        get_element_by_xpath(self.driver, 2, "//*[@id='id_name']").send_keys(self.assignment_name) # Set the assignment name
        summary_box = get_element_by_xpath(self.driver, 2, "//div[@id='id_introeditoreditable']")
        ActionChains(self.driver).move_to_element(summary_box).click().pause(1).perform()
        self.driver.execute_script("arguments[0].innerHTML=\"{}\"".format(html_quote_escape(self.assignment_instruction)), summary_box) # Add assignment instructions
        # Add files
        for fo in self.assignment_files:
            fo.file_picker()
        start_date = self.assignment_submission_start_date
        end_date = self.assignment_submission_end_date
        #setup start submission date
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowsubmissionsfromdate_day']/option[text()='{ int(start_date.strftime('%d')) }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowsubmissionsfromdate_month']/option[text()='{ start_date.strftime('%B') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowsubmissionsfromdate_year']/option[text()='{ start_date.strftime('%Y') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowsubmissionsfromdate_hour']/option[text()='{ start_date.strftime('%H') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowsubmissionsfromdate_minute']/option[text()='{ start_date.strftime('%M') }']").click()
        #setup due submission date
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_duedate_day']/option[text()='{ int(end_date.strftime('%d')) }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_duedate_month']/option[text()='{ end_date.strftime('%B') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_duedate_year']/option[text()='{ end_date.strftime('%Y') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_duedate_hour']/option[text()='{ end_date.strftime('%H') }']").click()
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_duedate_minute']/option[text()='{ end_date.strftime('%M') }']").click()
        # Uncheck "Remind me to grade by"
        get_element_by_xpath(self.driver, 1, f"//*[@id='id_gradingduedate_enabled']").click()
        # Set max file size
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_assignsubmission_file_maxsizebytes']/option[text()='{ self.max_file_size }']").click()
        # Set file type
        get_element_by_xpath(self.driver, 1, f"//*[@id='id_assignsubmission_file_filetypes']").send_keys(self.file_type)
        # Set restrict access
        self.add_restricted_date(self.activity_ava_start_date, 'from')
        self.add_restricted_date(self.activity_ava_end_date, 'until')
        get_element_by_xpath(self.driver, 1, f"//*[@id='id_submitbutton2']").click() # Save the assignment


    def add_assignment_file(self, file_actual_name):
        self.assignment_files.append(File("untitled", file_actual_name, False))
    
        