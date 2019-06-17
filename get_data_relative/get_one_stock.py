import twstock
import pandas as pd
import csv
import time
import sys

print("start")
stock_code=sys.argv[1]
from_year=int(sys.argv[2])
from_month=int(sys.argv[3])
# print(type(fr))
total_day_num=0
stock_val=pd.DataFrame(twstock.Stock(stock_code,initial_fetch=False).fetch(from_year,from_month))

#計算總共的天數
total_day_num=len(stock_val.open)
print (total_day_num)
# 開啟要輸出的 CSV 檔案
output_file_name='data/stock_'+stock_code+'.csv'
with open(output_file_name, 'a', newline='') as csvfile:
	# 建立 CSV 檔寫入器
	writer = csv.writer(csvfile)

	for date,val in zip(stock_val.date,stock_val.open):
		writer.writerow([date,val])
	


