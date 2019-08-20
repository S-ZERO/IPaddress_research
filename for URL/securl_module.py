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

def main_move(def_url,driver):
    try:
        driver.get('https://securl.nu/')
        sleep(1)
        #��������I��
        ib=driver.find_element_by_xpath('//*[@id="top_url_entry"]')
        #��������IP�A�h���X�����
        ib.send_keys(def_url)
        sleep(1)
        
        #�����J�n�{�^������������
        driver.find_element_by_xpath('//*[@id="top_url_entry_go"]').click()
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captured_img"]'))
        )
        
        #�������ʉ�ʂ�html���擾(�������ʉ�ʂ�html��driver.page_source�Ŏ擾�\)
        def_source = driver.page_source
        if def_source == None:
            print("Web�y�[�W���擾�ł��܂���ł���")
            print("�A�N�Z�X���������ꂽ�\�������邽�߁A5���Ԓ�~���܂�")
            sleep(300)
            return "Web�ڑ�����"
            
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
    #    print("Web�y�[�W���擾�ł��܂���ł���")
    #    print("�A�N�Z�X���������ꂽ�\�������邽�߁A5���Ԓ�~���܂�")
    #    sleep(300)
