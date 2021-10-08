import re, time, csv, os
from moodle import Moodle
from datetime import datetime
from functions import get_element_by_xpath
from pprint import pprint

class Report:
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    def __init__(self, section, assignment_name, similarity_threshold):
        self.section = section # The section Object
        self.driver = Moodle.driver
        self.assignment_name = assignment_name
        self.similarity_threshold = similarity_threshold
        self.submission_report_name = f"./exported/nil_late_submission_{ Report.timestamp }.csv"
        self.similarity_report_name = f"./exported/similarity_over_{ Report.timestamp }.csv"
        self.records = [] # List of Record(s)
        self.__construct_records()
        self.__update_submission_record()
        self.__output_submission_report()
        self.__output_similarity_report()
    
    def __construct_records(self):
        course_id = self.driver.current_url.split('?')[1]
        self.driver.get(f"https://buelearning.hkbu.edu.hk/user/index.php?{ course_id }")
        participant_count = int(get_element_by_xpath(self.driver, 2, "//p[@data-region]").text.split()[0])
        if participant_count > 20:
            show_all_elem = get_element_by_xpath(self.driver, 1, "//div[@id='showall']/a")
            show_all_elem.click() 
        #Getting user information
        time.sleep(3)
        teacher_name = self.section.teacher_name
        section_number = self.section.section_number
        std_name_elems = self.driver.find_elements_by_xpath("//a[contains(text(), 'Student')]/parent::*/parent::*/parent::*//th/a[starts-with(@href, 'https://buelearning.hkbu.edu.hk/user/view.php?id=')]")
        for n in std_name_elems:
            std_name = n.text # Get student name
            uid_url = n.get_attribute("href") 
            uid = self.__get_uid_by_url(uid_url)
            #Get email of student
            std_email = get_element_by_xpath(self.driver, 1, f"//th/a[contains(@href, '{ uid }')]/parent::*/parent::*/td[2]").text
            #Create Record
            self.records.append(Record(section_number, teacher_name, uid, std_name, std_email))
    

    def __update_submission_record(self):
        self.driver.get(self.section.section_url) # Back to main page
        get_element_by_xpath(self.driver, 2, f"//span[contains(normalize-space(),'{ self.assignment_name }')]").click() # Click on the assignment
        get_element_by_xpath(self.driver, 1, "//label/select/option[text()='All']").click() # Select display All records
        while True:
            total_submission_count = get_element_by_xpath(self.driver, 1, "//div[@class='dataTables_info'][@role='status']").text.split()[-2]
            total_shown_count = get_element_by_xpath(self.driver, 1, "//div[@class='dataTables_info'][@role='status']").text.split()[3]
            if int(total_shown_count) > 0:
                if total_submission_count == total_shown_count:
                    break  
        #Get similarity data
        similarity_over_name_elems = self.driver.find_elements_by_xpath(f"//tr[(@role='row') and not(@class='header')]/td[6]/div/div[@class='origreport_score'][number(substring-before(text(), '%')) > { self.similarity_threshold }]/parent::*/parent::*/parent::*/td[2]/a")
        for name in similarity_over_name_elems:
            uid = self.__get_uid_by_url(name.get_attribute("href"))
            for r in self.records:
                if r.uid == uid:
                    r.similarity = get_element_by_xpath(self.driver, 1, f"//tr/td[2]/a[contains(@href, '{ uid }')]/parent::*/parent::*/td[6]/div/div[2]").text
                    r.report_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        #Get nil/late data
        nil_late_name_elems = self.driver.find_elements_by_xpath("//tr/td[5]/span[@class='late_submission']/parent::*/parent::*/td[2]/a | //tr/td[5][text()='--']/parent::*/td[2]/a")
        for name in nil_late_name_elems:
            uid = self.__get_uid_by_url(name.get_attribute("href"))
            for r in self.records:
                if r.uid == uid:
                    r.submission_time = get_element_by_xpath(self.driver, 1, f"//tr/td[2]/a[contains(@href, '{ uid }')]/parent::*/parent::*/td[5]").text
                    r.report_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


    def __output_submission_report(self):
        self.__create_output_folder('.\exported')
        with open(self.submission_report_name, newline='' ,mode='a+') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if os.stat(self.submission_report_name).st_size == 0:
                writer.writerow(["Section", "Name", "Email", "Date", "Status", "Teacher", "Report time","Remarks"])
            for r in self.records:
                if r.submission_time != None:
                    status = 'no submission' if r.submission_time == '--' else 'late submission'
                    writer.writerow([r.section_number, r.name, r.email, r.submission_time, status, r.teacher_name, r.report_time, ""])
        print("<submission report updated>")
    

    def __output_similarity_report(self):
        self.__create_output_folder('.\exported')
        with open(self.similarity_report_name, newline='' ,mode='a+') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if os.stat(self.similarity_report_name).st_size == 0:
                writer.writerow(["Section", "Name", "Email", "Percentage", "Teacher", "Report time","Remarks"])
            for r in self.records:
                if r.similarity != None:
                    writer.writerow([r.section_number, r.name, r.email, r.similarity, r.teacher_name, r.report_time, ""])
        print("<similarity report updated>")
    

    def __create_output_folder(self, folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
                

    def __get_uid_by_url(self, url):
        pattern = "id=(\d+)"
        match = re.search(pattern, url)
        if match:
            uid = match.group(1) # Get student uid in Moodle
            return uid
        return None


class Record:
    def __init__(self, section_number, teacher_name, uid, student_name, email, similarity=None, submission_time=None, report_time=None):
        self.section_number = section_number
        self.teacher_name = teacher_name
        self.uid = uid
        self.name = student_name
        self.email = email
        self.similarity = similarity
        self.submission_time = submission_time
        self.report_time = report_time
    