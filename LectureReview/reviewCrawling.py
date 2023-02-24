from user_agent import generate_user_agent, generate_navigator
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time 
import random
import pandas as pd
import pyautogui


def randomTime():
    return random.uniform(3,5)

def login(userid, password):
    #아이디 입력
    id_every = driver.find_element_by_name("userid")
    id_every.send_keys(userid)
    
    
    #비밀번호 입력 
    pwd_every = driver.find_element_by_name("password")
    pwd_every.send_keys(password)
    time.sleep(randomTime())
    
    # 리캡챠 화나네
    pyautogui.click(800,600)
    
    time.sleep(randomTime())
    #로그인 버튼 클릭 
    login_btn = driver.find_element_by_tag_name("input")
    login_btn.send_keys(Keys.RETURN)
    time.sleep(randomTime())

    #강의실 페이지로 이동
    driver.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()
    time.sleep(randomTime())



if __name__ == '__main__':
    #selenium라이브러리로 Chrome 불러오기
    options = wd.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    agent = generate_user_agent(device_type='desktop')
    options.add_argument(f"user-agnet={agent}")   
    driver = wd.Chrome(executable_path='chromedriver_win32\\chromedriver', options = options)
    driver.maximize_window()
    
    driver.get('https://everytime.kr/login')
    time.sleep(randomTime())
    login("아이디", "비밀번호")
