import twstock
import pandas as pd
import csv


stock_code_list=[]
stock_stock_list=[]
with open('上市公司資訊.csv', 'r') as f:
	reader = csv.reader(f)
	rows = list(reader)
	for row in rows:
		stock_code_list.append(row[0])
# 刪掉前兩行
del stock_code_list[0]
del stock_code_list[0]

# print(stock_code_list)
for stock_code in stock_code_list:
	stock_stock_list.append(twstock.Stock(stock_code))
	test_pd=pd.DataFrame(stock_stock_list[0].fetch_from(2019,5))
	print(str(test_pd.close))
	break



















	
# sum_price=0
# count=0
# average_price=0
# highest=0
# lowest=100
# for key,one_stock in stock_info_list.items():
# 	print(count)
# 	realtime_info=twstock.realtime.get(stock_code)
# 	if not ('realtime' in realtime_info):
# 		continue
# 	price_str=twstock.realtime.get(stock_code)['realtime']['open']
# 	if price_str is None:
# 		continue
# 	price=float(price_str)
# 	sum_price+=price
# 	if price>highest:
# 		highest=price
# 	if price<lowest:
# 		lowest=price
# 	count+=1
# average_price=sum_price/count

# print ("sum: "+str(sum_price))
# print ("average_price: "+str(average_price))
# print ("highest: "+str(highest))
# print ("lowest: "+str(lowest))

