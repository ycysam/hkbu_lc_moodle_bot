import time
from moodle import Moodle
from functions import get_element_by_xpath

class Role:

    def __init__(self, ssoids):
        self.driver = Moodle.driver
        self.ssoid = ssoids 
        self.existing_participants = []
        self.__enroll()
    
    
    def __enroll(self):
        course_id = self.driver.current_url.split('?')[1]
        self.driver.get(f"https://buelearning.hkbu.edu.hk/user/index.php?{ course_id }")
        self.__get_existing_participants()
        self.driver.execute_script("window.scrollTo(0, 0)")
        get_element_by_xpath(self.driver, 2, "//input[@value='Enrol users']").click() # Click on Enrol users
        search_box = get_element_by_xpath(self.driver, 1, "//div[@id='fitem_id_userlist']//input[@placeholder='Search']")
        found_at_least_1_user = False
        for user in self.ssoid:
            email = user + '@' + self.email_domain
            if email in self.existing_participants:
                print(f"<{ email } is already enrolled>")
            else:
                search_box.send_keys(email)
                get_element_by_xpath(self.driver, 1, f"//select[@id='id_roletoassign']/option[text()='{ self.role }']").click() # Select Role
                time.sleep(2)
                get_element_by_xpath(self.driver, 2, f"//small[text()='{ email }']/ancestor::li").click() # Select the user in the result
                time.sleep(2)
                search_box.clear()
                found_at_least_1_user = True
        if found_at_least_1_user:
            get_element_by_xpath(self.driver, 1, "//button[contains(text(), 'Enrol users')]").click()
        for user in self.ssoid:
            if self.__user_is_enrolled(user):
                print(f"<{user}@{self.email_domain} is enrolled>")
            else:
                print(f"<{user}@{self.email_domain} is not being enrolled, please try again>")


    def __user_is_enrolled(self, user):
        total_participant = int(get_element_by_xpath(self.driver, 2, "//p[@data-region='participant-count']").text.split()[0])
        total_display_participant = int(len(self.driver.find_elements_by_xpath("//tr[starts-with(@id, 'user-index-participants-')]")))
        if total_display_participant < total_participant:
            show_all_elem = get_element_by_xpath(self.driver, 1, "//div[@id='showall']/a")
            show_all_elem.click() 
        user_found = get_element_by_xpath(self.driver, 5, f"//td[text() = '{ user }@{ self.email_domain }']")
        if user_found:
            return True
        else:
            return False


    def __get_existing_participants(self):
        total_participant = int(get_element_by_xpath(self.driver, 2, "//p[@data-region='participant-count']").text.split()[0])
        total_display_participant = int(len(self.driver.find_elements_by_xpath("//tr[starts-with(@id, 'user-index-participants-')]")))
        if total_display_participant < total_participant:
            show_all_elem = get_element_by_xpath(self.driver, 1, "//div[@id='showall']/a")
            show_all_elem.click()
            time.sleep(3)
        email_elem = self.driver.find_elements_by_xpath("//tr[starts-with(@id, 'user-index-participants-')][not(@class ='emptyrow')]/td[2]")
        for e in email_elem:
            self.existing_participants.append(e.text)
        

class TeachingAssistant(Role):
    def __init__(self, ssoid):
        self.role = "Teaching Assistant"
        self.email_domain = "hkbu.edu.hk"
        super().__init__(ssoid)


class Student(Role):
    def __init__(self, ssoid):
        self.role = "Student"
        self.email_domain = "life.hkbu.edu.hk"
        super().__init__(ssoid)