import json
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def getStoreInfo(offerId, userName):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent='
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) '
                                'Gecko/20100101 Firefox/122.0')

    service = Service('/opt/ansible/ansible/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.1688.com")

    time.sleep(2)

    driver.delete_all_cookies()

    file = open("/opt/apps/kp-aliWangWang-chat/" + userName + ".cookie", 'r')
    cookie_str = file.read()
    file.close()
    cookies = json.loads(cookie_str)

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()

    detailUrl = 'https://detail.1688.com/offer/' + offerId + '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                                                             '&cosite=-&tracelog=p4p&_p_isad=1&' \
                                                             'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                                                             'sessionid=a659238081d473668bf0881d132d92ee'

    driver.get(detailUrl)

    time.sleep(2)

    storeName = driver.find_element(By.XPATH, "//div[@id='shop-container-header']//span").text

    driver.close()

    return storeName