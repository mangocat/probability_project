# Python code for 1-D random walk.
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
param = {"days":300, "total_assets":1e8, "init_invest_ratio":0.01, "win_ratio":0.01, "lose_ratio":0.01, "buy_ratio":0.5}
# stock variety
stock_average = 48 # tw stock average

rate = 5 # raise/fall rate
budget = param["total_assets"]*param["init_invest_ratio"]

for times in range(n):
    stock_price = []
    positions = []
    stock_count = 0
    invested_money = 0
    while(invested_money < budget):
        cur_price = 2*stock_average*random.random()
        if(invested_money + 1000*cur_price < budget):
            stock_price.append(cur_price)
            # statically defining the starting position
            positions.append([cur_price])
            invested_money+=1000*cur_price
            stock_count+=1
        else:
            break

    remain_money = param["total_assets"] - invested_money
    # creating the random points
    rr = [] # random things
    for i in range(len(stock_price)):
        rr.append(np.random.random(param["days"]))
    for day in range(param["days"]):
        for i in range(len(stock_price)):
            positions[i].append(positions[i][-1] + rate*(rr[i][day]-0.5))
        # plotting down the graph of the random walk in 1D
        plt.plot(positions[i])

plt.show()
