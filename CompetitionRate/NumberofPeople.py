# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time 
#라이브러리 불러오기

chromedriver ='C:\\Users\\minseong\\Desktop\\MyStudy\\project_광운대학교_강의추천\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)
#selenium라이브러리로 Chrome 불러오기

driver.get('https://everytime.kr/login')
id_every = driver.find_element_by_name("userid")
#userid인 요소 가져오기 
id_every.send_keys("*^^*")
#아이디 입력


pwd_every = driver.find_element_by_name("password")
#password인 요소 가져오기  
pwd_every.send_keys("*^^*")
#비밀번호 입력 

login_btn =driver.find_element_by_tag_name("input")
login_btn.send_keys(Keys.RETURN)
#로그인 버튼 클릭

time.sleep(2)

#강의실 페이지로 이동
driver.find_element_by_xpath('//*[@id="menu"]/li[2]/a').click()

time.sleep(2)


driver.find_element_by_xpath('//*[@id="semesters"]/option[6]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()


time.sleep(2)

scroll_element = driver.find_element_by_class_name("list")
prev_height = scroll_element.get_attribute("scrollHeight")
print(prev_height)

while True:

    #스크롤 내리기
    driver.execute_script("arguments[0].scrollBy(0, {})".format(30000), scroll_element)

	#시간대기
    time.sleep(2)

	#현재높이 저장
    current_height = scroll_element.get_attribute("scrollHeight")
    print(current_height)
    
	#현재높이와 끝의 높이가 끝이면 탈출
    if current_height == prev_height:
    	break
	#업데이트해줘서 끝낼 수 있도록
    prev_height = current_height


# for i in range(1,1278):
#    for j in range(1,10):
# 교선 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[1]
# 학수번호: //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[2]
# 강의명 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[3]
#  교수명 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[4]
# 학점 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[5]
# 시간 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[6]
# 담은 인원 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[8]
# 유의사항 : //*[@id="subjects"]/div[2]/table/tbody/tr[1277]/td[9]



