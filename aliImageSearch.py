import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import requests
import aliImageSearchConst
import random


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


def getCookie(userName):
    if aliImageSearchConst.ALI_COOKIES is None:
        file = open("/opt/apps/kp-1688-search/" + userName + ".cookie", 'r')
        # file = open("/Users/gilbert/vendor-info/" + userName + ".cookie", 'r')
        cookie_str = file.read()
        file.close()
        cookies = json.loads(cookie_str)

        aliImageSearchConst.ALI_COOKIES = cookies

    return aliImageSearchConst.ALI_COOKIES


def initChrome(userName):
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

        cookies = getCookie(userName)

        for cookie in cookies:
            driver.add_cookie(cookie)

        driver.refresh()

        return driver
    except Exception as e:
        print(e.__str__())

        driver.close()

        return None


def getDriver(userName):
    return initChrome(userName)


def initChromePool(size):
    _chrome_drivers = []
    i = 0
    while i < size:
        _chrome_drivers.append(getDriver('tq02h2a_gb1981'))
        i = i + 1

    return _chrome_drivers


chrome_drivers = initChromePool(1)


def getDriverFromPool(size):
    index = random.randint(0, 99) % size

    return chrome_drivers[index]


def aliSearch():
    try:
        _driver = getDriverFromPool(1)

        _driver.get("https://s.1688.com/selloffer/offer_search.html")

        time.sleep(1)

        _driver.find_element(By.XPATH, "//div[@id='img-search-upload']").click()

        time.sleep(1)

        pyautogui.typewrite(r'/tmp/t.png', interval=0.1)

        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.press('enter')

        time.sleep(1)

        products = _driver.find_elements(By.XPATH, "//div[@class='img-container']/div/a/div[@class='img']")

        urls = []
        for detail in products:
            urlStr = detail.get_attribute('style')

            begin = urlStr.index("url") + 5
            urlStr = urlStr[begin:len(urlStr) - 3]

            urls.append(urlStr)

        return urls
    except Exception as e:
        print(e.__str__())

        return []




