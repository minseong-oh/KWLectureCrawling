# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd

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
    

def lookUp():
    # 2022년 2학기로 선택
    driver.find_element_by_xpath('//*[@id="selectYear"]/option[2]').click()
    driver.find_element_by_xpath('//*[@id="selecthakgi"]/option[3]').click()
    
    df = pd.read_csv("2022년2학기.csv")
    
    for i in range(df.shape[0]):
        
        # 과목과 담당교수 입력
        lecture = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[1]/input')
        lecture.clear()
        lecture.send_keys(df.과목명[i])
        
        professor = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[2]/td[2]/input')
        professor.clear()
        professor.send_keys(df.담당교수[i])
        
        time.sleep(1.5)
        
        # 인증코드
        code = driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[5]/td/span').text
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[5]/td/input').send_keys(code)
        
        # 강의정보 조회
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/div/button').send_keys(Keys.RETURN)
        time.sleep(1.5)
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[2]/tbody/tr/td[2]').click()
        time.sleep(1)
        
        # 수강인원 조회
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[2]/table[1]/tbody/tr[4]/td[2]/button').click()
        
        driver.switch_to.window(driver.window_handles[1]) 
    
        code = driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/span').text
        driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/input').send_keys(code)
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/table/tbody/tr/td/button[2]').click()
        time.sleep(1)
        people = driver.find_element_by_xpath('//*[@id="appModule"]/div/div[2]/div/b[2]').text
        
        print(people)
        driver.switch_to.window(driver.window_handles[0])
        driver.find_element_by_xpath('//*[@id="appModule"]/div[2]/div[1]/span/button').click()


if __name__ == "__main__":
    #selenium라이브러리로 Chrome 불러오기
    chromedriver ='C:\\Users\\minseong\\Desktop\\MyStudy\\project_광운대학교_강의추천\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)

    login("학번", "비번")
    lookUp()
    
