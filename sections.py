import re
from functions import get_element_by_xpath

class Sections:
    def __init__(self, driver, course_code, year, semester, filter_combine_section = True):
        self.driver = driver
        self.course_code = course_code
        self.year = year
        self.semester = semester
        self.filter_combine_section = filter_combine_section
        self.search_url = self.get_search_url()
        self.sections = [] #store object of section
        self.__init_sections()

    def iterate_sections(self, procedures):
        sections_count = len(self.sections)
        for num, section in enumerate(self.sections, start=1):
            print(f"processing { num } of { sections_count } - { section.section_name }: ")
            self.driver.get(section.section_url)
            permission_not_granted = bool(self.driver.find_elements_by_xpath("//div[@id='notice'][text()='You cannot enrol yourself in this course.']"))
            if not permission_not_granted:
                procedures(section)
            else:
                print("!!!You are not enrol into this section!!!")
        print("finished.")
    
    def get_search_url(self):
        return f"https://buelearning.hkbu.edu.hk/course/search.php?search={ self.course_code }%20{ self.year }%20{ self.semester }&perpage=all"

    def resume_section(self, from_section_number):
        from_section_url = self.__get_section_url_by_section_number(from_section_number)
        #define filter
        def filter_section(section):
            if section.section_url >= from_section_url:
                return True
            else:
                return False
        new_list = list(filter(filter_section, self.sections))
        self.sections = sorted(new_list, key=lambda obj: obj.section_url)
    
    def exclude_section(self, exc_section):
        #define filter
        def filter_section(section):
            if section.section_number == exc_section:
                return False
            else:
                return True
        new_list = list(filter(filter_section, self.sections))
        self.sections = sorted(new_list, key=lambda obj: obj.section_url)

    def include_only_section(self, inc_section):
        #define filter
        def filter_section(section):
            if section.section_number == inc_section:
                return True
            else:
                return False
        new_list = list(filter(filter_section, self.sections))
        self.sections = sorted(new_list, key=lambda obj: obj.section_url)

    def __init_sections(self):
        is_login = get_element_by_xpath(self.driver, 30, "//*[@id='page-site-index']") #set to 30 second because wait for 2FA
        if is_login:
            self.driver.get(self.search_url)
            xpath_inc_combined = "//a[text()!='Meta Course']//parent::div[@class='coursecat']//parent::div[@class='content']//preceding-sibling::div[@class='info']/h3/a"
            xpath_exc_combined = xpath_inc_combined + "[not(contains(text(), '/'))]"
            section_elems = self.driver.find_elements_by_xpath(xpath = xpath_exc_combined if self.filter_combine_section else xpath_inc_combined) #exclude meta course
            for section in section_elems:
                section_name = section.text
                section_number = self.__get_section_number(section_name)
                section_url = section.get_attribute("href")
                teacher_elem = self.driver.find_elements_by_xpath(f"//a[@href='{ section_url }']//ancestor::div[@class='info']//following-sibling::div[@class='content']/ul[@class='teachers']/li/a")
                teacher_name = teacher_elem[0].text if teacher_elem else ""
                self.sections.append(Section(section_name, section_number, section_url, teacher_name))
            sections = sorted(self.sections, key=lambda obj: obj.section_url)
            return sections

    def __get_section_number(self, section_name):
        pattern = '[(]Section (.+)[)]'
        match = re.search(pattern, section_name)
        if match:
            return match.group(1)
    
    def __get_section_url_by_section_number(self, section_number):
        for section in self.sections:
            if section.section_number == section_number:
                return section.section_url

class Section:
    def __init__(self, section_name, section_number, section_url, teacher_name):
        self.section_name = section_name
        self.section_number = section_number
        self.section_url = section_url
        self.teacher_name = teacher_name
