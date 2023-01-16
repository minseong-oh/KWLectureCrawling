# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd


def login(stdNum, password):
    #selenium라이브러리로 Chrome 불러오기
    chromedriver ='C:\\Users\\minseong\\Desktop\\MyStudy\\project_광운대학교_강의추천\\chromedriver_win32\\chromedriver.exe'
    driver = webdriver.Chrome(chromedriver)
    
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
    

login(학번, 비번)
