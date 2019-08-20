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
import xforce_exchange_module_2 as xforce
import xforce_exchange_login_module as xforce_login

import pandas as pd
import openpyxl
from openpyxl import load_workbook

search = []

aguse_results = []
mxtoolbox_results = []
owner_IP_results = []
xforce_results_category = []
xforce_results_time = []
xforce_results_risk = []
xforce_results_IP = []

driver = webdriver.Chrome(r'C:\Users\user\Desktop\���q�������O���\mxtoolbox\chromedriver.exe') 

print("�ǂݍ��܂���t�@�C����I��")
target_file = input(">> ")
with open(target_file, encoding='utf-8') as f:

    for rows in f:
        row = rows.rstrip('\n\n')
        search.append(row)

for ip in search:
    #------aguse�̏���--------------------------------
    for roop in range(0,5):
        aguse_result = aguse.main_move(ip,driver)
        if aguse_result == "safe" or aguse_result == "caution":
            break
    aguse_results.append(aguse_result)
    print(aguse_results)
    
    #------mxtoolbox�̏���--------------------------------
    for roop in range(0,6):#���[�v��6�܂ł��闝�R�́Aaguse�̖W�Q������1���[�v���ʂɂ��邩������Ȃ�����
       mxtoolbox_result = mxtoolbox.main_move(ip,driver)
       if not mxtoolbox_result == None and int(mxtoolbox_result[1]) < 5:
           break
    mxtoolbox_results.append(mxtoolbox_result[0])
    print(mxtoolbox_results)
    
    #------owner�̏���--------------------------------
    for roop in range(0,5):
       owner_IP_result = ownerIP.main_move(ip,driver)
       if not owner_IP_result == None:
           break
    owner_IP_results.append(owner_IP_result)
    print(owner_IP_results)

xforce_login.login(driver)
for ip in search:
    for roop in range(0,5):
        xforce_result = xforce.main_move(ip, driver)
        if not xforce_result == None:
            break
    xforce_results_category.append(xforce_result[0][0])
    xforce_results_time.append(xforce_result[1][0])
    xforce_results_risk.append(xforce_result[2][0])
    xforce_results_IP.append(xforce_result[3][0])
    print(xforce_results_category)
    print(xforce_results_time)
    print(xforce_results_risk)
    print(xforce_results_IP)

#--------�ȉ����ʂ̏o��--------------------------------------------------------------------------------
#��������IP�A�h���X�ƑS���̌��ʂ��f�[�^�t���[���ɂ���
df_searchIP = pd.DataFrame(search, columns=["IP"])
df_aguse_results = pd.DataFrame(aguse_results, columns=["aguse"])
df_mxtoolbox_results = pd.DataFrame(mxtoolbox_results, columns=["mxtoolbox"])
df_owner_IP_results = pd.DataFrame(owner_IP_results, columns=["���L��"])

#�f�[�^�t���[���ɂ������ʂ�����
df_all_results_tmp = pd.concat([df_searchIP, df_aguse_results, df_mxtoolbox_results, df_owner_IP_results], axis=1)

df_all_results = df_all_results_tmp.set_index(['IP', 'aguse', 'mxtoolbox', '���L��'])

#--------xforce�̌��ʏo��------------------------------------------------
df_searchIP = pd.DataFrame(xforce_results_IP, columns=["IP"])
df_xforce_category = pd.DataFrame(xforce_results_category, columns=["�J�e�S���["])
df_xforce_time = pd.DataFrame(xforce_results_time, columns=["�^�C�����C��"])
df_xforce_risk = pd.DataFrame(xforce_results_risk, columns=["���X�N"])

df_xforce_all_results_tmp = pd.concat([df_searchIP, df_xforce_category, df_xforce_time, df_xforce_risk], axis=1)

df_xforce_all_results = df_xforce_all_results_tmp.set_index(["IP", "�J�e�S���[", "�^�C�����C��", "���X�N"])


#----------test.xlsx���J���āA���ʃV�[�g��xforce���ʃV�[�g�Ɍ��ʂ�ǋL-------------------------------------------
with pd.ExcelWriter(r'C:\Users\user\Desktop\���q�������O���\�ŏI�`\test.xlsx') as writer:
    writer.book = openpyxl.load_workbook(r'C:\Users\user\Desktop\���q�������O���\�ŏI�`\test.xlsx')
    df_all_results.to_excel(writer, sheet_name="����")
    df_xforce_all_results.to_excel(writer, sheet_name="xforce����")

print("����")
driver.close()