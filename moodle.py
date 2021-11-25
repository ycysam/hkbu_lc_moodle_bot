from functions import get_element_by_xpath
from sections import Sections
from selenium import webdriver
from dotenv import dotenv_values


class Moodle:
    driver = webdriver.Chrome()

    def __init__(self, course_code, year, semester, filter_combine_section=True):
        self.procedures = None
        self.url = "https://buelearning.hkbu.edu.hk/login/"
        #Getting credential
        config = dotenv_values(".env")
        self.ssoid = config['SSOID']
        self.ssopw = config['SSOPW']
        self.login()
        self.sections = Sections(Moodle.driver, course_code, year, semester, filter_combine_section)
    
    def login(self):
        Moodle.driver.get(self.url)
        is_logout = not bool(Moodle.driver.find_elements_by_xpath("//button[text()='Log out']"))
        if is_logout:
            get_element_by_xpath(Moodle.driver, 2, "//*[@id='ssoidLogin']").click() # orange button (login from staff)
            require_sso_login = bool(Moodle.driver.find_elements_by_id("ssoid"))
            if require_sso_login:
                get_element_by_xpath(Moodle.driver, 2, "//*[@id='ssoid']").send_keys(self.ssoid) # enter SSOID
                get_element_by_xpath(Moodle.driver, 2, "//*[@id='btn_next']").click() # click next
                get_element_by_xpath(Moodle.driver, 2, "//*[@id='pwd']").send_keys(self.ssopw) # enter SSOID PWD
                get_element_by_xpath(Moodle.driver, 2, "//*[@id='btn_sign_in']").click() # click sign in
        else:
            get_element_by_xpath(Moodle.driver, 1, "//button[text()='Cancel']").click()
    
    def start_iteration(self, procedures):
        self.procedures = procedures
        self.sections.iterate_sections(self.procedures)
    
    def resume_from_section(self, section):
        self.sections.resume_section(section)

    def include_single_section(self, section):
        self.sections.include_only_section(section)
    
    def exclude_section(self, section):
        self.sections.exclude_section(section)
