from activity import Activity
from functions import get_element_by_xpath, html_quote_escape

class CourseImport(Activity):
    def __init__(self, clone_from_course, import_everything=False):
        super().__init__()
        self.clone_from_course = clone_from_course
        self.import_everything = import_everything
        self.activities = []
    
    def import_course(self):
        self.driver.execute_script("window.scrollTo(0, 0)")
        get_element_by_xpath(self.driver, 5, "//div[@class='context-header-settings-menu']//div[@class='dropdown']").click() #click on the setting wheel
        get_element_by_xpath(self.driver, 1, "//div[@class='context-header-settings-menu']//following::a[contains(text(), 'Import')]").click() # Click on Import
        get_element_by_xpath(self.driver, 1, "//input[@name='search']").send_keys(self.clone_from_course) # Type the corse to import from
        get_element_by_xpath(self.driver, 1, "//input[@value='Search']").click() # Perform search
        get_element_by_xpath(self.driver, 5, "//div[@class='import-course-search']/div[text()='Total courses: 1']") # Ensure only one result
        get_element_by_xpath(self.driver, 1, "//input[@name='importid']").click() # Select the only course
        get_element_by_xpath(self.driver, 1, "//input[@value='Continue']").click() # Click on continue
        if self.import_everything:
            get_element_by_xpath(self.driver, 1, "//input[@value='Jump to final step']").click() # Click on jump to final step
        else:
            get_element_by_xpath(self.driver, 1, "//input[@value='Next']").click() # Click on Next
            get_element_by_xpath(self.driver, 1, "//*[@id='backup-none-included']").click() # Uncheck all activity
            # Test topic name
            topic_elems = self.driver.find_elements_by_xpath("//div[@class='form-check']//input[@type='checkbox'][starts-with(@id, 'id_setting_section_section')]/parent::label[text()][not(parent::input)]")
            activity_elems = self.driver.find_elements_by_xpath("//div[@class='form-check']//input[@type='checkbox'][starts-with(@id, 'id_setting_activity')]/parent::label[text()][not(parent::input)]")
            all_checkbox_elems = self.driver.find_elements_by_xpath("//div[@class='form-check']//input[@type='checkbox']/parent::label[text()][not(parent::input)]")
            # Construct dictionary topic_name:[act1, act2, act3...]
            d = {}
            current_topic = None
            for cb in all_checkbox_elems:
                if cb not in d and cb in topic_elems:
                    current_topic = cb
                    d[cb] = []
                elif cb in activity_elems:
                    d[current_topic].append(cb)

            # Select activity and the topic to import
            for k, v in d.items():
                topic_clicked = False
                for e in v:
                    if e.text in self.activities:
                        topic_name = k.text
                        if not topic_clicked:
                            k.click()
                            topic_clicked = True
                        e.click()
            #Click on Next
            get_element_by_xpath(self.driver, 1, "//input[@value='Next']").click()
            get_element_by_xpath(self.driver, 1, "//input[@value='Perform import']").click()
            get_element_by_xpath(self.driver, 120, "//div[@class='alert alert-success alert-block fade in ']") # Wait until success box show
            get_element_by_xpath(self.driver, 1, "//button[text()='Continue']").click() # Return to Course
            Activity.topic_id = self.find_topic_id_by_topic_name(topic_name)
            if Activity.topic_id == None:
                raise Exception("Existed topic may overwited the imported one, make sure the topic(location) of the course to be imported do not overlap with the distination.")
            print("<item(s) imported>")

    
    def add_activity_to_import(self, activity_name):
        self.activities.append(activity_name)
