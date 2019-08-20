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

#-----------def_mainのイメージとしてはaguseでのHTMLソースの取得を一回分----------------------------------------------------------
def main_move(def_ip,driver):
    try:
        #seleniumでブラックリスト検索画面に移行
        driver.get('https://www.aguse.jp/')
        sleep(1)
        #検索欄を選択
        id=driver.find_element_by_id('url')
        #searchからipアドレスを一つずつ検索欄に入力する
        id.send_keys(def_ip)
    
    
        #検索開始ボタンを押下する
        driver.find_element_by_class_name('btn1').click()
        
        #img[@alt!="indicator"]でalt属性がindicatorでない場合状態がDOM上に表示されたら次に進むようにできた
        WebDriverWait(driver, 60).until(lambda driver: 
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_wwwphishtankcom"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_codegooglecomphish"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_codegooglecomblack"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_bbarracudacentralorg"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_sbl-xblspamhausorg"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result__multisurblorg"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result___multisurblorg"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result____multisurblorg"]/img[@alt!="indicator"]'))(driver) and
            EC.presence_of_element_located((By.XPATH, '//*[@id="BL_result_cblabuseatorg"]/img[@alt!="indicator"]'))(driver)
            )

        def_source = driver.page_source
        if def_source == None:
            print("Webページが取得できませんでした")
            print("アクセスが制限された可能性があるため、5分間停止します")
            sleep(300)
            return "Web接続制限"
            
        def_soup = BeautifulSoup(def_source, "html.parser")
    
        #各々のブラリでsafeかcaution判定を一つずつ取得
        wwwphishtankcom = def_soup.select('div#BL_result_wwwphishtankcom')
        a = wwwphishtankcom[0].select('img')
        a_text = a[0].attrs['alt']
        print(a_text)
    
        codegooglecomphish = def_soup.select('div#BL_result_codegooglecomphish')
        b = codegooglecomphish[0].select('img')
        b_text = b[0].attrs['alt']
        print(b_text)

        codegooglecomblack = def_soup.select('div#BL_result_codegooglecomblack')
        c = codegooglecomblack[0].select('img')
        c_text = c[0].attrs['alt']
        print(c_text)

        bbarracudacentralorg = def_soup.select('div#BL_result_bbarracudacentralorg')
        d = bbarracudacentralorg[0].select('img')
        d_text = d[0].attrs['alt']
        print(d_text)
    
        sbl_xblspamhausorg = def_soup.select('div#BL_result_sbl-xblspamhausorg')
        e = sbl_xblspamhausorg[0].select('img')
        e_text = e[0].attrs['alt']
        print(e_text)
    
        multisurblorg = def_soup.select('div#BL_result__multisurblorg')
        f = multisurblorg[0].select('img')
        f_text = f[0].attrs['alt']
        print(f_text)
    
        ___multisurblorg = def_soup.select('div#BL_result___multisurblorg')
        g = ___multisurblorg[0].select('img')
        g_text = g[0].attrs['alt']
        print(g_text)

        ____multisurblorg = def_soup.select('div#BL_result____multisurblorg')
        h = ___multisurblorg[0].select('img')
        h_text = h[0].attrs['alt']
        print(h_text)

        cblabuseatorg = def_soup.select('div#BL_result_cblabuseatorg')
        i = cblabuseatorg[0].select('img')
        i_text = i[0].attrs['alt']
        print(i_text)
    
    
        if a==b==c==d==e==f==g==h==i:
            return "safe"
        else:
            return "caution"
        
    except UnexpectedAlertPresentException:
        try:
            print("dialog on")
            Alert(driver).accept()
            return "no result"
        except NoAlertPresentException:
            return "no result"

    except TimeoutException:
        print('no result')
        return "time out"
  
    #except NoSuchElementException:
    #    print("Webページが取得できませんでした")
    #    print("アクセスが制限された可能性があるため、5分間停止します")
    #    sleep(300)
