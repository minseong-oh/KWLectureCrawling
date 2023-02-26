from user_agent import generate_user_agent
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
    
    pyautogui.click(800,600)
    
    time.sleep(10)
    #로그인 버튼 클릭 
    login_btn = driver.find_element_by_tag_name("input")
    login_btn.send_keys(Keys.RETURN)
    time.sleep(randomTime())

    #강의실 페이지로 이동
    driver.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()
    time.sleep(randomTime())


def collectReviews(lecture, professor):
    # 강의평 위치로 이동
    search = driver.find_element_by_name("keyword")
    search.send_keys(lecture)
    time.sleep(randomTime())
    driver.find_element_by_class_name('submit').click()
    time.sleep(randomTime())
    
    size = len(driver.find_elements_by_class_name("lecture"))
    
    for i in range(1,size+1):
        # 해당 과목을 맡은 교수가 존재하는지 확인 없으면 리턴
        name = driver.find_element_by_xpath('/html/body/div/div/div[2]/a[{}]/div[2]'.format(i))
        if name.text == professor:
            break
    if name.text != professor:
        driver.back()
        return "알수없음"
            
    name.click()
    time.sleep(randomTime())
    
    # 리뷰 수집 시작
    try:
        driver.find_element_by_class_name('more').click()
    except: # 강의평이 없는 경우
        return "알수없음"
    
    time.sleep(randomTime())
    reviewSize = len(driver.find_elements_by_class_name("article"))
    # 리뷰 최대 10개만 수집
    if reviewSize>10:
        reviewSize=10
    
    review = ''
    for i in range(1,reviewSize):
        res = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/div[2]/div[{}]/div[2]'.format(i)).text
        
        review += res+' '
        time.sleep(randomTime())
        
    driver.back()
    time.sleep(randomTime())
    driver.back()
    time.sleep(randomTime())
    driver.back()
    time.sleep(randomTime())
    
    return review
            
            

if __name__ == '__main__':
    #selenium 라이브러리로 Chrome 불러오기
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
    fileName = "2022년2학기.csv"
    df = pd.read_csv(fileName)
    info = df[['과목명','담당교수']]
    
    reviews = dict()
#    for i in range(info.shape[0]):
#        lecture, professor = info.과목명[i], info.담당교수[i]
#        reviews[(lecture, professor)] = collectReviews(lecture, professor)
    collectReviews(info.과목명[18], info.담당교수[18])
    
