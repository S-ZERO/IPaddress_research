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

def main_move(def_url,driver):
    try:
        driver.get('https://securl.nu/')
        sleep(1)
        #検索欄を選択
        ib=driver.find_element_by_xpath('//*[@id="top_url_entry"]')
        #検索欄にIPアドレスを入力
        ib.send_keys(def_url)
        sleep(1)
        
        #検索開始ボタンを押下する
        driver.find_element_by_xpath('//*[@id="top_url_entry_go"]').click()
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captured_img"]'))
        )
        
        #検索結果画面のhtmlを取得(検索結果画面のhtmlはdriver.page_sourceで取得可能)
        def_source = driver.page_source
        if def_source == None:
            print("Webページが取得できませんでした")
            print("アクセスが制限された可能性があるため、5分間停止します")
            sleep(300)
            return "Web接続制限"
            
        def_soup = BeautifulSoup(def_source, "html.parser")
        sleep(1)

        def_page_title = driver.find_element_by_xpath('//*[@id="result_title"]')
        
        return def_page_title.text
    
    except TimeoutException:
        print("timeout")
        
    except NoSuchElementException:
        print("no data")
        return "no result"
        
    #except NoSuchElementException:
    #    print("Webページが取得できませんでした")
    #    print("アクセスが制限された可能性があるため、5分間停止します")
    #    sleep(300)
