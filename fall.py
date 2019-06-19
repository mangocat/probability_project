import math
import random
import numpy as np
from datetime import datetime
# import matplotlib.pyplot as plt

random.seed(datetime.now())

def buy(remain_money, current_price, avg_price, current_stock_num, lose_ratio, buy_ratio):
	want_to_buy = math.ceil(((avg_price-current_price)/avg_price//lose_ratio)*buy_ratio*current_stock_num)
	can_buy = remain_money//(current_price*1000)
	if (want_to_buy <= can_buy):
		return want_to_buy
	# else
	return can_buy

def experiment(days, total_assets, init_invest_ratio, win_ratio, lose_ratio, buy_ratio):

	# times
	n = 1000

	stock_average = 48 # tw stock average
	
	fall_prob = 0.51
	rise_prob = 1 - fall_prob
	fall_rate = 0.1/fall_prob
	rise_rate = 0.1/rise_prob
	rate = 0.1/0.5 # rate

	budget = total_assets*init_invest_ratio
	final_assets = 0
	total_trend = 0
	avg_trend = 0
	for times in range(n):
		init_price_sum = 0
		final_price_sum = 0
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

		remain_money = total_assets - invested_money
		#remain_money_list.append(remain_money)
		# creating the random points
		rr = [] # random things
		for i in range(stock_count):
			rr.append(np.random.random(days))
		for day in range(days):
			for i in range(stock_count):
				if rr[i][day] > fall_rate: # rise
					current_price[i].append(current_price[i][-1]*(1+rise_rate*(rr[i][day]-fall_prob)))
				else: #fall
					current_price[i].append(current_price[i][-1]*(1+fall_rate*(rr[i][day]-fall_prob)))
				if current_price[i][-1] < 0:
					stock_num[i] = 0
					current_price[i][-1] = 0
				if stock_num[i]==0: # sold
					continue
				if (current_price[i][day]<stock_price[i]*(1-lose_ratio)):
					# buy
					buy_num = buy(remain_money, current_price[i][day], stock_price[i], stock_num[i], lose_ratio, buy_ratio)
					remain_money -= buy_num*current_price[i][day]*1000
					stock_price[i] = (stock_price[i]*stock_num[i] + buy_num*current_price[i][day])/(stock_num[i] + buy_num)
					stock_num[i] += buy_num
				elif (current_price[i][day]>stock_price[i]*(1+win_ratio)):
					# sell
					remain_money += current_price[i][day]*stock_num[i]*1000
					stock_num[i] = 0
			#remain_money_list.append(remain_money)

		for i in range(stock_count):
			# plot
			# plt.plot(current_price[i])
			# sell everything
			# calculate the total sum of initial price
			init_price_sum += current_price[i][1]
			final_price_sum += current_price[i][-1]
			# sell all the stock
			remain_money += current_price[i][-1]*stock_num[i]*1000
			stock_num[i] = 0
		total_trend += (final_price_sum/init_price_sum)-1
		#remain_money_list.append(remain_money)
		#plt.plot(remain_money_list)
		#plt.show()
		final_assets += remain_money
	final_assets /= float(n)
	final_assets /= 1e8
	final_assets -= 1
	avg_trend = total_trend/float(n)
	return (final_assets, avg_trend)

best_param = [-1000, 0, 0, 0, 0, 0]
#lose_ratio = 0.2
#buy_ratio = 3.0

count = 0
limit = 1
# print(experiment(300, 1e8, 0.001, 1, 0.2, 3.0))
for win_ratio in np.arange(0.1, 0.6, 0.1):
	round(win_ratio, 1)
	for lose_ratio in np.arange(0.1, 0.6, 0.1):
		round(lose_ratio, 1)
		for buy_ratio in np.arange(0.5, 5.5, 0.5):
			round(buy_ratio, 1)
			final_assets, avg_trend = experiment(300, 1e8, 0.001, win_ratio, lose_ratio, buy_ratio)
			win_wrt_trend = final_assets - avg_trend
			if win_wrt_trend > best_param[0]:
				best_param = [win_wrt_trend, final_assets, avg_trend, win_ratio, lose_ratio, buy_ratio]
#			count += 1
#			if count == limit:
#				break
#		if count == limit:
#		   break
#	if count == limit:
#		break

print("best param: ")
print("win with respect to trend: ", best_param[0])
print("final assets: ", best_param[1])
print("avg trend: ", best_param[2])
print("win ratio: ", best_param[3])
print("lose ratio: ", best_param[4])
print("buy ratio: ", best_param[5])
