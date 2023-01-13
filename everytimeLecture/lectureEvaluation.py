# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import pandas as pd


#selenium라이브러리로 Chrome 불러오기
chromedriver ='C:\\Users\\minseong\\Desktop\\MyStudy\\project_광운대학교_강의추천\\chromedriver_win32\\chromedriver.exe'
driver = webdriver.Chrome(chromedriver)

driver.get('https://everytime.kr/login')
#아이디 입력
id_every = driver.find_element_by_name("userid")
id_every.send_keys("아이디")


#비밀번호 입력 
pwd_every = driver.find_element_by_name("password")
pwd_every.send_keys("비밀번호")

#로그인 버튼 클릭 
login_btn =driver.find_element_by_tag_name("input")
login_btn.send_keys(Keys.RETURN)
time.sleep(2)

#강의실 페이지로 이동
driver.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()
time.sleep(2)

# 과제, 조모임, 성적, 출결, 시험, 평점 추출
def GetInfo(lecture, professor):
    search = driver.find_element_by_name("keyword")
    search.send_keys(lecture)
   
    try:
        driver.find_element_by_xpath('//*[@id="container"]/form/input[2]').click()
        time.sleep(2)
    except:
        return [-1]*6
    
    size = len(driver.find_elements_by_class_name("lecture"))
    print(size)
    for i in range(1,size+1):
        # 해당 과목을 맡은 교수가 존재하는지 확인 없으면 리턴
        try:
            name = driver.find_element_by_xpath('/html/body/div/div/div[2]/a[{}]/div[2]'.format(i))
            if name.text == professor:
                break
        except:
            return [-1] * 6
            
    name.click()
    time.sleep(2)
    
    # 과제, 조모임, 성적, 출결, 시험, 평점 추출
    homework, team, grade, attendance, test, score_rate = evaluation()
    return [homework, team, grade, attendance, test, score_rate]



'''
별점 먼저 확인
별점이 존재하면 두가지 모두 확인 (try-except 사용)
별점이 존재하지 않으면 [-1]*6 return 
'''

def evaluation():
    # 1: 과제 없음/ 2: 과제 보통/ 3: 과제 많음
    # 1: 조모임 없음/ 2. 조모임 보통/ 3. 조모임 많음
    # 1. 성적 너그러움/ 2. 성적 보통/ 3. 성적 깐깐함
    res = []
    
    try:
        score_rate = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[1]/div[1]/span[1]').text 
    except:  # 별점이 없는 경우 예외처리가 됨.
        return [-1]*6
    
    # 퍼센트로 이뤄진 강의평가
    try:
        for j in range(1,3+1):
            high_rate = [-1,-1]
            for i in range(1,3+1):
                homework_rate = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[{}]/div/div[{}]/div[2]'.format(j,i)).text        
                homework_rate = [int(homework_rate[:-1]), i]
                high_rate = max(high_rate, homework_rate)
            res.append(high_rate[1])
            
        attendance = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[4]/div/span').text
        test = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[5]/div/span').text
        
        res.append(attendance)
        res.append(test)
        res.append(score_rate)
        
        return res
    
        
    # 아니었다면 다른 방식으로 시도
    except:
        try:
            homework = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[1]/div[1]/span').text
            team = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[1]/div[2]/span').text
            grade = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[1]/div[3]/span').text
            attendance = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[2]/div/span[1]').text
            test = driver.find_element_by_xpath('/html/body/div/div/div[2]/div/section[2]/div[2]/div[3]/div/span').text
            res = [homework, team, grade, attendance, test, score_rate]
            
            return res
        
        except:     # 별점만 있고 세부적인 내용은 없는 경우 예외처리가 됨.
            return [-1]*6


df = pd.read_csv("2022년2학기.csv")
df['과제'] = -1
df['조모임'] = -1
df['성적'] = -1
df['출결'] = -1
df['시험'] = -1
df['평점'] = -1


eval_data = []

for i in range(df.shape[0]):
    eval_data.append(GetInfo(df.과목명[i], df.담당교수[i]))
    print(eval_data)
    driver.back()
    driver.back()
    time.sleep(1)
df[['과제','조모임','성적','출결','시험','평점']] = eval_data

df.to_csv("tteesstt.csv", index=False)
