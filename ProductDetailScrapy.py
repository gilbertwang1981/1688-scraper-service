import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from ProductDetail import Product


def crawl_from_1688(url, userName):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('user-agent='
                                '\'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:122.0) '
                                'Gecko/20100101 Firefox/122.0\'')

    service = Service('/opt/ansible/ansible/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get("https://www.1688.com")

    time.sleep(3)

    driver.delete_all_cookies()

    file = open("/opt/apps/kp-1688-product/" + userName + ".cookie", 'r')
    cookie_str = file.read()
    file.close()
    cookies = json.loads(cookie_str)

    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()

    driver.get(url)
    time.sleep(2)
    driver.maximize_window()
    time.sleep(1)

    title = driver.find_element(By.XPATH, "//div[contains(@class, 'title-text')]").text
    price = driver.find_elements(By.XPATH, "//span[contains(@class, 'price-text')]")
    start = driver.find_element(By.XPATH, "//span[contains(@class, 'unit-text')]").text

    products = driver.find_elements(By.XPATH, "//div[@class='od-pc-attribute']//div[@class='offer-attr-list']"
                                              "//div[@class='offer-attr-item']")

    crosses = driver.find_elements(By.XPATH, "//div[@class='od-pc-offer-cross']//div[@class='offer-attr-list']"
                                             "//div[@class='offer-attr-item']")

    p = Product()

    p.title = title

    for product in products:
        pn = product.find_element(By.XPATH, "span[@class='offer-attr-item-name']").text
        pv = product.find_element(By.XPATH, "span[@class='offer-attr-item-value']").text
        if len(pn) > 0 and len(pv) > 0:
            p.pAttrs[pn] = pv

    for c in crosses:
        cn = c.find_element(By.XPATH, "span[@class='offer-attr-item-name']").text
        cv = c.find_element(By.XPATH, "span[@class='offer-attr-item-value']").text
        if len(cn) > 0 and len(cv) > 0:
            p.pCross[cn] = cv

    p.price = price[0].text
    p.start = start

    driver.close()

    return p


