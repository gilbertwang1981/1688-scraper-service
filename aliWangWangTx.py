import json
from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def chatWithCustomer(offerId, chatList, userName):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Version: 126, Browser and Driver
    service = Service('/opt/ansible/ansible/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.1688.com")

    time.sleep(3)

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

    driver.maximize_window()

    time.sleep(3)

    driver.find_element(By.XPATH,
                        "//div[@class='pi-layout-container']"
                        "//a/img[contains(@src, '-tps-28') or contains(@src, '-tps-134')]").click()

    time.sleep(2)

    driver.find_element(By.XPATH, "//button[text()='优先使用网页版']").click()

    time.sleep(1)

    windows = driver.window_handles
    driver.switch_to.window(windows[-1])
    driver.maximize_window()

    time.sleep(2)

    chat_url = driver.find_element(By.XPATH, "//div[@id='ice-container']//iframe").get_attribute("src")

    driver.get(chat_url)

    time.sleep(7)

    driver.maximize_window()

    time.sleep(3)

    for chatContent in chatList:
        driver.find_element(By.XPATH, "//div[@class='ww_input']//pre").send_keys(chatContent)

        driver.find_element(By.XPATH, "//div/button/span").click()

        time.sleep(2)

    time.sleep(3)

    driver.close()

