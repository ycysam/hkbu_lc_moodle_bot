import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def get_element_by_xpath(driver, second, xpath):
    try:
        return WebDriverWait(driver, second).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    except TimeoutException as tex:
        return WebDriverWait(driver, second).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    except TimeoutException as tex:
        print("Time-out, not able to locate the element." + str(tex))
        return None


def html_quote_escape(html):
    f_html = ''
    for line in html.splitlines():
        f_html += line
    f_html = f_html.replace('"', '\\"')#escape double-quote
    f_html = f_html.replace("'", "\\'")#escape single-quote
    return f_html