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
        
        #��������I��
        ib=driver.find_element_by_id('top_search')
        
        #��������IP�A�h���X�����
        ib.send_keys(ip)
        sleep(1)

        #�����J�n�{�^������������
        driver.find_element_by_id('submitTopSearch').click()

       
        WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='timelineTable']/tbody/tr[1]/td[5]/span"))
        )
        

        #�������ʉ�ʂ�html���擾(�������ʉ�ʂ�html��driver.page_source�Ŏ擾�\)
        source = driver.page_source
        soup = BeautifulSoup(source, "html.parser")
        sleep(1)
        
        risk = driver.find_elements_by_xpath("//*[@id='searchresults']/div/div[1]/div[1]/div[2]")
        

        #�������ʉ�ʂ�html���A<div class=tool-result-body>~</div>�ň͂܂ꂽ���������X�g�^�Œ��o
        table_all = soup.select('ip-history')
        tbody = table_all[0].select('tbody')
        
        trs = tbody[0].select('tr')
        
        for tr in trs:
            tds = tr.select('td')
            span = tds[1].select('span')
            time = tds[4].text
            time_date = datetime.strptime(time,'%Y/%m/%d %H:%M')
            if datetime(2019,3,1)<= time_date <= datetime(2019,4,30):
                #span[0].text�̓J�e�S���{�̂̓��e span[1].text��%�̒l

                return span[0].text + span[1].text ,time ,risk[0].text,ip
                #tds[1]�Ɏ��������������Ă�����category_tmp��append���Ȃ��悤�ɂ���
                #//*[@id="timelineTable"]/tbody/tr[2]/td[2]/ul/li/p/span�Ɂu�J�e�S���[���폜����܂����v�Ƃ������Ă邩�炻���if������
            else:
                return "���ԊO" , " " ,risk[0].text,ip
                   
    except IndexError:
        return "no result" ,time ,risk[0].text,ip
                
    except TimeoutException:
        print("�s��")
        
    finally:
        #���͗��̋󔒉�
        searcher=driver.find_element_by_id('top_search')
        searcher.clear()
    