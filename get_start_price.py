# 獲取所有股票初始資料並建立csv檔，以及算出股價整體趨勢
import csv
import time
import sys
import subprocess
import os
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# 這幾個股票沒有一整年的資訊
lost_data_list=[604,711,832,835]

# 得到股票代碼和名稱的list
stock_code_list=[]
stock_name_list=[]
with open('get_data_relative/上市公司資訊.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)
    for row in rows:
        stock_code_list.append(row[0])
        stock_name_list.append(row[1])

#把起始的空元素和沒有資料的股票刪掉 
del stock_code_list[0]
del stock_name_list[0]
for i in range(len(lost_data_list)):
    del stock_code_list[lost_data_list[i]-i]
    del stock_name_list[lost_data_list[i]-i]
# print(stock_code_list[604])
# print("6669" in stock_code_list)
total_stock_num=len(stock_code_list)

stock_start_price=[]
start_total=0
final_total=0
win_list=[]
win_list_val=[]
for stock_code in stock_code_list:
	with open('get_data_relative/data/stock_'+stock_code+'.csv', 'r') as f:
		reader = csv.reader(f)
		rows = list(reader)
		nan_num=0
		count=0
		start_end=[0,0]
		for row in rows:
			if row[1]=="nan":
				# print("nan")
				nan_num+=1
			else:
				if count==0:
					start_end[0]=float(row[1])
					start_total+=float(row[1])
				if count==200:
					start_end[1]=float(row[1])
					final_total+=float(row[1])
				count+=1
		stock_start_price.append([stock_code,rows[0][1],len(rows)-nan_num])
	if start_end[0]<start_end[1]:
		win_list.append(stock_code)
		win_list_val.append(start_end)
tf=0
ts=0
for u in win_list_val:
	ts+=u[0]
	tf+=u[1]
# 印出 win 的股票的趨勢
print("win ",tf/ts)

# 開啟要輸出的 CSV 檔案
output_file_name='start_price.csv'
with open(output_file_name, 'w', newline='') as csvfile:
	# 建立 CSV 檔寫入器
	writer = csv.writer(csvfile)

	for stock in stock_start_price:
		writer.writerow(stock)

# 印出所有股票的趨勢
print((final_total/start_total)-1)
