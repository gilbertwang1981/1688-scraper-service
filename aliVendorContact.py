import time
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
import pandas as pd


def scrapVendorsByCategory(categoryUrl, userName, categoryName):
    try:
        driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(3)

        driver.delete_all_cookies()

        cookie = open(str(userName) + ".cookie", 'r')
        cookie_str = cookie.read()
        cookie.close()
        cookies = json.loads(cookie_str)

        for c in cookies:
            driver.add_cookie(c)

        driver.refresh()

        driver.get(categoryUrl)

        time.sleep(3)

        offerIds = driver.find_elements(By.XPATH, "//div[@class='list']/div")
        i = 0
        productIds = []
        while i < len(offerIds):
            if offerIds[i].get_attribute('id') != '':
                productIds.append(offerIds[i].get_attribute('id'))

            i = i + 1

        data = {
            '商品ID': [],
            '商品标题': [],
            '手机号': [],
            '公司': []
        }
        i = 0
        while i < len(productIds):
            detailUrl = 'https://detail.1688.com/offer/' + productIds[i] + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(4)

            try:
                title = driver.find_element(By.XPATH, "//div[@class='title-text']").text

                driver.find_element(By.XPATH, "//a[text()='联系方式']").click()

                time.sleep(5)

                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
                driver.maximize_window()

                phone = driver.find_element(By.XPATH,
                                            "//div[contains(text(), '手机：')]/following-sibling::*[position()=1]").text

                company = driver.find_element(By.XPATH,
                                              "//div[text()='联系方式']/following-sibling::*[position()=1]").text

                if phone != '' and not phone.__contains__('暂无'):
                    data['商品ID'].append(str(productIds[i]))
                    data['商品标题'].append(title)
                    data['手机号'].append(phone)
                    data['公司'].append(company)

            finally:
                i = i + 1

                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
    finally:
        driver.close()
        df = pd.DataFrame(data)
        df.to_excel(categoryName + '.xlsx', index=False)


if __name__ == '__main__':
    url = 'https://show.1688.com/pinlei/industry/pllist.html?spm=a262eq.12572798.jsczhi85.2.751d2fb1q1EcnW&sceneSetId=869&sceneId=7018&bizId=9711'
    userName = 'tq02h2a_gb1981'
    categoryName = '临沂百货'

    scrapVendorsByCategory(url, userName, categoryName)

