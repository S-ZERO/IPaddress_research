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

#---ファイルパスを入れるためのリストを生成-------
file_path=[]

print("テスト：行を表示するファイルを入力")
target_file = input(">>")

#-----Pathlistは対象のログエクセルファイルのパス一覧ファイル-----------
#-----Pathlistを「\n」を区切り文字にリスト化したものをfile_pathとする
with open(target_file ,encoding="utf-8") as f:
    for row in f:
        row= str(row)
        path = row.rstrip("\n")
        path = row.split("\n")

for path in file_path:
    #この時点でエクセルファイルが開かれている
    wb=openpyxl.load_workbook(file_path)
    sheet = wb["全体"]
    for row in wb.active.rows:
        for cell in row:
            print(cell.value)
            
        num = 0
        for cell in wb.active.rows:
            if cell[num] == "SourceAddr":
                print(cell[num])
            num += 1