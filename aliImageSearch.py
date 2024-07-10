import json
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import aliImageSearchConst
import aliImageSearchConfig
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def getCookie(userName):
    file = open(
        aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['cookieDir'] +
        userName + ".cookie", 'r')
    cookie_str = file.read()
    file.close()
    cookies = json.loads(cookie_str)

    return cookies


def initChrome(userName):
    try:
        # Version: 126, Browser and Driver
        if aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['prod'] == 1:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--single-process')
            chrome_options.add_argument('--disable-dev-shm-usage')

            service = Service('/opt/ansible/ansible/chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
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
    _chrome_drivers = []
    for user in aliImageSearchConfig.aliImageSearchConfig['aliImageSearch']['users']:
        _chrome_drivers.append(getDriver(user))

    return _chrome_drivers


chrome_drivers = initChromePool()


def getDriverFromPool():
    with aliImageSearchConst.indexLocking:
        if aliImageSearchConst.CURRENT >= len(chrome_drivers):
            return None
        else:
            aliImageSearchConst.CURRENT = aliImageSearchConst.CURRENT + 1

        aliImageSearchConst.index = aliImageSearchConst.index + 1

        return chrome_drivers[aliImageSearchConst.index % len(chrome_drivers)]


def releaseDriverToPool():
    with aliImageSearchConst.indexLocking:
        if aliImageSearchConst.CURRENT > 0:
            aliImageSearchConst.CURRENT = aliImageSearchConst.CURRENT - 1


def aliSearch(imageUrl):
    _driver = getDriverFromPool()
    if _driver is None:
        return []

    try:
        _driver.get("https://s.1688.com/selloffer/offer_search.html")

        WebDriverWait(_driver, 1).until(EC.presence_of_element_located((By.ID, 'alisearch-input')))

        _driver.find_element(By.XPATH, "//input[@id='alisearch-input']").send_keys(imageUrl)

        _driver.find_element(By.XPATH, "//button[contains(text(), '搜')]").click()

        time.sleep(500/1000)

        products = _driver.find_elements(By.XPATH, "//div[@class='img-container']/div/a/div[@class='img']")

        urls = []
        for detail in products:
            if len(urls) >= 5:
                break

            urlStr = detail.get_attribute('style')

            begin = urlStr.index("url") + 5
            urlStr = urlStr[begin:len(urlStr) - 3]

            urls.append(urlStr)

        return urls
    except Exception as e:
        print(e.__str__())

        return []
    finally:
        releaseDriverToPool()





