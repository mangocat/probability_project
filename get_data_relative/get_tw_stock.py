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
count=0
for stock_code in stock_code_list:
	if count<419:
		count+=1
		continue
	# os.system("echo run "+str(count)+" : "+stock_code+" >> log")
	print("run "+stock_code)
	print(count)
	cmd="python3 get_a_year.py "+stock_code
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	process.communicate()
	# print process.returncode
	# os.system("echo end "+str(count)+" : "+stock_code+" >> log")
	print("end "+stock_code)
	count+=1