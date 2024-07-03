import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import requests


def downloadImage(img_url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    r = requests.get(img_url, headers=headers, stream=True)
    if r.status_code == 200:
        with open("/tmp/t.png", 'wb') as f:
            f.write(r.content)
        return True


def aliSearch(userName):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--single-process')
        chrome_options.add_argument('--disable-dev-shm-usage')

        # Version: 126, Browser and Driver
        service = Service('/opt/ansible/ansible/chromedriver')
        driver = webdriver.Chrome(service=service, options=chrome_options)
        # driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(1)

        driver.delete_all_cookies()

        file = open("/opt/apps/kp-search-service/" + userName + ".cookie", 'r')
        # file = open("/Users/gilbert/vendor-info/" + userName + ".cookie", 'r')
        cookie_str = file.read()
        file.close()
        cookies = json.loads(cookie_str)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        driver.get("https://s.1688.com/selloffer/offer_search.html")

        time.sleep(1)

        driver.find_element(By.XPATH, "//div[@id='img-search-upload']").click()

        time.sleep(1)

        pyautogui.typewrite("/tmp/t.png", interval=0.25)

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        pyautogui.press('enter')

        time.sleep(1)

        products = driver.find_elements(By.XPATH, "//div[@class='img-container']/div/a")

        urls = []
        for detail in products:
            urls.append(detail.get_attribute('href'))

        return urls
    except Exception as e:
        e.__str__()

        return []
    finally:
        driver.close()

