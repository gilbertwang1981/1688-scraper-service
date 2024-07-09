import time
from selenium.webdriver.common.by import By
from aliWangWangChat import ChatObject
import aliWangWangConnection


def getChatHistory(offerId, userName):
    with aliWangWangConnection.global_chat_lock:
        try:
            driver = aliWangWangConnection.getChromeInstance(userName)

            detailUrl = 'https://detail.1688.com/offer/' + offerId +\
                        '.html?spm=a26352.13672862.offerlist.59.2fac1e62cO65Hm' \
                        '&cosite=-&tracelog=p4p&_p_isad=1&' \
                        'clickid=fcf11b87a6f14ad796969a9a52836c9b&' \
                        'sessionid=a659238081d473668bf0881d132d92ee'

            driver.get(detailUrl)

            time.sleep(2)

            driver.maximize_window()

            time.sleep(1)

            driver.find_element(By.XPATH,
                                "//div[@class='pi-layout-container']"
                                "//a/img[contains(@src, '-tps-28') or contains(@src, '-tps-134')]").click()

            time.sleep(2)

            try:
                driver.find_element(By.XPATH, "//button[text()='优先使用网页版']").click()

                time.sleep(1)
            except Exception as e:
                print("忽略:" + e.__str__())

            windows = driver.window_handles
            driver.switch_to.window(windows[-1])
            driver.maximize_window()

            time.sleep(2)

            chat_url = driver.find_element(By.XPATH, "//div[@id='ice-container']//iframe").get_attribute("src")

            driver.get(chat_url)

            time.sleep(3)

            driver.maximize_window()

            time.sleep(1)

            elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'message-item-line')]")

            chatHistory = []

            for el in elements:
                content = el.text.split('\n')
                data = ChatObject()
                if len(content) >= 2:
                    data.user = content[0]
                    data.time = content[1]
                    if len(content) > 2:
                        data.chats.append(content[2])

                    chatHistory.append(data)
        except Exception as e:
            print(e.__str__())

        return chatHistory
