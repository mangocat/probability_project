# 檢查缺了哪些股票資料
import csv
import time
import sys
import subprocess
import os

# 股票代碼 
stock_code_list=[]

# 讀取csv檔
with open('上市公司資訊.csv', 'r') as f:
	reader = csv.reader(f)
	rows = list(reader)
	for row in rows:
		stock_code_list.append(row[0])
# 刪掉前兩行，是空白行
del stock_code_list[0]

# print process.returncode

stock_exist_list = []
with open('test_log', 'r') as f:
	reader = csv.reader(f)
	rows = list(reader)
	for row in rows:
		stock_exist_list.append(row[0])
# 刪掉前兩行，是空白行
del stock_exist_list[0]
# print(stock_exist_list)
count=0
for stock in stock_code_list:
	if ("stock_"+stock+".csv") not in stock_exist_list:
		print("loss index: "+str(count)+" id: "+stock)
	count+=1


