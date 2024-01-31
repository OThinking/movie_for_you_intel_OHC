from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import pandas as pd
import re
import time
import datetime

options = ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#크롤링할려는 페이지 -> 마우스 오른쪽 클릭 -> 검사 -> 네트워크 -> 새로고침 -> 아무거나 눌러서 ->
options.add_argument("user_agent=" + user_agent)
options.add_argument("lang=ko_KR")
# options.add_argument() # 웹사이즈 크기 조정
# 모바일의 경우에는 페이지가 다르게 만들어진다 (반응형 웹) -> 확인방법: 검사 -> toggle divice toolbar확인

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

start_url = 'https://m.kinolights.com/discover/explore'
button_movie_tv_xpath = '//*[@id="contents"]/section/div[3]/div/div/div[3]/button'
button_movie_xpath = '//*[@id="contents"]/section/div[4]/div[2]/div[1]/div[3]/div[2]/div[2]/div/button[1]'
button_ok_xpath = '//*[@id="applyFilterButton"]'
driver.get(start_url)
time.sleep(0.5)
button_movie_tv = driver.find_element(By.XPATH, button_movie_tv_xpath)
driver.execute_script('arguments[0].click();', button_movie_tv) # 자바스크립트로 되어있어서 변형해준다
time.sleep(1)
button_movie = driver.find_element(By.XPATH, button_movie_xpath)
driver.execute_script('arguments[0].click();', button_movie)
time.sleep(1)
button_ok = driver.find_element(By.XPATH, button_ok_xpath)
driver.execute_script('arguments[0].click();', button_ok)
time.sleep(1)

for i in range(2):
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(1)
list_review_url = []
movie_titles = []
for i in range(1, 10):
    base = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/a').get_attribute("href")
    list_review_url.append(f"{base}/reviews") # 모두 보기 리뷰로 바로감
    title = driver.find_element(By.XPATH, f'//*[@id="contents"]/div/div/div[3]/div[2]/div[{i}]/div/div[1]').text
    movie_titles.append(title)
print(list_review_url[:5])
print(len(list_review_url))
print(movie_titles)

reviews = []
for url in list_review_url:
    driver.get(url)
    time.sleep(1)
    review = ''
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(1)
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
    time.sleep(1)
    for i in range(1, 31):
        try:
            review_title_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/a[1]/div'.format(i)
            review_more_xpath = '//*[@id="contents"]/div[2]/div[2]/div[{}]/div/div[3]/div/button'.format(i)
            try:
                print(i)
                review_more = driver.find_element(By.XPATH, review_more_xpath)
                driver.execute_script('arguments[0].click();', review_more)
                time.sleep(1)
                review_xpath = '//*[@id="contents"]/div[2]/div[1]/div/section[2]/div/div/div/p'
                review += ' ' + driver.find_element(By.XPATH, review_xpath).text
                driver.back()
                time.sleep(1)
            except:
                review += ' ' + driver.find_element(By.XPATH, review_title_xpath).text
        except:
            print('no more')
    # print(review)
    reviews.append(review + '@@')
print(reviews[:5])
print(len(reviews))
    # reviews.append(review)


# //*[@id="contents"]/div[2]/div[2]/div[1]/div/div[3]/a[1]/div
# //*[@id="contents"]/div[2]/div[2]/div[2]/div/div[3]/a[1]/div

# //*[@id="contents"]/div[2]/div[2]/div[1]/div/div[3]/a[2]/div/p

# def scroll():
#     try:
#         # 페이지 내 스크롤 높이 받아오기
#         last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
#         while True:
#             # 임의의 페이지 로딩 시간 설정
#             # PC환경에 따라 로딩시간 최적화를 통해 scraping 시간 단축 가능
#             pause_time = random.uniform(1, 2)
#             # 페이지 최하단까지 스크롤
#             driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
#             # 페이지 로딩 대기
#             time.sleep(pause_time)
#             # 무한 스크롤 동작을 위해 살짝 위로 스크롤(i.e., 페이지를 위로 올렸다가 내리는 제스쳐)
#             driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight-50)")
#             time.sleep(pause_time)
#             # 페이지 내 스크롤 높이 새롭게 받아오기
#             new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
#             # 스크롤을 완료한 경우(더이상 페이지 높이 변화가 없는 경우)
#             if new_page_height == last_page_height:
#                 print("스크롤 완료")
#                 break
#             # 스크롤 완료하지 않은 경우, 최하단까지 스크롤
#             else:
#                 last_page_height = new_page_height
#     except Exception as e:
#         print("에러 발생: ", e)

# button_one_movie_xpath = '//*[@id="contents"]/div/div/div[3]/div[2]/div[1]/a/div/img'
# button_one_movie = driver.find_element(By.XPATH, button_one_movie_xpath)
# driver.execute_script('arguments[0].click();', button_one_movie)
# time.sleep(1)
#
# button_skip_xpath = '//*[@id="root"]/div/div[2]/div/div/div[3]/button'
# button_skip = driver.find_element(By.XPATH, button_skip_xpath)
# driver.execute_script('arguments[0].click();', button_skip)
# time.sleep(1)
#
# button_review_xpath = '//*[@id="review"]'
# button_review = driver.find_element(By.XPATH, button_review_xpath)
# driver.execute_script('arguments[0].click();', button_review)
# time.sleep(1)
#
# button_review_plus_xpath = '//*[@id="reviewsButton"]/span'
# button_review_plus = driver.find_element(By.XPATH, button_review_plus_xpath)
# driver.execute_script('arguments[0].click();', button_review_plus)
# time.sleep(10)

# //*[@id="contents"]/div/div/div[3]/div[2]/div[1]/a/div/img
# //*[@id="contents"]/div/div/div[3]/div[2]/div[2]/a/div/img

