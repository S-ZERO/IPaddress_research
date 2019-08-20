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

from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

def main_move(def_ip,driver):
    try:
        #seleniumでブラックリスト検索画面に移行
        driver.get('https://mxtoolbox.com/blacklists.aspx')
        sleep(1)

        #検索欄を選択
        ib=driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput')

        #検索欄にIPアドレスを入力
        ib.send_keys(def_ip)
        sleep(1)

        #検索開始ボタンを押下する
        driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_btnAction').click()
        
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tool-result-body"))
        )
        
        def_source = driver.page_source
        if def_source == None:
            print("Webページが取得できませんでした")
            print("アクセスが制限された可能性があるため、5分間停止します")
            sleep(300)
            return "Web接続制限"
            
        def_soup = BeautifulSoup(def_source, "html.parser")
        
        #検索結果画面のhtmlより、<div class=tool-result-body>~</div>で囲まれた部分をリスト型で抽出
        div_tool_result_body = def_soup.select('div.tool-result-body')
        
        strongs = div_tool_result_body[0].select('strong')
        strong = strongs[2].text
        timeout = strongs[3].text
        print("リスト："+strong+"　タイムアウト："+timeout)
        
        return strong ,timeout
        
    except TimeoutException:
        print("timeout")
    
    except UnexpectedAlertPresentException:
        print("mxtoolboxの妨害")
        Alert(driver).accept()

    except NoSuchElementException:
        print("要素が見つかりません")
        
    #except NoSuchElementException:
    #    print("Webページが取得できませんでした")
    #    print("アクセスが制限された可能性があるため、5分間停止します")
    #    sleep(300)
