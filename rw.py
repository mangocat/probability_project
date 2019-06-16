# Python code for 1-D random walk.
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

random.seed(datetime.now())
# Probability to move up or down
prob = 0.5

# times
n = 1
# parameters
# 各參數range
# 初始投資資金比: 1~30% 一次1%
# 認賺%數: 1~50% 一次1%
# 跌%價買進: 1~50% 一次1%
# 跌價買進張數: 0.5~5 一次0.5
param = {"days":300, "total_assets":1e8, "init_invest_ratio":0.01, "win_ratio":0.01, "lose_ratio":0.01, "buy_ratio":0.5}
# stock variety
stock_average = 48 # tw stock average

rate = 5 # raise/fall rate
budget = param["total_assets"]*param["init_invest_ratio"]

def buy(remain_money, current_price, avg_price, current_stock_num, lose_ratio, buy_ratio):
    want_to_buy = math.ceil(((avg_price-current_price)/avg_price//lose_ratio)*buy_ratio*current_stock_num)
    can_buy = remain_money//(current_price*1000)
    if (want_to_buy <= can_buy):
        return want_to_buy
    # else
    return can_buy


for times in range(n):
    remain_money_list = []
    stock_price = []
    stock_num = []
    current_price = []
    stock_count = 0
    invested_money = 0
    while(invested_money < budget):
        cur_price = 2*stock_average*random.random()
        if(invested_money + 1000*cur_price < budget):
            stock_price.append(cur_price)
            stock_num.append(1)
            # statically defining the starting position
            current_price.append([cur_price])
            invested_money+=1000*cur_price
            stock_count+=1
        else:
            break

    remain_money = param["total_assets"] - invested_money
    # creating the random points
    rr = [] # random things
    for i in range(stock_count):
        rr.append(np.random.random(param["days"]))
    for day in range(param["days"]):
        for i in range(stock_count):
            if stock_num[i]==0: # sold
                continue
            current_price[i].append(current_price[i][-1] + rate*(rr[i][day]-0.5))
            if (current_price[i][day]<stock_price[i]*(1-param["lose_ratio"])):
                # buy
                buy_num = buy(remain_money, current_price[i][day], stock_price[i], stock_num[i], param["lose_ratio"], param["buy_ratio"])
                remain_money -= buy_num*current_price[i][day]*1000
                stock_price[i] = (stock_price[i]*stock_num[i] + buy_num*current_price[i][day])/(stock_num[i] + buy_num)
                stock_num[i] += buy_num
            elif (current_price[i][day]>stock_price[i]*(1+param["win_ratio"])):
                # sell
                remain_money += current_price[i][day]*stock_num[i]*1000
                stock_num[i] = 0
        remain_money_list.append(remain_money)
        print(remain_money)

    for i in range(stock_count):
        # sell everything
        remain_money += current_price[i][-1]*stock_num[i]*1000
        stock_num[i] = 0
        # plotting down the graph of the random walk in 1D
        # plt.plot(current_price[i])

plt.plot(remain_money_list)
plt.show()
