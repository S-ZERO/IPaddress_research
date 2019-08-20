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
        driver.get('http://www.ip-adress.com')
        sleep(1)
        #��������I��
        ib=driver.find_element_by_xpath('/html/body/header/nav/span/form/input')
        #��������IP�A�h���X�����
        ib.send_keys(def_ip)
        sleep(1)
        
        #�����J�n�{�^������������
        driver.find_element_by_xpath('/html/body/header/nav/span/form/button').click()
        WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/main/table'))
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

        def_organization = driver.find_element_by_xpath('/html/body/main/table/tbody/tr[10]/td')
        
        return def_organization.text
    
    except TimeoutException:
        print("timeout")
        
    except NoSuchElementException:
        
        print("no data")
        return "no result"
        
    #except NoSuchElementException:
    #    print("Web�y�[�W���擾�ł��܂���ł���")
    #    print("�A�N�Z�X���������ꂽ�\�������邽�߁A5���Ԓ�~���܂�")
    #    sleep(300)
