# -*- coding: Shift-JIS -*-

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


from time import sleep
import os, argparse, csv

from bs4 import BeautifulSoup

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from requests.exceptions import Timeout
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

from datetime import datetime

import pandas as pd
import openpyxl

def main_move(ip,driver):
    try: 
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "top_search"))
            )
        
        #検索欄を選択
        ib=driver.find_element_by_id('top_search')
        
        #検索欄にIPアドレスを入力
        ib.send_keys(ip)
        sleep(1)

        #検索開始ボタンを押下する
        driver.find_element_by_id('submitTopSearch').click()

       
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='timelineTable']/tbody/tr[1]/td[5]/span"))
        )
        

        #検索結果画面のhtmlを取得(検索結果画面のhtmlはdriver.page_sourceで取得可能)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        sleep(1)
        
        risk = driver.find_elements_by_xpath("//*[@id='searchresults']/div/div[1]/div[1]/div[2]")
        

        #検索結果画面のhtmlより、<div class=tool-result-body>~</div>で囲まれた部分をリスト型で抽出
        table_all = soup.select('ip-history')
        tbody = table_all[0].select('tbody')
        
        trs = tbody[0].select('tr')
        
        for tr in trs:
            tds = tr.select('td')
            span = tds[1].select('span')
            time = tds[4].text
            time_date = datetime.strptime(time,'%Y/%m/%d %H:%M')
            if datetime(2019,3,1)<= time_date <= datetime(2019,4,30):
                #span[0].textはカテゴリ本体の内容 span[1].textは%の値

                return span[0].text + span[1].text ,time ,risk[0].text,ip
                #tds[1]に取り消し線が入っていたらcategory_tmpにappendしないようにする
                #//*[@id="timelineTable"]/tbody/tr[2]/td[2]/ul/li/p/spanに「カテゴリーが削除されました」とか書いてるからそれでif文処理
            else:
                return "期間外" , " " ,risk[0].text,ip
                   
    except IndexError:
        return "no result" ,time ,risk[0].text,ip
                
    except TimeoutException:
        print("不明")
        
    finally:
        #入力欄の空白化
        searcher=driver.find_element_by_id('top_search')
        searcher.clear()
    