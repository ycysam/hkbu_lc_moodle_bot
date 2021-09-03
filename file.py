import time
import datetime
from activity import Activity
from functions import get_element_by_xpath
from selenium.webdriver.common.action_chains import ActionChains

class File(Activity):
    def __init__(self, file_display_name, file_real_name, on_create_activity = True):
        super().__init__()
        self.file_display_name = file_display_name
        self.file_real_name = file_real_name
        if on_create_activity:
            self.add_activity("File")

    def add_file(self):
        get_element_by_xpath(self.driver, 1, "//*[@id='id_name']").send_keys(self.file_display_name) # Enter file display name
        self.file_picker()
        self.add_restricted_date(self.activity_ava_start_date, 'from')
        self.add_restricted_date(self.activity_ava_end_date, 'until')
        get_element_by_xpath(self.driver, 1, "//*[@id='id_submitbutton2']").click() # Save and return to course
        print("<file added>")
    
    def file_picker(self):
        get_element_by_xpath(self.driver, 2, "//a[@title='Add...']").click() # Click on the upload button
        time.sleep(1)
        get_element_by_xpath(self.driver, 2, "//a/span[text()='Private files']").click() # Click on Private file tab
        time.sleep(2)
        get_element_by_xpath(self.driver, 2, f"//p[contains(@class, 'fp-filename')][text()='{ self.file_real_name }']/ancestor::a").click() # click on the actual file
        author_box = get_element_by_xpath(self.driver, 1, "//label[text()='Author']/following-sibling::input")
        author_box.clear()
        author_box.send_keys("HKBU Language Centre") # Give new owner
        get_element_by_xpath(self.driver, 1, "//button[text()='Select this file']").click() # Select the file

    def file_replace(self, new_file):
        if isinstance(new_file, File):
            file_edit_elem = get_element_by_xpath(self.driver, 1, f"//span[normalize-space(text())=\"{ self.file_display_name }\"]/following::a[contains(text(), 'Edit')][1]")
            edit_setting_elem = get_element_by_xpath(self.driver, 1, f"//span[normalize-space(text())=\"{ self.file_display_name }\"]/following::a[contains(text(), 'Edit')][1]/following::span[contains(text(), 'Edit settings')][1]")
            ActionChains(self.driver).pause(1).move_to_element(file_edit_elem).click().pause(1).move_to_element(edit_setting_elem).click().perform()
            # Set new file name
            file_name = get_element_by_xpath(self.driver, 2, f"//*[@id='id_name']")
            file_name.clear()
            file_name.send_keys(new_file.file_display_name)
            # Delete old file
            get_element_by_xpath(self.driver, 1, "//a[text()='Files']").click() # Click on the file box
            get_element_by_xpath(self.driver, 1, f"//div[text()='{ self.file_real_name }']/parent::div/parent::a/parent::div//div[@class='fp-reficons2']").click() # Click on the file to be delete
            get_element_by_xpath(self.driver, 1, "//button[text()='Delete']").click() # Delete
            get_element_by_xpath(self.driver, 1, "//button[text()='OK']").click() # Confirm
            # Add new file
            new_file.file_picker()
            get_element_by_xpath(self.driver, 1, "//*[@id='id_submitbutton2']").click() # Save and return to course
            print("<file replaced: ", self.file_real_name, "-->", new_file.file_real_name, ">")
