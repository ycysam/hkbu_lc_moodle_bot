import time
import datetime
from moodle import Moodle
from functions import get_element_by_xpath, html_quote_escape
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#pre-condition: in the section main-page
class Activity:
    topic_id = None

    def __init__(self):
        self.driver = Moodle.driver
        self.activity_ava_start_date = None
        self.activity_ava_end_date = None
    
    def turn_editing_on(self):
        turn_editing_on_elem = self.driver.find_elements_by_xpath("//button[text()='Turn editing on']")
        if turn_editing_on_elem:
            turn_editing_on_elem[0].click()
            print("<turn editing on>")
        else:
            return False
    
    def create_topic(self, topic_name, new=False):
        if not new:
            # Find the topic start with 'Topic ', and there are no activity under that topic
            topic_id = self.find_toppest_empty_topic_id()
            if topic_id:
                Activity.topic_id = topic_id
            else:
                new = True
        if new:
            get_element_by_xpath(self.driver, 2, "//a[@class='add-sections']").click() # Add topics
            get_element_by_xpath(self.driver, 1, "//button[.='Add topics']").click() # Click on the "Add topics" button
            topic_id = get_element_by_xpath(self.driver, 5, "//li[contains(@id, 'section-')][last()]").get_attribute("id")
            Activity.topic_id = topic_id.split('-')[1]
            print("<new topic created>")
        self.rename_topic(topic_name)
    
    def rename_topic(self, topic_name, old_topic=''):
        if old_topic:
            Activity.topic_id = self.find_topic_id_by_topic_name(old_topic)
        topic_name_elem = get_element_by_xpath(self.driver, 3, f"//li[@id='section-{ Activity.topic_id }']//span[@data-itemtype='sectionname']/a")
        ActionChains(self.driver).move_to_element(topic_name_elem).click().send_keys(Keys.BACKSPACE).pause(1).send_keys(topic_name).key_down(Keys.ENTER).perform()
        print("<topic renamed>")
    
    def hide_topic_from_student(self):
        edit_elem = get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//child::a[@aria-label='Edit']")
        hide_topic_elem = get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//child::a[@aria-label='Edit']/ancestor::li//a/span[contains(text(), 'Hide topic')]")
        if hide_topic_elem:
            ActionChains(self.driver).pause(1).move_to_element(edit_elem).click().pause(1).move_to_element(hide_topic_elem).click().perform()
            get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//span[text()='Hidden from students']") # Wait for 'hidden from students' tag to show
            print("<topic hidden>")
    
    def add_topic_summary(self, summary):
        summary = html_quote_escape(summary)
        edit_elem = get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//child::a[@aria-label='Edit']")
        edit_topic_elem = get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//child::a[@aria-label='Edit']/ancestor::li//a/span[contains(text(), 'Edit topic')]")
        ActionChains(self.driver).move_to_element(edit_elem).click().pause(1).move_to_element(edit_topic_elem).pause(1).click().perform()
        summary_box = get_element_by_xpath(self.driver, 3, "//*[@id='id_summary_editoreditable']")
        ActionChains(self.driver).move_to_element(summary_box).click().pause(1).perform()
        self.driver.execute_script(f"arguments[0].innerHTML=\"{ summary }\"", summary_box)
        get_element_by_xpath(self.driver, 1, "//input[@value= 'Save changes']").click() # Save changes
    
    def add_activity(self, activity_type):
        get_element_by_xpath(self.driver, 2, f"//li[@id='section-{ Activity.topic_id }']//child::span[@class='section-modchooser-text']").click() # Add activity
        get_element_by_xpath(self.driver, 3, f"(//div[@class='optionname clamp-2'][text()='{ activity_type }'])[1]").click() # Select 'File'
        print(f"<setting up {activity_type}>")

    def find_topic_id_by_topic_name(self, topic_name):
        self.turn_editing_on()
        get_element_by_xpath(self.driver, 120, "//li[@id='section-0']") # Wait until first topic show
        topics = self.driver.find_elements_by_xpath("//li[contains(@id, 'section-')]//span/a[@title='Edit topic name']")
        section_ids = self.driver.find_elements_by_xpath("//li[contains(@id, 'section-')]//span/a[@title='Edit topic name']/ancestor::li")
        for topic, section_id in zip(topics, section_ids):
            if topic.text == topic_name:
                return section_id.get_attribute('id').split('-')[1]

    def set_topic_id(self, topic_id):
        Activity.topic_id = topic_id
    
    def add_restricted_date(self, date, from_or_until):
        if isinstance(date, datetime.datetime):
            self.driver.execute_script("window.scrollTo(0, 0)")
            expand_all = self.driver.find_elements_by_xpath("//a[text()='Expand all']") #expand all link
            if expand_all:
                time.sleep(1)
                expand_all[0].click()
            restrictions = len(self.driver.find_elements_by_xpath("//h3[@class='accesshide']"))
            if restrictions > 1:
                print("<be careful, other restriction(s) already exist>")
            #Add date restriction
            get_element_by_xpath(self.driver, 1, "//button[contains(text(), 'Add restriction')]").click() # Add restriction
            get_element_by_xpath(self.driver, 1, "//button[text()='Date']").click() # Add Date restriction
            time.sleep(1)
            #Date setup
            get_element_by_xpath(self.driver, 1, f"(//select[@name='direction']/option[text()='{ from_or_until }'])[last()]").click()
            get_element_by_xpath(self.driver, 1, f"(//select[@name='x[day]']/option[text()='{ int(date.strftime('%d')) }'])[last()]").click()
            get_element_by_xpath(self.driver, 1, f"(//select[@name='x[month]']/option[text()='{ date.strftime('%B') }'])[last()]").click()
            get_element_by_xpath(self.driver, 1, f"(//select[@name='x[year]']/option[text()='{ date.strftime('%Y') }'])[last()]").click()
            get_element_by_xpath(self.driver, 1, f"(//select[@name='x[hour]']/option[text()='{ date.strftime('%H') }'])[last()]").click()
            get_element_by_xpath(self.driver, 1, f"(//select[@name='x[minute]']/option[text()='{ date.strftime('%M') }'])[last()]").click()
            print("<date restriction added>")
    
    def topic_reallocate(self, under_topic="", top_or_bottom="bottom"): # Toppic will move to the top by default
        self.turn_editing_on()
        self.driver.execute_script("window.scrollTo(0, 0)")
        get_element_by_xpath(self.driver, 3, f"(//li[@id='section-{ Activity.topic_id }']//i)[1]").click() #Click on the anchor to be reallocate
        sid = self.find_toppest_empty_topic_id()
        if under_topic == "":
            if top_or_bottom == 'top':
                get_element_by_xpath(self.driver, 2, "//a[@data-drop-target='section-1']").click()
            else:
                if sid:
                    get_element_by_xpath(self.driver, 2, f"//a[starts-with(@data-drop-target, 'section-{ sid }')]").click()
        else:
            if sid:
                get_element_by_xpath(self.driver, 2, f"//li/a[contains(text(), '{under_topic}')]/following::li[1]/a").click()
        time.sleep(2)
        print("<topic reallocated>")
    
    def find_toppest_empty_topic_id(self):
        self.turn_editing_on()
        self.driver.implicitly_wait(3)
        xpath = "(//a[starts-with(normalize-space(text()), 'Topic ')]//ancestor::h3//parent::div[@class='content']//ul[@data-draggroups='resource' and count(li) = 1])[1]//ancestor::li[contains(@id, 'section-')]"
        empty_topic = self.driver.find_elements_by_xpath(xpath)
        self.driver.implicitly_wait(0)
        if empty_topic:
            topic_id = empty_topic[0].get_attribute('id').split('-')[1]
            return topic_id
        else:
            return None
    
    def find_all_empty_topic_ids(self):
        self.turn_editing_on()
        self.driver.implicitly_wait(3)
        xpath = "//a[starts-with(normalize-space(text()), 'Topic ')]//ancestor::h3//parent::div[@class='content']//ul[@data-draggroups='resource' and count(li) = 1]//ancestor::li[contains(@id, 'section-')]"
        empty_topics = self.driver.find_elements_by_xpath(xpath)
        self.driver.implicitly_wait(0)
        empty_topics_list = []
        if empty_topics:
            for et in empty_topics:
                tid = et.get_attribute('id').split('-')[1]
                empty_topics_list.append(int(tid))
            print(empty_topics_list)
            return empty_topics_list
        else:
            print("<No empty topic in this section, creating new one...>")
            self.create_topic(topic_name='', new=True)
            return self.find_all_empty_topic_ids()


    def __edit_activity(self, activity_name, feature):
        self.turn_editing_on()
        edit_elem = get_element_by_xpath(self.driver, 1, f"//span[@class='instancename'][text()='{ activity_name }']/following::a[normalize-space(text()) = 'Edit'][1]")
        feature_elem = get_element_by_xpath(self.driver, 1, f"//span[@class='instancename'][text()='{ activity_name }']/following::a[normalize-space(text()) = 'Edit'][1]/following::span[@class='menu-action-text'][normalize-space(text()) = '{ feature }']")
        self.driver.execute_script("window.scrollTo(0, 0)")
        ActionChains(self.driver).move_to_element(edit_elem).click().pause(1).move_to_element(feature_elem).click().perform()
    
    def edit_activity_settings(self, activity_name):
        self.__edit_activity(activity_name, "Edit settings")
        print(f"<editing \"{activity_name}\">")
    
    def hide_activity(self, activity_name):
        self.__edit_activity(activity_name, "Hide")
        print(f"<\"{activity_name}\" was hidden>")
    
    def delete_activity(self, activity_name):
        self.__edit_activity(activity_name, "Delete")
        get_element_by_xpath(self.driver, 1, "//input[@type='button'][@value='Yes']").click() # Confirm delete
        print(f"<\"{activity_name}\" was deleted>")
    
    def set_activity_avaliable_start_date(self, start_date):
        if isinstance(start_date, datetime.datetime):
            self.activity_ava_start_date = start_date
    
    def set_activity_avaliable_end_date(self, end_date):
        if isinstance(end_date, datetime.datetime):
            self.activity_ava_end_date = end_date

