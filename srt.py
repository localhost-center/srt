import os
import sys
import datetime
from time import sleep
from random import randint
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
def open_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # https://chromedriver.chromium.org/downloads 요기서 자신의 크롬 버전과 같은 걸 다운로드 받아서 밑에 경로 입력
    driver = webdriver.Chrome("/Users/localhost/Documents/chromedriver", chrome_options=options)
    return driver
def run():
    driver = open_browser()
    driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
    driver.implicitly_wait(15)
    driver.find_element_by_id('srchDvNm01').send_keys("") #아이디
    driver.find_element_by_id('hmpgPwdCphd01').send_keys("") #비번
    driver.find_element_by_xpath('//*[@id="login-form"]/fieldset/div[1]/div[1]/div[2]/div/div[2]/input').click()
    driver.implicitly_wait(4)
    sleep(4)
    driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[1]/select').click()
    driver.implicitly_wait(1)
    dptRsStnCd = Select(driver.find_element_by_id('dptRsStnCd'))
    dptRsStnCd.select_by_visible_text(dpt)
    sleep(0.4)
    driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[2]/select').click()
    driver.implicitly_wait(1)
    arvRsStnCd = Select(driver.find_element_by_id('arvRsStnCd'))
    arvRsStnCd.select_by_visible_text(avl)
    date_ele = driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[3]/div/input[1]')
    driver.execute_script("arguments[0].setAttribute('value','{}')".format(dpt_date), date_ele)
    driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/div[4]/select').click()
    dptTm = Select(driver.find_element_by_id('dptTm'))
    dptTm.select_by_visible_text(when)
    sleep(0.4)
    driver.find_element_by_xpath('//*[@id="search-form"]/fieldset/a').click()
    driver.implicitly_wait(2)
    sleep(0.4)
    counter = 1
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        trlist = soup.select('#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr')  # [tr,tr,tr,....]
        index=0
        done=False
        for tdl in trlist:
            if done == False:
                index += 1
                for train_no in train_nums:
                    if tdl.select('.trnNo')[0].text.strip() == str(train_no):
                        if '예약하기' in tdl.select("td")[6].find_all(text='예약하기'):
                            t = "#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child("+str(index)+") > td:nth-child(7) > a"
                            driver.find_element_by_css_selector(t).click()
                            print("예약완료------------------------------------------------------------")
                            done=True
                            # sleep(5)
                            # break
                        else:
                            sleep(0.3)
            else:
                break
        print("loop done. counter : {}".format(counter))
        sleep(1)
        if done == False:
            elm = driver.find_element_by_xpath('//*[@id="search_top_tag"]/input')
            driver.execute_script("arguments[0].click();", elm)
            driver.implicitly_wait(2)
            counter += 1
        else:
            # driver.quit()
            break
        if counter > 1000:
            driver.quit()
            break
if __name__ == "__main__":
    dpt = input("출발지 입력 (ex 동탄, 울산, 동대구, 수서, 천안아산) : ")
    avl = input("도착지 입력 (ex 동탄, 울산, 동대구, 수서, 천안아산) : ")
    dpt_date = input("날짜 입력. 반드시 2021.04.30 형태 : ")
    when = input("18시 이후와 같이 입력  : ")
    train_nums = list(map(int,input("기차 번호 입력 스페이스바로 구분 : ").strip().split()))
    run()