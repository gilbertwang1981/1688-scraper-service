import json
from selenium import webdriver
import time
import pyautogui

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def publishSourcing(userName, subject, amount, price, desc, remark):
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

    sourcingUrl = "https://pinpai.1688.com/page/p_mro_post_buyoffer.htm?" \
                  "source=open&entrySource=work&entrySource=work"

    driver.get(sourcingUrl)

    time.sleep(2)

    driver.maximize_window()

    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@id='subject']").send_keys(subject)

    time.sleep(1)

    category = driver.find_element(By.XPATH, "//input[@id='customCategory']")
    category.click()

    time.sleep(1)

    el0 = driver.find_element(By.XPATH, "//span[text()='玩具']")
    el0.click()
    el0.click()

    time.sleep(2)

    el1 = driver.find_element(By.XPATH, "//span[text()='儿童音乐玩具']")
    el1.click()
    el1.click()

    time.sleep(2)

    el2 = driver.find_element(By.XPATH, "//span[text()='口风琴/笛子/吹奏乐器玩具']")
    el2.click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@id='amount']").send_keys(amount)

    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@id='price']").send_keys(price)

    time.sleep(1)

    driver.find_element(By.XPATH, "//textarea[@id='description']").send_keys(desc)

    time.sleep(1)

    driver.find_element(By.XPATH, "//div[@class='upload--dft']/img").click()

    time.sleep(2)

    pyautogui.typewrite(r'/Users/gilbert/Desktop/test.png', interval=0.15)

    time.sleep(2)

    pyautogui.press('enter')

    time.sleep(1)

    pyautogui.press('enter')

    time.sleep(1)

    el = driver.find_element(By.XPATH, "//input[@class='next-checkbox-input']")
    el.click()
    time.sleep(1)
    el.click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//span[text()='下一步']").click()

    time.sleep(1)

    dt = driver.find_element(By.XPATH, "//input[@placeholder='请选择日期']")
    dt.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//button[@class='next-calendar-btn']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='7月']").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//div[text()='12']").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@id='sendWay']").click()
    time.sleep(1)

    el30 = driver.find_element(By.XPATH, "//span[text()='物流站点自提']")
    el30.click()
    el30.click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//input[@id='invoiceType']").click()
    time.sleep(1)

    el40 = driver.find_element(By.XPATH, "//span[text()='增值税普通发票']")
    el40.click()
    el40.click()

    time.sleep(1)

    driver.find_element(By.XPATH, "//textarea[@id='remark']").send_keys(remark)

    time.sleep(1)

    inputs = driver.find_elements(By.XPATH, "//input[@placeholder='请选择日期']")
    inputs[1].click()

    driver.find_element(By.XPATH, "//button[contains(text(), '月')]").click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//div[text()='7月']").click()
    time.sleep(1)

    days = driver.find_elements(By.XPATH, "//div[text()='2']")
    days[1].click()
    time.sleep(1)

    driver.find_element(By.XPATH, "//button[@groupid='submit']/span[text()='立即发布']").click()

    print("发布成功.")

    time.sleep(2)

    driver.close()

