import time
from selenium import webdriver
import json
from selenium.webdriver.common.by import By
import aliVendorConfig
import pymysql


def getDatabaseConnection4Vendor():
    mysqlConn4Vendor = pymysql.connect(host=aliVendorConfig.aliVendorConfig['aliVendor']['db']['host'],
                                       port=aliVendorConfig.aliVendorConfig['aliVendor']['db']['port'],
                                       user=aliVendorConfig.aliVendorConfig['aliVendor']['db']['user'],
                                       password=aliVendorConfig.aliVendorConfig['aliVendor']['db']['pass'],
                                       database=aliVendorConfig.aliVendorConfig['aliVendor']['db']['dbName'])

    return mysqlConn4Vendor


def getProductIds(_begin, _offset, _categoryOne, _categoryThree):
    try:
        _connection = getDatabaseConnection4Vendor()

        _cursor = _connection.cursor()
        _cursor.execute("select offer_id from product_vendor_1688 where category_one = '" +
                        _categoryOne + "' and category_three= '" + _categoryThree + "'order by id asc limit "
                        + str(_begin) + "," + str(_offset))
        _productIds = _cursor.fetchall()

        _connection.commit()

        return _productIds
    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()

        return []
    finally:
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def initProductIds(_userName, _categoryUrl, _categoryOne, _categoryThree):
    try:
        driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(3)

        driver.delete_all_cookies()

        cookie = open("/Users/gilbert/vendor-info/" + str(_userName) + ".cookie", 'r')
        cookie_str = cookie.read()
        cookie.close()
        cookies = json.loads(cookie_str)

        for c in cookies:
            driver.add_cookie(c)

        driver.refresh()

        driver.get(_categoryUrl)

        time.sleep(3)

        c = 0
        off = 2000
        while c < 35:
            off = off + c * 3000
            driver.execute_script("window.scrollBy(0," + str(off) + ")")

            time.sleep(1)

            c = c + 1

        offerIds = driver.find_elements(By.XPATH, "//div[@class='list']/div")

        i = 0
        _connection = getDatabaseConnection4Vendor()
        while i < len(offerIds):
            if offerIds[i].get_attribute('id') != '':
                _cursor = _connection.cursor()
                _offerId = offerIds[i].get_attribute('id')
                _cursor.execute("insert into product_vendor_1688(offer_id, category_one, category_three) values('"
                                + _offerId + "', '" + _categoryOne + "', '" + _categoryThree + "')")

            i = i + 1
        _connection.commit()
    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()
    finally:
        driver.close()

        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


def scrapVendorsByCategory(_categoryUrl, _userName, _productIds):
    try:
        driver = webdriver.Chrome()

        driver.get("https://www.1688.com")

        time.sleep(3)

        driver.delete_all_cookies()

        cookie = open("/Users/gilbert/vendor-info/" + str(_userName) + ".cookie", 'r')
        cookie_str = cookie.read()
        cookie.close()
        cookies = json.loads(cookie_str)

        for c in cookies:
            driver.add_cookie(c)

        driver.refresh()

        time.sleep(1)

        i = 0
        print("本次要处理的商品数:" + str(len(productIds)))
        _connection = getDatabaseConnection4Vendor()
        _cursor = _connection.cursor()
        while i < len(productIds):
            detailUrl = 'https://detail.1688.com/offer/' + productIds[i] + \
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(3)

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
                _cursor.execute("update product_vendor_1688 set title='" + title + "', mobile=" + str(phone) +
                                ", company='" + company + "' where offer_id=" + str(productIds[i]))

            i = i + 1

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])

            _connection.commit()
    except Exception as e:
        print(e.__str__())
        if _connection:
            _connection.rollback()
    finally:
        driver.close()
        if _cursor:
            _cursor.close()
        if _connection:
            _connection.close()


if __name__ == '__main__':
    url = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryUrl']
    userName = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['user']
    categoryOne = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryOne']
    categoryThree = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['categoryThree']
    begin = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['begin']
    offset = aliVendorConfig.aliVendorConfig['aliVendor']['ali']['offset']

    initProductIds(userName, url, categoryOne, categoryThree)

    rows = getProductIds(begin, offset, categoryOne, categoryThree)
    productIds = []
    for row in rows:
        productIds.append(row[0])

    scrapVendorsByCategory(url, userName, productIds)

