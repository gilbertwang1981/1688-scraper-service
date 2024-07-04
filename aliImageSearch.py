import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import aliImageSearchConst


def getCookie(userName):
    if aliImageSearchConst.ALI_COOKIES is None:
        # file = open("/opt/apps/kp-1688-search/" + userName + ".cookie", 'r')
        file = open("/Users/gilbert/vendor-info/" + userName + ".cookie", 'r')
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
        # driver = webdriver.Chrome(service=service, options=chrome_options)
        driver = webdriver.Chrome()

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


def initChromePool():
    _chrome_drivers = [getDriver('15876578981'), getDriver('tq02h2a_gb1981')]

    return _chrome_drivers


chrome_drivers = initChromePool()


def getDriverFromPool():
    with aliImageSearchConst.indexLocking:
        aliImageSearchConst.index = aliImageSearchConst.index + 1

        return chrome_drivers[aliImageSearchConst.index % len(chrome_drivers)]


def aliSearch(imageUrl):
    try:
        _driver = getDriverFromPool()

        _driver.get("https://s.1688.com/selloffer/offer_search.html")

        time.sleep(1)

        _driver.find_element(By.XPATH, "//input[@id='alisearch-input']").send_keys(imageUrl)

        time.sleep(1)

        _driver.find_element(By.XPATH, "//button[contains(text(), '搜')]").click()

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




