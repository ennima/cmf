from time_metrics import *

time_metric = TimeMetrics()

time_metric.init()
print("Begin")
sleep(1000/1000)
print("end")
print(time_metric.get_elapsed_time())