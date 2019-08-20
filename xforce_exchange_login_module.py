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

def login(driver):

    #seleniumでブラックリスト検索画面に移行
    driver.get('https://exchange.xforce.ibmcloud.com/')
    sleep(1)
       
    #IDとPWの入力----------------------------------------------------------------
    sleep(5)
    driver.find_element_by_id("termsCheckbox").click()
    sleep(1)
    login_button1 = driver.find_element_by_xpath("//*[@id='bootstrap-tisp-app']/body/div[1]/div/div/div[4]/div/button[2]")
    login_button1.click()

    sleep(5)

    try:
        login_button2 = driver.find_element_by_xpath("//*[@id='formColumn']/div/div/div/div/div[1]/div/div/div[2]/a")
        login_button2.click()
    except NoSuchElementException:
        pass

    WebDriverWait(driver,60).until(
    EC.presence_of_element_located((By.ID, "ibmid"))
    )

    driver.find_element_by_id("ibmid").send_keys("r-suzuki@ift-kk.co.jp")
    driver.find_element_by_class_name("ibm-btn-pri").click()


    WebDriverWait(driver,60).until(
    EC.presence_of_element_located((By.ID, "password"))
    )

    driver.find_element_by_id("password").send_keys("ArisIft3051")
    driver.find_element_by_class_name("ibm-btn-pri").click()

    WebDriverWait(driver,60).until(
    EC.invisibility_of_element_located((By.XPATH, "//*[@id='processing']/div/div/div/img"))
    )
    #----------------------------------------------------------------------------