import numpy as np
import pandas as pd
import csv

import xlrd
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
#드라이버 초기화
from selenium.webdriver.common.by import By

s = Service('~/Documents/chromedriver')
SCROLL_PAUSE_TIME = 0.5

driver = webdriver.Chrome(service=s)

f = open('sentence.tsv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f, delimiter='\t')

label = ["sentence"]
wr.writerow(label)

base_url = "https://www.google.com/search?q="

agents = ['Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36', 
'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36',
'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17']
agent_num = 0


def get_certificate_keywords():
    wb = xlrd.open_workbook('keywords.xls')
    ws_1 = wb.sheet_by_index(0)
    ws_2 = wb.sheet_by_index(1)
    keyword2 = []
    result = []

    for i in range(ws_2.nrows):
        keyword2.append(ws_2.cell(i, 0).value)

    for i in range(ws_1.nrows):
        keyword_main = ws_1.cell(i, 0).value

        for j in keyword2:
            result.append(keyword_main + ' ' + j)
    
    return result


def change_agent():
    options = Options()
    global agent_num, agents, driver
    agent_num = (agent_num + 1) % len(agents)
    options.add_argument(f'user-agent=' + agents[agent_num])

    driver.quit()
    driver = webdriver.Chrome(chrome_options=options, service=s)


# 자격증 정보 크롤링
c_keywords = get_certificate_keywords()
for word in c_keywords:
    url = base_url + word
    driver.get(url)
    driver.implicitly_wait(2)

    html = driver.page_source
    soup = BeautifulSoup(html)

    v = soup.select('.yuRUbf')

    for page in range(1, 30):
        for i in v:
            print(i.select_one('.LC20lb.DKV0Md').text)
            print(i.a.attrs['href'])
            print()
        
        try:
            driver.find_element('id','pnnext').click()
        except:
            try:
                driver.find_element('class', 'nBDE1b G5eFlf').click()
            except:
                break
    change_agent()
        
        


#wr.writerow(["안녕"])

f.close()

dataset = pd.read_csv("train.tsv", delimiter='\t', header=None)
print(dataset)
