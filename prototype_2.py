from selenium import webdriver
from selenium.webdriver.common.by import By
import re


def in_brackets(html, link_html):
    split_html = html.split(link_html, 1)

    in_brackets = split_html[0].count('(') > split_html[0].count(')')
    citation = re.match(r'\[.+\]', link.text) is not None

    return in_brackets or citation


def find_clickable_link(driver):
    content = driver.find_element(By.ID, "mw-content-text")
    tables = [table.get_attribute("outerHTML") for table in content.find_elements(By.TAG_NAME, 'table')]

    for paragraph in content.find_elements(By.TAG_NAME, "p"):
        paragraph_html = paragraph.get_attribute("outerHTML")
        if any(paragraph_html in table for table in tables):  # skip paragraphs in tables
            continue
        italics = [i.get_attribute("outerHTML") for i in paragraph.find_elements(By.TAG_NAME, 'i')]

        for link in paragraph.find_elements(By.TAG_NAME, "a"):
            link_html = link.get_attribute("outerHTML")
            if link.get_attribute('class') == 'new':  # red links are skipped
                continue
            if any(link_html in i for i in italics):  # italicised links links are skipped
                continue
            if in_brackets(paragraph_html, link_html):  # links in brackets are skipped
                continue
            if link.get_attribute("href") and link.text:
                return link
    return False


if __name__ == '__main__':

    url = 'https://en.wikipedia.org/wiki/Special:Random'

    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(0.5)

    print(driver.title)

    while driver.title != 'Philosophy - Wikipedia':
        link = find_clickable_link(driver)
        if link:
            link.click()
            print(driver.title)
        else:
            print("No clickable link found.")
            driver.quit()
            break
