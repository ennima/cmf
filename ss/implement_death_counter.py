from death_counter import *

dc = DeathCounter()
dc.step = 1000000 * 1000000 * 1000000
dc.set_max_step(1000)
# print("Installed: ",dc.read_installed_dependency())
# print("Counter: ",dc.read_counter_dependency())

for i in range(0,1003):
	print(str(i+1),"--",dc.run_death_counter())