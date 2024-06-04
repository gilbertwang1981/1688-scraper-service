import base64
import random

import time

import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def get_tracks(distance):
    # 分割加减速路径的阀值
    value = round(random.uniform(0.55, 0.75), 2)
    # 划过缺口 20 px
    distance += 5
    # 初始速度，初始计算周期， 累计滑动总距
    v, t, sum = 0, 0.7, 0
    # 轨迹记录
    plus = []
    # 将滑动记录分段，一段加速度，一段减速度
    mid = distance * value
    while sum < distance:
        if sum < mid:
            # 指定范围随机产生一个加速度
            a = round(random.uniform(2.5, 3.5), 1)
        else:
            # 指定范围随机产生一个减速的加速度
            a = -round(random.uniform(2.0, 3.0), 1)
        s = v * t + 0.5 * a * (t ** 2)
        v = v + a * t
        sum += s
        plus.append(round(s))

    reduce = [-6, -4, -6, -4]
    return {'plus': plus, 'reduce': reduce}


def findfic(target, template):
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    distance = min_loc[0]

    return distance


driver = webdriver.Chrome()

driver.get("https://mdm4.idatachina.com/")
time.sleep(2)
driver.maximize_window()
time.sleep(1)

driver.find_element(By.XPATH, "//input[@type='text']").send_keys('kpcs')
driver.find_element(By.XPATH, "//input[@type='password']").send_keys('kp@123456')
driver.find_element(By.XPATH, "//div/button").click()

actions = ActionChains(driver)
slider = driver.find_element(By.XPATH, "//div[@id='slider-button']")
actions.click_and_hold(slider)
actions.move_to_element(slider)
actions.perform()

time.sleep(3)

sliderImg = driver.find_element(By.XPATH, "//img[@class='slide-block']").get_attribute("src")

image_data_0 = sliderImg.split(";base64,")[1]
image_bytes_0 = base64.b64decode(image_data_0)
with open("slider.png", "wb") as f:
    f.write(image_bytes_0)

backgroundImg = driver.find_element(By.XPATH, "//img[@class='slide-canvas']").get_attribute("src")
image_data_1 = backgroundImg.split(";base64,")[1]
image_bytes_1 = base64.b64decode(image_data_1)
with open("background.png", "wb") as f:
    f.write(image_bytes_1)

distance = findfic("background.png", "slider.png")
print(distance)
trajectory = get_tracks(distance + 4)

ActionChains(driver).click_and_hold(slider).perform()
for track in trajectory['plus']:
    ActionChains(driver).move_by_offset(
        xoffset=track,
        yoffset=round(random.uniform(1.0, 3.0), 1)
    ).perform()

for back_tracks in trajectory['reduce']:
    ActionChains(driver).move_by_offset(
        xoffset=back_tracks,
        yoffset=round(random.uniform(1.0, 3.0), 1)
    ).perform()

for i in [-4, 4]:
    ActionChains(driver).move_by_offset(
        xoffset=i,
        yoffset=0
    ).perform()

ActionChains(driver).release().perform()
time.sleep(5)

driver.close()


