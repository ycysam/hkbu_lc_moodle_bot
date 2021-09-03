from activity import Activity
from functions import get_element_by_xpath, html_quote_escape
from selenium.webdriver.common.action_chains import ActionChains

class Turnitin(Activity):
    def __init__(self, assignment_name, summary, submission_type, max_file_size, display_originality, part_name, start_date, due_date, post_date, max_marks, allow_due, gen_speed, store_student_papers, check_stored_paper, check_internet, check_journals, exclude_bibliography, exclude_quoted, rubric):
        super().__init__()
        self.assignment_name = assignment_name
        self.summary = summary
        self.submission_type = submission_type
        self.max_file_size = max_file_size
        self.display_originality = display_originality
        self.part_name = part_name
        self.start_date = start_date
        self.due_date = due_date
        self.post_date = post_date
        self.max_marks = max_marks
        self.allow_due = allow_due
        self.gen_speed = gen_speed
        self.store_student_paper = store_student_papers
        self.check_stored_paper = check_stored_paper
        self.check_internet = check_internet
        self.check_journals = check_journals
        self.exclude_bibliography = exclude_bibliography
        self.exclude_quoted = exclude_quoted
        self.rubric =rubric
        self.add_activity("Turnitin Assignment 2")
    
    def add_turnitin(self):
        get_element_by_xpath(self.driver, 2, "//*[@id='id_name']").send_keys(self.assignment_name) # Set the turnitin assignment name
        summary_box = get_element_by_xpath(self.driver, 2, "//div[@id='id_introeditoreditable']")
        ActionChains(self.driver).move_to_element(summary_box).click().pause(1).perform()
        self.driver.execute_script("arguments[0].innerHTML=\"{}\"".format(html_quote_escape(self.summary)), summary_box) # Add turnitin assignment instructions
        get_element_by_xpath(self.driver, 1, "//*[@id='id_showdescription']").click() # Tick 'Display description on course page'
        get_element_by_xpath(self.driver, 1, f"//div[@id='fitem_id_type']//select[@id='id_type']/option[text()='{ self.submission_type }']").click() # Select submission type
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_maxfilesize']/option[text()='{ self.max_file_size }']").click() # Select max file upload size
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_studentreports']/option[text()='{ self.display_originality }']").click() # Select display originality to student
        part_name = get_element_by_xpath(self.driver, 1, "//*[@id='id_partname1']")
        part_name.clear()
        part_name.send_keys(self.part_name) # Set assignment part name
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtstart1_day']/option[text()='{ int(self.start_date.strftime('%d')) }']").click() # Set start date (day)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtstart1_month']/option[text()='{ self.start_date.strftime('%B') }']").click() # Set start date (month)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtstart1_year']/option[text()='{ self.start_date.strftime('%Y') }']").click() # Set start date (year)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtstart1_hour']/option[text()='{ self.start_date.strftime('%H') }']").click() # Set start date (hour)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtstart1_minute']/option[text()='{ self.start_date.strftime('%M') }']").click() # Set start date (minute)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtdue1_day']/option[text()='{ int(self.due_date.strftime('%d')) }']").click() # Set due date (day)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtdue1_month']/option[text()='{ self.due_date.strftime('%B') }']").click() # Set due date (month)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtdue1_year']/option[text()='{ self.due_date.strftime('%Y') }']").click() # Set due date (year)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtdue1_hour']/option[text()='{ self.due_date.strftime('%H') }']").click() # Set due date (hour)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtdue1_minute']/option[text()='{ self.due_date.strftime('%M') }']").click() # Set due date (minute)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtpost1_day']/option[text()='{ int(self.post_date.strftime('%d')) }']").click() # Set post date (day)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtpost1_month']/option[text()='{ self.post_date.strftime('%B') }']").click() # Set post date (month)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtpost1_year']/option[text()='{ self.post_date.strftime('%Y') }']").click() # Set post date (year)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtpost1_hour']/option[text()='{ self.post_date.strftime('%H') }']").click() # Set post date (hour)
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_dtpost1_minute']/option[text()='{ self.post_date.strftime('%M') }']").click() # Set post date (minute)
        max_marks = get_element_by_xpath(self.driver, 1, "//*[@id='id_maxmarks1']")
        max_marks.clear()
        max_marks.send_keys(self.max_marks) # Set a new max mark
        get_element_by_xpath(self.driver, 1, "//a[text()='Similarity Report Options']").click() # Open up the originality tab
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_allowlate']/option[text()='{ self.allow_due }']").click() # Set allow due
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_reportgenspeed']/option[text()='{ self.gen_speed }']").click() # Set report generate speed
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_submitpapersto']/option[text()='{ self.store_student_paper }']").click() # Set store students paper or not
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_spapercheck']/option[text()='{ self.check_stored_paper }']").click() # Set check against stored students paper or not
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_internetcheck']/option[text()='{ self.check_internet }']").click() # Set check against internet or not
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_journalcheck']/option[text()='{ self.check_journals }']").click() # Set check against journals or not
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_excludebiblio']/option[text()='{ self.exclude_bibliography }']").click() # Set to exclude bibliography or not
        get_element_by_xpath(self.driver, 1, f"//select[@id='id_excludequoted']/option[text()='{ self.exclude_quoted }']").click() # Set to exclue quoted materials or not
        if self.rubric:
            get_element_by_xpath(self.driver, 1, "//a[text()='GradeMark Options']").click() # Open up GradeMark Options tag
            get_element_by_xpath(self.driver, 1, f"//select[@id='id_rubric']/option[text()='{ self.rubric }']").click() # Set the rubric
        self.add_restricted_date(self.activity_ava_start_date, 'from')
        self.add_restricted_date(self.activity_ava_end_date, 'until')
        get_element_by_xpath(self.driver, 1, "//*[@id='id_submitbutton2']").click() # Save the turnitin assignment
        print("<turnitin assignment added>")
