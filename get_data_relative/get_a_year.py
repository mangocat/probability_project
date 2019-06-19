import time
import sys
import subprocess

stock_code=sys.argv[1]
# 要抓的日期
get_date=[[2018,5],[2018,6],[2018,7],[2018,8],[2018,9],[2018,10],[2018,11],[2018,12],[2019,1],[2019,2],[2019,3],[2019,4],[2019,5]]
for month in get_date:
	cmd="python3 get_one_stock.py "+stock_code+" "+str(month[0])+" "+str(month[1])
	print("run "+cmd)
	process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	# 用 communicate 等 subprocess terminate
	process.communicate()
	# 延遲1.7秒，因為5秒內只能 query 3次，twse超爛= =
	time.sleep(1.7)