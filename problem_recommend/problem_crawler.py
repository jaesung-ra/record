from ctypes import create_unicode_buffer
from operator import truediv
import pymysql
from openpyxl import load_workbook
from ast import Pass
from bs4 import BeautifulSoup as bs
from urllib.request import HTTPError
import selenium
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
db=pymysql.connect(host='localhost',port=3306,user='root',passwd='0000',db='recodb',charset='utf8')
cursor=db.cursor()

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver=webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 10)

sql="select code,name,text,difficulty,id,group_concat(tag separator', ') as tag from problems group by code order by id ;"
url="https://www.codechef.com/submit/"
cursor.execute(sql)
result=cursor.fetchall()
for idx,res in enumerate(result):
    code=res[0]
    name=res[1]
    text=res[2].replace("'","''")
    difficulty=res[3]
    driver.get(url+code)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="vertical-tab-panel-0"]/span[1]')))
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, '#root > div > div._pageContainer_x1ji1_2 > div > div > div._problem-banner__container_bvg0e_387 > div._navigate-button__container_bvg0e_450 > div._navigation-left-wrapper_bvg0e_459 > div._expand__container_bvg0e_525 > span > svg').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div')))
    html=driver.page_source
    soup=bs(html,'html.parser')
    tags=soup.find_all('div','_tag-list__item_bvg0e_795')
    
    for tag in tags:
        tagg=tag.get_text().replace("'","''")
        sql=f"INSERT INTO tmp (code,name,text,difficulty,tag) VALUES ('{code}','{name}','{text}',{difficulty},'{tagg}')"
        cursor.execute(sql)
        #sql=f"INSERT INTO tmp VALUES (code,name,text,difficulty,tag) values (%s,%s,%s,%s,%s)"
        #cursor.execute(sql,(code,name,text,difficulty,tag.get_text()))
        
db.commit()
db.close()
