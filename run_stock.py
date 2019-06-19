# 跑真實股票資料的script
# 輸出csv
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
import statistics

# 最後股價上漲的200支股票
win_list=['1102', '1103', '1109', '1110', '1203', '1216', '1218', '1219', '1231', '1232', '1233', '1310', '1315', '1323', '1402', '1409', '1410', '1417', '1434', '1438', '1443', '1446', '1451', '1468', '1472', '1477', '1503', '1507', '1515', '1529', '1532', '1533', '1537', '1539', '1540', '1558', '1582', '1604', '1614', '1617', '1712', '1713', '1718', '1722', '1730', '1733', '1736', '1737', '1762', '1773', '1786', '1808', '1902', '1904', '2002', '2007', '2012', '2014', '2022', '2027', '2101', '2104', '2107', '2108', '2207', '2208', '2228', '2301', '2302', '2308', '2312', '2316', '2321', '2323', '2328', '2329', '2330', '2332', '2338', '2345', '2348', '2349', '2351', '2355', '2356', '2362', '2363', '2368', '2371', '2373', '2375', '2379', '2382', '2383', '2387', '2390', '2395', '2397', '2404', '2413', '2415', '2421', '2423', '2424', '2425', '2426', '2428', '2439', '2442', '2458', '2462', '2467', '2478', '2480', '2486', '2488', '2491', '2492', '2493', '2501', '2514', '2515', '2516', '2524', '2530', '2538', '2542', '2546', '2547', '2548', '2597', '2601', '2607', '2612', '2613', '2617', '2633', '2636', '2637', '2702', '2712', '2748', '2801', '2812', '2816', '2834', '2836', '2838', '2845', '2850', '2852', '2880', '2884', '2885', '2886', '2892', '2904', '2910', '2912', '2913', '2915', '2923', '2936', '3004', '3005', '3008', '3016', '3017', '3022', '3023', '3025', '3029', '3034', '3037', '3038', '3043', '3047', '3049', '3051', '3054', '3266', '3296', '3312', '3338', '3356', '3376', '3416', '3432', '3454', '3501', '3504', '3533', '3535', '3557', '3583', '3596', '3622', '3653', '3694', '3698', '3701', '3703', '3704', '3705', '4119', '4137', '4142', '4190', '4426', '4438', '4536', '4725', '4763', '4764', '4906', '4927', '4942', '4958', '4960', '4977', '4994', '4999', '5203', '5215', '5225', '5234', '5269', '5288', '5469', '5519', '5522', '5525', '5533', '5607', '5608', '5871', '5880', '5906', '5907', '6108', '6142', '6155', '6172', '6176', '6183', '6189', '6191', '6192', '6201', '6202', '6209', '6213', '6214', '6230', '6251', '6269', '6278', '6281', '6282', '6285', '6409', '6431', '6442', '6552', '6582', '8011', '8016', '8021', '8028', '8046', '8072', '8081', '8101', '8131', '8150', '8163', '8210', '8213', '8215', '8261', '8341', '8427', '8442', '8463', '8467', '8481', '8497', '8499', '8996', '9136', '9904', '9907', '9908', '9910', '9911', '9914', '9918', '9921', '9924', '9926', '9929', '9931', '9935', '9937', '9943', '9945', '9958']


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

total_stock_num=len(stock_code_list)

stock_start_price_dict={}
with open('start_price.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)
    for row in rows:
        if int(row[2])<250:
            stock_start_price_dict[row[0]]=-1   
        else:
            stock_start_price_dict[row[0]]=float(row[1])


random.seed(datetime.now())

def buy(remain_money, current_price, avg_price, current_stock_num, lose_ratio, buy_ratio):
    want_to_buy = math.ceil(((avg_price-current_price)/avg_price//lose_ratio)*buy_ratio*current_stock_num)
    can_buy = remain_money//(current_price*1000)
    if (want_to_buy <= can_buy):
        return want_to_buy
    # else
    return can_buy

def experiment(n,days, total_assets, init_invest_ratio, win_ratio, lose_ratio, buy_ratio,type_win):
    # type_win =True的話使用整體股票趨勢1.2的股票組合，反之使用全部股票組合
    # n --> 跑的次數

    param = {"days":days, "total_assets":total_assets, "init_invest_ratio":init_invest_ratio, "win_ratio":win_ratio, "lose_ratio":lose_ratio, "buy_ratio":buy_ratio}
    # stock variety
    stock_average = 48 # tw stock average

    rate = 0.1/0.5 # rate
    budget = param["total_assets"]*param["init_invest_ratio"]
    final_assets = 0

    for times in range(n):
        remain_money_list = []
        stock_buy_dict = {}
        current_price = []
        stock_count = 0
        invested_money = 0
        while(invested_money < budget):
            if type_win is False:
                stock_to_buy_index=random.randint(0,total_stock_num-1)
                stock_to_buy_code=stock_code_list[stock_to_buy_index]
            else:
                stock_to_buy_code=win_list[random.randint(0,len(win_list)-1)]
            cur_price = stock_start_price_dict[stock_to_buy_code]
            if cur_price < 0:
                continue
            if(invested_money + 1000*cur_price < budget):
                if stock_to_buy_code in stock_buy_dict.keys():
                    stock_buy_dict[stock_to_buy_code][1]+=1
                else:
                    stock_buy_dict[stock_to_buy_code]=[cur_price,1]
                    stock_count+=1
                # statically defining the starting position
                invested_money+=1000*cur_price
            else:
                break
        remain_money = param["total_assets"] - invested_money
        # creating the random points
        remain_money_list.append(remain_money)
        # get all stock
        stock_price_all={}
        # 讀取股票初始價格檔案
        for stock_code, price_num in stock_buy_dict.items():
            stock_price_list=[]
            with open('get_data_relative/data/stock_'+stock_code+'.csv', 'r') as f:
                reader = csv.reader(f)
                rows = list(reader)
                for row in rows:
                    try:
                        if not np.isnan(float(row[1])):
                            stock_price_list.append(float(row[1]))
                    except ValueError:
                        print ("Not a float ",row[1],"##")
                        
            stock_price_all[stock_code]=stock_price_list
        #開始跑200天
        everyday_trend=[]
        for day in range(param["days"]):
            current_price_total_aday=0
            for stock_code, price_num in stock_buy_dict.items():
                if price_num[1]==0:
                    continue
                
                current_price=stock_price_all[stock_code][day]
                current_price_total_aday+=current_price
                
                if (current_price<price_num[0]*(1-param["lose_ratio"])):
                    # buy
                    buy_num = buy(remain_money, current_price, price_num[0], price_num[1], param["lose_ratio"], param["buy_ratio"])
                    remain_money -= buy_num*current_price*1000
                    price_num[0] = (price_num[0]*price_num[1] + buy_num*current_price)/(price_num[1] + buy_num)
                    price_num[1] += buy_num
                elif (current_price>price_num[0]*(1+param["win_ratio"])):
                    # sell
                    remain_money += current_price*price_num[1]*1000
                    price_num[1] = 0

            remain_money_list.append(remain_money)
            # print(remain_money)
            everyday_trend.append(current_price_total_aday)
        # 出售所有股票
        for stock_code, price_num in stock_buy_dict.items():
            if price_num[1]==0:
                continue
            current_price=stock_price_all[stock_code][param["days"]]
            if np.isnan(current_price):
                print("process error")
                print(len(stock_price_all[stock_code]))
                print(stock_price_all[stock_code])
            remain_money += current_price*price_num[1]*1000
            price_num[1] = 0
        remain_money_list.append(remain_money)
        
        final_assets += remain_money
        # 底下可以印出剩下錢的圖表
        # plt.plot(remain_money_list)
        # plt.show()
    final_assets /= float(n)
    

    return final_assets
    # print(remain_money)
    
# 傳入參數，開始跑
print("avg: ",experiment(1000, 200, 1e9, 0.001, 0.3, 0.03, 0.5,True))


