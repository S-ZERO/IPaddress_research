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
        #selenium�Ńu���b�N���X�g������ʂɈڍs
        driver.get('https://mxtoolbox.com/blacklists.aspx')
        sleep(1)

        #��������I��
        ib=driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_txtToolInput')

        #��������IP�A�h���X�����
        ib.send_keys(def_ip)
        sleep(1)

        #�����J�n�{�^������������
        driver.find_element_by_id('ctl00_ContentPlaceHolder1_ucToolhandler_btnAction').click()
        
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tool-result-body"))
        )
        
        def_source = driver.page_source
        if def_source == None:
            print("Web�y�[�W���擾�ł��܂���ł���")
            print("�A�N�Z�X���������ꂽ�\�������邽�߁A5���Ԓ�~���܂�")
            sleep(300)
            return "Web�ڑ�����"
            
        def_soup = BeautifulSoup(def_source, "html.parser")
        
        #�������ʉ�ʂ�html���A<div class=tool-result-body>~</div>�ň͂܂ꂽ���������X�g�^�Œ��o
        div_tool_result_body = def_soup.select('div.tool-result-body')
        
        strongs = div_tool_result_body[0].select('strong')
        strong = strongs[2].text
        timeout = strongs[3].text
        print("���X�g�F"+strong+"�@�^�C���A�E�g�F"+timeout)
        
        return strong ,timeout
        
    except TimeoutException:
        print("timeout")
    
    except UnexpectedAlertPresentException:
        print("mxtoolbox�̖W�Q")
        Alert(driver).accept()

    except NoSuchElementException:
        print("�v�f��������܂���")
        
    #except NoSuchElementException:
    #    print("Web�y�[�W���擾�ł��܂���ł���")
    #    print("�A�N�Z�X���������ꂽ�\�������邽�߁A5���Ԓ�~���܂�")
    #    sleep(300)
