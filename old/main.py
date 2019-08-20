# -*- coding: Shift-JIS -*

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

import aguse_reserach_module as aguse
import mxtoolbox_blacklist_module as mxtoolbox
import owner_search_IP_module as ownerIP

search = []

aguse_results = []
mxtoolbox_results = []
owner_IP_results = []

driver = webdriver.Chrome(r'C:\Users\user\Desktop\王子製紙ログ解析\mxtoolbox\chromedriver.exe') 

print("読み込ませるファイルを選択")
target_file = input(">> ")
with open(target_file, encoding='utf-8') as f:

    for rows in f:
        row = rows.rstrip('\n\n')
        search.append(row)

for ip in search:
    #------aguseの処理--------------------------------
    for roop in range(0,5):
        aguse_result = aguse.main_move(ip,driver)
        if not aguse_result == None:
            break
    aguse_results.append(aguse_result)
    print(aguse_results)
    
    #------mxtoolboxの処理--------------------------------
    for roop in range(0,5):
       mxtoolbox_result = mxtoolbox.main_move(ip,driver)
       if not mxtoolbox_result == None and mxtoolbox_result[1] <= 5:
           break
    mxtoolbox_results.append(mxtoolbox_result[0])
    print(mxtoolbox_results)
    
    #------ownerの処理--------------------------------
    for roop in range(0,5):
       owner_IP_result = owner.main_move(ip,driver)
       if not owner_IP_result == None:
           break
    owner_IP_results.append(owner_IP_result)
    print(owner_IP_results)
