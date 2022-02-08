# *********** 필 독 ***********
# 1. 크롬 드라이버를 설치해주세요. <참고 https://chromedriver.chromium.org/downloads>
# 1.1 크롬 드라이버 버전을 확인하고 싶다면 크롬 주소창에 chrome://version를 입력해
# 주신 뒤 제일 상단에 숫자를 확인하시면 됩니다.
# 2. 설치한 chromedriver.exe를 파일에 함께 넣어주신 뒤 실행해주세요.
#
#
#
#
# *********** 오 류 ***********
# 1. 프로그램이 실행되지 않을 경우
# https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=govlaos3444&logNo=221421842360
# 를 참고해주세요.
#
# 해킹 프로그램이 절대 아니므로 안심하셔도 됩니다.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import re


# driver 작업
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.set_window_position(0, 0)
driver.set_window_size(700, 1000)

# 콘솔 작업
COLLEGE = "서울과기대"
VERSION = "2.0.0"
print("=" * 60)
print(COLLEGE + "LMS 강의 매크로(" + VERSION + ") made by K.J.H")
print("=" * 60)

# XPATH, URL, 전역 변수
LOGINURL = 'https://eclass.seoultech.ac.kr/ilos/main/member/login_form.acl'
LOGINBUTTON = '//*[@id="myform"]/div/div/div/fieldset/input[3]'
# 대학교마다 강의 시간 표기 방법이 다름

global currentSubNum
currentSubNum = 0
global subNum
subNum = 0
global lectureBuffer
lectureBuffer = []  # lecture number를 받는 버퍼
global completeLectureNum
completeLectureNum = 0


# 로그인
def Login():
    while True:
        id = input("아이디 : ")
        pw = input("비밀번호 : ")

        while True:
            try:
                inputSubNum = input("LMS 전체 수강 과목 수(숫자) : ")
                subNum = int(inputSubNum) + 1
                break
            except:
                print("plz enter only numbers")

        driver.get(LOGINURL)
        driver.find_element(By.NAME, 'usr_id').send_keys(id)
        driver.find_element(By.NAME, 'usr_pwd').send_keys(pw)
        driver.find_element(By.XPATH, LOGINBUTTON).click()

        # id,pw가 틀렸을 시 다시 url 들어가면 오류가 뜸
        try:
            driver.get(LOGINURL)
            return subNum
        except:
            print("id or pw is incorrect")


# 과목 진입
def EnterSub(currentSubNum):
    subjectName = ""
    try:
        sleep(2)
        driver.get(LOGINURL)
        subjectName = driver.find_element(By.XPATH, '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[' + str(
            currentSubNum) + ']/em').text
        driver.find_element(By.XPATH,
                            '//*[@id="contentsIndex"]/div[2]/div[2]/ol/li[' + str(currentSubNum) + ']/em').click()
        driver.find_element(By.XPATH, '//*[@id="menu_lecture_weeks"]').click()
    except:
        print("error : 과목 진입 실패")

    print()
    print(subjectName + "과목에 진입하였습니다.")
    #*numbers(for admin) : " + str(currentSubNum)
    print()


# *차 찾기(lecture)
def SearchLectureNum():
    count = 0
    while True:
        for i in lectureBuffer:
            if i == count:
                count += 1
                #print("같아부러" + str(count))
            #else:
            #print("달라부러" + str(count))
        try:
            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                count) + '"]/div/ul/li[1]/ol/li[5]/div/div/div[2]/div[3]')
            #print(str(count))
            return count
        except:
            count += 1
            print("...")

    if True:
        print("error : SearchLectureNum loof escape")


# **차 찾기
def SearchSubLectureNum(lectureNum):
    count = 10
    while True:

        try:
            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                lectureNum) + '"]/div/ul/li[1]/ol/li[5]/div/div[' + str(count) + ']/div[2]/div[3]')
            #print(str(count) + "차시")
            return count
        except:
            count -= 1

        if count <= 0:
            print("error : **차 search error")
            break


# 시, 분, 초
def hms(str, s):
    hours = s // 3600
    s = s - hours * 3600
    mu = s // 60
    ss = s - mu * 60
    print(str, hours, '시간', mu, '분', ss, '초')


# 강의 시간 계산
def lectureTimeCalculate(subLectureNum, lectureNum):
    search = "분"

    lectureTimeText = driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
        lectureNum) + '"]/div/ul/li[1]/ol/li[5]/div/div[' + str(subLectureNum) + ']/div[2]/div[3]').text
    lectureTimeTextSplit = lectureTimeText.split('/')

    # 뒤
    lectureTimeBack = re.findall(r'\d+', lectureTimeTextSplit[1])  # 정해진 강의 시간
    size = len(lectureTimeBack)
    if size == 3:
        lectureTimeBackInt = int(lectureTimeBack[0]) * 360 + int(lectureTimeBack[1]) * 60 + int(
            lectureTimeBack[2])
    elif size == 2:
        lectureTimeBackInt = int(lectureTimeBack[0]) * 60 + int(lectureTimeBack[1])
    elif size == 1:
        if search in lectureTimeTextSplit[1]: ###############################################오류
            lectureTimeBackInt = int(lectureTimeBack[0]) * 60
        else:
            lectureTimeBackInt = int(lectureTimeBack[0])
    hms("강의 시간 : ", lectureTimeBackInt)

    # 앞
    lectureTimeFront = re.findall(r'\d+', lectureTimeTextSplit[0])  # 듣고 있는 강의 시간
    size = len(lectureTimeFront)
    if size == 3:
        lectureTimeFrontInt = int(lectureTimeFront[0]) * 360 + int(lectureTimeFront[1]) * 60 + int(
            lectureTimeFront[2])
    elif size == 2:
        lectureTimeFrontInt = int(lectureTimeFront[0]) * 60 + int(lectureTimeFront[1])
    elif size == 1:
        if search in lectureTimeTextSplit[0]:
            lectureTimeFrontInt = int(lectureTimeFront[0]) * 60
        else:
            lectureTimeFrontInt = int(lectureTimeFront[0])
    hms("내가 듣고 있는 시간 : ", lectureTimeFrontInt)

    if lectureTimeBackInt > lectureTimeFrontInt:
        runningTime = lectureTimeBackInt - lectureTimeFrontInt
        hms("남은 강의 시간 : ", runningTime)
        return runningTime
    else:
        #print("들은 강의, 강의시간 오류")
        return False


# 강의 진행
def RunLecture(subLectureNum, lectureNum):
    runningTime = lectureTimeCalculate(subLectureNum, lectureNum)

    if runningTime:
        try:
            driver.find_element(By.XPATH, '//*[@id="lecture-' + str(
                lectureNum) + '"]/div/ul/li[1]/ol/li[5]/div/div[' + str(subLectureNum) + ']/div[1]/div/span').click()
            sleep(3)
            driver.find_element(By.XPATH, '/html/body').click()
            driver.find_element(By.XPATH, '/html/body').send_keys(Keys.SPACE)
            print("\n<강의 재생>\n")

            sec = runningTime + 5
            while (sec != 0):
                sec = sec - 1
                sleep(1)
                hms("남은 시간 : ", sec)

            driver.find_element(By.XPATH, '//*[@id="close_"]').click()  # 출석 종료 버튼
            print("\n<강의 종료>\n")
            sleep(5)
            driver.back()
            sleep(2)
            driver.forward()
            sleep(2)
        except:
            print("\nwarning : 학습 기간이 아니거나 오류가 발생했습니다.")
            return False, runningTime

    #print("RunLecture : lectureNum 보내기 성공")
    return int(lectureNum), runningTime


currentSubNum = 2
subNum = Login()
sleep(1)

# 과목 전체 루프
while True:
    EnterSub(currentSubNum)
    currentSubNum += 1

    # *주차 확인 루프 진입
    allWeekElement = driver.find_elements(By.CSS_SELECTOR, '#chart > div > div')  # *주 박스 나누기
    for weekElement in allWeekElement:
        completeLectureNum = 0  # 완료된 lecture 번호
        lectureNum = 0  # lecture 번호
        subLectureNum = 0  # sub lecture 번호 (차시)
        #lectureBuffer = [0 for i in range(100)]
        lectureBuffer.clear()
        weekElementNumText = weekElement.find_element(By.CLASS_NAME, "wb-week").text
        weekElementProgText = weekElement.find_element(By.CLASS_NAME, "wb-status").text
        weekElementProgTextSplit = weekElementProgText.split('/')
        check = int(weekElementProgTextSplit[1]) - int(weekElementProgTextSplit[0])  # 1/3 같이 주차 밑에 있는 숫자 확인
        #print(weekElementNumText)
        #print(weekElementProgText)

        # *주 존재여부 확인 and 1/3와 같이 듣지 않은 강의가 있는지 확인  -> 없을 시 다음 주차로 넘어감
        if weekElementNumText != '' and check != 0:

            count = 0
            loofcheck = 0 #RunLecture()함수의 2번째 반환값.
            # 한 주차 루프
            while True:
                count += 1
                lastTime = 0
                try:
                    weekElement.find_element(By.TAG_NAME, "span").click()
                except:
                    pass
                    #print("error : *주차 버튼이 클릭 되지 않음")

                lectureNum = SearchLectureNum()
                print()
                subLectureNum = SearchSubLectureNum(lectureNum)
                print()
                # print("lectureNum : " + str(lectureNum))
                # print("subLectureNum : " + str(subLectureNum))

                if subLectureNum == 1:
                    completeLectureNum, loofcheck = RunLecture(1, lectureNum)
                    if completeLectureNum == False:
                        break
                elif subLectureNum == 2:
                    completeLectureNum, loofcheck = RunLecture(1, lectureNum)
                    completeLectureNum, loofcheck = RunLecture(2, lectureNum)
                    if completeLectureNum == False:
                        break
                elif subLectureNum == 3:
                    completeLectureNum, loofcheck = RunLecture(1, lectureNum)
                    completeLectureNum, loofcheck = RunLecture(2, lectureNum)
                    completeLectureNum, loofcheck= RunLecture(3, lectureNum)
                    if completeLectureNum == False:
                        break
                elif subLectureNum == 4:
                    completeLectureNum, loofcheck = RunLecture(1, lectureNum)
                    completeLectureNum, loofcheck = RunLecture(2, lectureNum)
                    completeLectureNum, loofcheck = RunLecture(3, lectureNum)
                    completeLectureNum, loofcheck = RunLecture(4, lectureNum)
                    if completeLectureNum == False:
                        break

                # 버퍼에 값넣기
                lectureBuffer.append(completeLectureNum)
                #for i in lectureBuffer:
                #    print(i)

                # loofcheck이 true라는 것은 lectureNum에 runningtime이 있는거고 false는 lectureNum에 runningtime이 없는거임.
                # 즉 loofcheck이 false면 다른 남은 강의를 찾아야한다는 것임. 루프를 한번 더 돌게 해야함
                if loofcheck == False:
                    if count == 0:
                        count = 0
                    else:
                        count -= 1

                # loofcheck에 runningtime이 있다는 것은 강의를 Run했다는 것이고 count를 활용해 남은 강의가 있는지 없는지 확인을 해야함.
                if count == check and loofcheck != False:
                    print(weekElementNumText + "차 종료")
                    break


        #else:
        #print("다음 주차 진입")

    # 과목 수 초과 시 프로그램 종료
    if currentSubNum > subNum:
        print("프로그램 종료")
        driver.close()
        break
