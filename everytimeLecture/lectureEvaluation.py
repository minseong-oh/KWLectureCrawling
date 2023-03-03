from user_agent import generate_user_agent
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
import random
import time 
import pyautogui
import pickle
import pandas as pd

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


# 과제, 조모임, 성적, 출결, 시험, 평점 추출
def GetInfo(lecture, professor):
    search = driver.find_element_by_xpath("/html/body/div/div/div[1]/form/input[1]")
    search.clear()
    time.sleep(1)
    search.send_keys(lecture)
    time.sleep(randomTime())
    
    try:
        driver.find_element_by_class_name('submit').click()
        time.sleep(randomTime())
    except:
        return [-1]*6
    
    size = len(driver.find_elements_by_class_name("lecture"))
    for i in range(1,size+1):
        # 해당 과목을 맡은 교수가 존재하는지 확인 없으면 리턴        
        name = driver.find_element_by_xpath('/html/body/div/div/div[2]/a[{}]/div[2]'.format(i))
        if name.text == professor:
            break
        
    if name.text != professor:
        time.sleep(randomTime())
        return [-1] * 6
            
    name.click()
    time.sleep(randomTime())
    
    # 과제, 조모임, 성적, 출결, 시험, 평점 추출
    totalEvaluation = evaluation()
    return totalEvaluation



'''
별점 먼저 확인
별점이 존재하면 두가지 모두 확인 (try-except)
별점이 존재하지 않으면 [-1]*6 return 
'''

def evaluation():
    # 1: 과제 없음/ 2: 과제 보통/ 3: 과제 많음
    # 1: 조모임 없음/ 2. 조모임 보통/ 3. 조모임 많음
    # 1. 성적 너그러움/ 2. 성적 보통/ 3. 성적 깐깐함
    res = []
    
    # 별점 
    try:
        score_rate = float(driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[1]/div[1]/span[1]').text)
        res.append(score_rate)
    except:  # 별점이 없는 경우 예외처리가 됨.
        driver.back()
        time.sleep(randomTime())
        return [-1]*6
    
    
    # 퍼센트로 이뤄진 강의평가
    # 과제, 조모임, 성적 평가 비율
    try:
        for j in range(1,4):
            high_rate = [-1,-1]
            for i in range(1,4):
                rate = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[{}]/div/div[{}]/div[2]'.format(j,i)).text
                rate = [int(rate[:-1]), i]
                high_rate = max(high_rate, rate)
            res.append(high_rate[1])
            time.sleep(randomTime())
            
        # 출결, 시험
        attendance = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[4]/div/span').text
        test = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[5]/div/span').text
        time.sleep(randomTime())
        
        res.append(attendance)
        res.append(test)
        
        driver.back()
        time.sleep(randomTime())

        return res
    
        
    # 퍼센트로 이뤄진 강의평가가 아닌 경우
    except:
        try:
            for i in range(1,4):
                data = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[1]/div[{}]/span'.format(i)).text
                res.append(data)
                time.sleep(randomTime())
            
            # 출결, 시험
            attendance = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[2]/div/span[1]').text
            test = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[3]/div/span').text
            time.sleep(randomTime())
            
            res.append(attendance)
            res.append(test)
            
            driver.back()
            time.sleep(randomTime())

            return res
        
        except:     # 별점만 있고 세부적인 내용은 없는 경우
            driver.back()
            time.sleep(randomTime())

            return [score_rate] + [-1]*5
        

if __name__ == '__main__':
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
    
    df = pd.read_csv("2022년2학기.csv")
    df['평점'] = -1
    df['과제'] = -1
    df['조모임'] = -1
    df['성적'] = -1
    df['출결'] = -1
    df['시험'] = -1
    
    
    eval_data = []
    for i in range(df.shape[0]):
        eval_data.append(GetInfo(df.과목명[i], df.담당교수[i]))
        print(i, "ok")
        time.sleep(randomTime())
        
    with open("listEvaluation.pkl","wb") as f:
        pickle.dump(eval_data, f)
        
    df[['평점','과제','조모임','성적','출결','시험']] = pd.DataFrame(eval_data)
    df.to_csv("lectureEval.csv", index=False)
