import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import aliCookieConfig
import threading


def check_task(name):
    for user in aliCookieConfig.config['aliCookie']['users']:
        try:
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

            cookie = open("/opt/apps/kp-aliWangWang-chat/" + str(user) + ".cookie", 'r')
            cookie_str = cookie.read()
            cookie.close()
            cookies = json.loads(cookie_str)

            for c in cookies:
                driver.add_cookie(c)

            driver.refresh()

            cartUrl = "https://cart.1688.com/cart.htm"

            driver.get(cartUrl)

            time.sleep(3)

            driver.find_element(By.XPATH, "//div[contains(text(), '现货')]").click()
        except Exception as e:
            alert = {
                'msgtype': 'text',
                'text': {
                    'content': str('1688账号') + str(user) + str('异常探测结果：失败，请检查账号有效性。') + str(e.__str__())
                }
            }
            requests.post(aliCookieConfig.config['aliCookie']['robot'], json=alert)
        finally:
            driver.close()


def loop_checker(name):
    while 1:
        check_task(name)
        time.sleep(aliCookieConfig.config['aliCookie']['interval'])


def start_checker():
    thread = threading.Thread(target=loop_checker, args=("1688-account-checker",))
    thread.start()


