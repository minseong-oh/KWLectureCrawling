from user_agent import generate_user_agent
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import time 
import random
import pandas as pd
import pyautogui
import pickle

def randomTime():
    return random.uniform(2,4.5)

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
    
    search = driver.find_element_by_xpath('/html/body/div/div/div[1]/div/form/input[1]')
    search.send_keys('이동')
    time.sleep(1)
    driver.find_element_by_class_name('submit').click()
    time.sleep(randomTime())
    

def collectReviews(lecture, professor):
    # 강의평 위치로 이동
    search = driver.find_element_by_xpath('/html/body/div/div/div[1]/form/input[1]')
    search.clear()
    time.sleep(1)
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
        time.sleep(randomTime())
        return "알수없음"
            
    name.click()
    time.sleep(randomTime())
    
    # 리뷰 수집 시작
    try:
        driver.find_element_by_class_name('more').click()
    except: # 강의평이 없는 경우
        driver.back()
        time.sleep(randomTime())
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
        time.sleep(random.uniform(1,3))
        
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
    
    '''
    강의 수가 너무 많아서 나눠서 저장.
    6:17 ->  200개 진행 -> 7:50 완료
    8:27 -> 200개 진행 -> 10:02 완료
    10:15 -> 100개 진행 -> 10:55 완료
    3:55 -> 나머지 진행 -> 11:57 완료
    '''
    
    info = df[['과목명','담당교수']]
    
    reviews = dict()
    for i in range(info.shape[0]):
        lecture, professor = info.과목명[i], info.담당교수[i]
        reviews[(lecture, professor)] = collectReviews(lecture, professor)
        print(i," ok")
        
    # pkl 파일로 저장
    with open("LectureReviews.pkl", "wb") as f:
        pickle.dump(reviews, f)
    
    '''pickle 불러오기
    with open("LectureReviews.pkl", "rb") as f:
        d = pickle.load(f)
    '''
