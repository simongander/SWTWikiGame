from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import re

url = 'https://en.wikipedia.org/wiki/Special:Random'

driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(0.5)

print(driver.title)

while driver.title != 'Philosophy - Wikipedia':
    test = driver.find_element(By.ID, "mw-content-text")
    match = False

    for p in test.find_elements(By.TAG_NAME, "p"):
        p_text = p.get_attribute("outerHTML")
        for a in p.find_elements(By.TAG_NAME, "a"):
            if a.get_attribute("href") and a.text:
                a_text = a.get_attribute("outerHTML")
                pattern_1 = re.compile(rf'\(.*?{re.escape(a_text)}.*?\)')
                pattern_2 = re.compile(r'\[.*[0-9]+\]')
                match_1 = pattern_1.search(p_text)
                match_2 = pattern_2.search(a_text)
                if match_1 is None and match_2 is None:
                    match = True
                    break
        if match:
            break

    if match:
        print(driver.title)
        a.click()
    else:
        print("No clickable link found.")
        driver.quit()
        break
