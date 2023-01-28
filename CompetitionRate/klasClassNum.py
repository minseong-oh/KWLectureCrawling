# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd
from selenium.common.exceptions import NoSuchElementException

def login(stdNum, password):
    
    driver.get('https://klas.kw.ac.kr/std/cps/atnlc/LectrePlanStdPage.do')
    
    #아이디 입력
    id_every = driver.find_element_by_xpath('//*[@id="loginId"]')
    id_every.send_keys(stdNum)
    
    
    #비밀번호 입력 
    pwd_every = driver.find_element_by_xpath('//*[@id="loginPwd"]')
    pwd_every.send_keys(password)
    
    #로그인 버튼 클릭 
    login_btn =driver.find_element_by_class_name("btn")
    login_btn.send_keys(Keys.RETURN)
    time.sleep(2)
    
def searchLecture(index):
    try:
        # 과목과 담당교수 입력
        lecture = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/input')
        lecture.clear()
        lecture.send_keys(df.과목명[index])
        
        # 담당교수 결측값
        if pd.isnull(df.담당교수[index]):
            return False
        
        professor = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[2]/input')
        professor.clear()
        professor.send_keys(df.담당교수[index].split('\n')[0])          
        time.sleep(0.5)
        
        # 인증코드
        code = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[5]/td/span').text
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[5]/td/input').send_keys(code)
        
        # 강의정보 조회
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/div/button').send_keys(Keys.RETURN)
        time.sleep(0.5)
        
        
        # 강의 분반 체크
        table = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[2]/tbody')
        tr = len(table.find_elements_by_tag_name("tr"))
        for idx in range(1,tr+1):
            lectureNum = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[2]/tbody/tr[{}]/td[1]'.format(idx))
            if df.학정번호[index] == lectureNum.text:
                break                    
                
        # 강의 클릭(학정번호 클릭)
        lectureNum.click()
        time.sleep(0.5)
        return True
   
    except NoSuchElementException:
        return False

def checkPeopleNum(index):
    # 수강인원 조회
    try:
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[4]/td[2]/button').click()
    except NoSuchElementException:
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]/button').click()
    
    driver.switch_to.window(driver.window_handles[1]) 

    code = driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/span').text
    driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/input').send_keys(code)
    time.sleep(0.5)
    driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/button[2]').click()
    time.sleep(0.5)
    people = driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/div/b[2]').text
    
    print(people)
    df['total_people'][index] = people
    
    driver.switch_to.window(driver.window_handles[0])
    driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[1]/span/button').click()
    return True
    
    
def lookUp():
    # 2022년 2학기로 선택
    driver.find_element_by_xpath('//*[@id="selectYear"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="selecthakgi"]/option[3]').click()
    
    for i in range(df.shape[0]):
        if not searchLecture(i):
            continue

        checkPeopleNum(i)


    
# 약 2시간 동안 크롤링 진행됨
if __name__ == "__main__":
    #selenium라이브러리로 Chrome 불러오기
    chromedriver ='C:\\Users\\minseong\\Desktop\\MyStudy\\project_광운대학교_강의추천\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    df = pd.read_csv("2022년2학기.csv")
    df['total_people'] = -1      # 수강가능한 인원 초기화
    login("학번", "비밀번호")
    lookUp()
    df.to_csv("klas_total_people.csv", index=False)
