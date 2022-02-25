import time

import null
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import collections as co
import datetime
from datetime import timedelta

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://play.google.com/store/apps/details?id=com.ibk.android.ionebank&hl=ko&gl=US&showAllReviews=true"

options = webdriver.ChromeOptions()
options.add_argument('headless')
driverPath = "/Users/ibk/Documents/libs/chromedriver"
# driver = webdriver.Chrome(driverPath)
driver = webdriver.Chrome(driverPath, chrome_options=options)
driver.get(url)

# 관련성순 -> 최신 순서 변경
driver.find_element_by_xpath("//span[@class='DPvwYc']").click()
time.sleep(5)
#/span[@class='vRMGwf oJeWuf']
#/div[@class='kRoyt MbhUzd ziS7vd']
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@jsname='wQNmvb']/div[@class='kRoyt MbhUzd ziS7vd']"))).click()
# recent_button =
driver.find_element_by_xpath("/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/c-wiz/div[1]/div/div[2]/div[1]").click()
# recent_button.click()
# recent_button.send_keys(Keys.ENTER)


SCROLL_PAUSE_TIME = 1.5
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # (1) 4번의 스크롤링
    for i in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
    # (2) 더보기 클릭
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='RveJvd snByac']"))).click()
    except TimeoutException:
        print("timeout")
    except ElementClickInterceptedException:
        print("ElementClickInterceptedException")

    # (3) 종료 조건
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

merged_reviews = []
reviews = driver.find_elements_by_xpath("//span[@jsname='bN97Pc']")
for i in range(len(reviews)):
    # print(str(i) + "\t" + reviews[i].text)
    # if reviews[i].text != '':
    merged_reviews.append(reviews[i].text)

dates = driver.find_elements_by_xpath("//div[@class='bAhLNe kx8XBd']/div/span[@class='p2TkOb']")
stars = driver.find_elements_by_xpath("//span[@class='nt2C1d']/div[@class='pf5lIe']/div[@role='img']")
likes = driver.find_elements_by_xpath("//div[@aria-label='이 리뷰가 유용하다는 평가를 받은 횟수입니다.']")

print(len(merged_reviews), len(dates), len(likes), len(stars))
res_deque = co.deque([])
for i in range(len(dates)):
    res_deque.append({
        'NO': i+1,
        '내용': merged_reviews[i],
        '날짜': dates[i].text,
        '평점': stars[i].get_attribute('aria-label')[10],
        'LIKE': likes[i].text if likes[i].text else '0'
    })

#타임스탬프를 찍어주기 위해 날짜 작업
timestamp = datetime.datetime.today().strftime("%Y%m%d%H%M%S")

res_df = pd.DataFrame(res_deque)
res_df.to_csv('./app_review_' + timestamp + '.csv', index=False, encoding='utf-8-sig')
