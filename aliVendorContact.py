import time
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
import pandas as pd
import os


def scrapVendorsByCategory(_categoryUrl, _userName, _categoryName, _begin, _num):
    try:
        driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(3)

        driver.delete_all_cookies()

        cookie = open(str(_userName) + ".cookie", 'r')
        cookie_str = cookie.read()
        cookie.close()
        cookies = json.loads(cookie_str)

        for c in cookies:
            driver.add_cookie(c)

        driver.refresh()

        driver.get(_categoryUrl)

        time.sleep(3)

        c = 0
        offset = 2000
        while c < 30:
            offset = offset + c * 3000
            driver.execute_script("window.scrollBy(0," + str(offset) + ")")

            time.sleep(1)

            c = c + 1

        offerIds = driver.find_elements(By.XPATH, "//div[@class='list']/div")
        totalNum = len(offerIds)
        print("总共商品数:" + str(totalNum))
        i = _begin
        productIds = []
        end = _begin + _num
        if end > totalNum:
            end = totalNum

        while i < end:
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
        print("本次要处理的商品数:" + str(len(productIds)))
        while i < len(productIds):
            detailUrl = 'https://detail.1688.com/offer/' + productIds[i] + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(3)

            try:
                title = driver.find_element(By.XPATH, "//div[@class='title-text']").text

                driver.find_element(By.XPATH, "//a[text()='联系方式']").click()

                time.sleep(3)

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
            except:
                pass
            finally:
                i = i + 1

                print("current:" + str(i + _begin))

                windows = driver.window_handles
                driver.switch_to.window(windows[-1])
    except:
        pass
    finally:
        driver.close()

        if os.path.exists(_categoryName + '.xlsx'):
            df = pd.read_excel(_categoryName + '.xlsx')
            df = pd.concat([df, pd.DataFrame(data)], axis=0)
        else:
            df = pd.DataFrame(data)

        df.to_excel(_categoryName + '.xlsx', index=False)


if __name__ == '__main__':
    userName = 'tq02h2a_gb1981'
    number = 40

    url = "https://show.1688.com/pinlei/industry/pllist.html?spm=a262eq.12572798.jsczez1k.85.67332fb1XohH0A&&sceneSetId=839&sceneId=40096&bizId=298013&adsSearchWord=%E6%A0%91%E8%84%82%E5%B7%A5%E8%89%BA%E5%93%81"
    categoryName = '树脂工艺品'
    begin = 140

    scrapVendorsByCategory(url, userName, categoryName, begin, number)

