from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

# 플레이리스트 목록 기본 url
# =>  https://www.jamendo.com/explore/playlists
# 60개 크롤링할 때 한 10~15분


# 1. 크롬 드라이버 버전에 맞게 다운받아 같은 폴더에 준비
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')
driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(1000)


# 2. 키워드에 맞게 검색
base_url = 'https://www.jamendo.com/playlist'


# ** 플레이리스트에 따라 이 부분 변경해줘야함 **
emotion_url = '/500605176/chill-zone'  # 1) 검색할 플레이리스트 url 뒷부분
filename = 'chill-zone'  # 2) 결과로 출력할 파일명
playlist_id = 0  # 3) 플레이리스트 식별할 고유 번호 (ex. chill-zone 0번, Indie는 1번..)

driver.get(url=base_url + emotion_url)


# 3. dataframe에 넣을 준비
title_list = []
singer_list = []
img_list = []

# 세부 페이지 이동 후 이미지 주소 추출하는 함수


def next_page(next_url):
    driver2 = webdriver.Chrome('chromedriver', options=options)
    driver2.get(url=next_url)
    driver2.implicitly_wait(200)

    element = driver2.find_element_by_class_name('hero-cover')

    img = element.find_element_by_tag_name('img').get_attribute('src')
    print(img)

    driver2.close()
    return img


# 4. title, singer, img_url 추출해서 리스트에 저장
elements = driver.find_elements_by_xpath(
    '/html/body/div[1]/div[2]/div/ul/li[1]/div/div[1]/ul/li')

for element in elements:
    title = element.find_element_by_class_name("track_information_title").text
    singer = element.find_element_by_class_name(
        "track_information_artist").text

    # 이미지url은 세부 페이지로 이동 후 추출
    next_url = element.find_element_by_tag_name(
        'a').get_attribute('href')
    img = next_page(next_url)

    title_list.append(title)
    singer_list.append(singer)
    img_list.append(img)


# 5. csv 파일로 가공 후 저장
raw_data = {'id': playlist_id,
            'title': title_list,
            'singer': singer_list,
            'img_url': img_list
            }

dataframe = pd.DataFrame(raw_data)

dataframe.to_csv(filename + '.csv', index=False)

sleep(3)
driver.close()
