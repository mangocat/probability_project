# Python code for 1-D random walk.
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

random.seed(datetime.now())
# Probability to move up or down
prob = 0.5

def buy(remain_money, current_price, avg_price, current_stock_num, lose_ratio, buy_ratio):
    want_to_buy = math.ceil(((avg_price-current_price)/avg_price//lose_ratio)*buy_ratio*current_stock_num)
    can_buy = remain_money//(current_price*1000)
    if (want_to_buy <= can_buy):
        return want_to_buy
    # else
    return can_buy

def experiment(days, total_assets, init_invest_ratio, win_ratio, lose_ratio, buy_ratio):

    # times
    n = 10

    # parameters
    # 各參數range
    # 初始投資資金比: 1~30% 一次1%
    # 認賺%數: 1~50% 一次1%
    # 跌%價買進: 1~50% 一次1%
    # 跌價買進張數: 0.5~5 一次0.5
    param = {"days":days, "total_assets":total_assets, "init_invest_ratio":init_invest_ratio, "win_ratio":win_ratio, "lose_ratio":lose_ratio, "buy_ratio":buy_ratio}
    # stock variety
    stock_average = 48 # tw stock average

    rate = 0.1/0.5 # rate
    budget = param["total_assets"]*param["init_invest_ratio"]
    final_assets = 0

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
                current_price[i].append(current_price[i][-1]*(1+rate*(rr[i][day]-0.5)))
                if current_price[i][-1] < 0:
                    stock_num[i] = 0
                    current_price[i][-1] = 0;
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
            # remain_money_list.append(remain_money)
            # print(remain_money)

        for i in range(stock_count):
            # sell everything
            remain_money += current_price[i][-1]*stock_num[i]*1000
            stock_num[i] = 0
            # plotting down the graph of the random walk in 1D
            # plt.plot(current_price[i])
        # remain_money_list.append(remain_money)
        # print(remain_money/param["total_assets"])
        final_assets += remain_money
    final_assets /= float(n)
    # plt.show()
    return final_assets
    # print(remain_money)
    # plt.plot(remain_money_list)

# parameters
# 各參數range
# 初始投資資金比: 1~30% 一次1%
# 認賺%數: 1~50% 一次1%
# 跌%價買進: 1~50% 一次1%
# 跌價買進張數: 0.5~5 一次0.5
param_to_assets = []
best_param = [0, 0, 0, 0, 0]
for init_invest_ratio in np.arange(0.01, 0.31, 0.03):
    round(init_invest_ratio, 2)
    for win_ratio in np.arange(0.01, 0.51, 0.025):
        round(win_ratio, 3)
        for lose_ratio in np.arange(0.01, 0.51, 0.025):
            round(lose_ratio, 3)
            for buy_ratio in np.arange(0.5, 5.5, 0.5):
                round(buy_ratio, 1)
                final_assets = experiment(300, 1e8, init_invest_ratio, win_ratio, lose_ratio, buy_ratio)
                param_to_assets.append([final_assets, init_invest_ratio, win_ratio, lose_ratio, buy_ratio])
                # print(param_to_assets[-1])
                if final_assets > best_param[0]:
                    best_param = param_to_assets[-1]

print("best param : ", best_param)

