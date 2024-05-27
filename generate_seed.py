import time
import random



random.seed (time.time ())

sample_num = 30
seeds = []


for i in range (0, sample_num):
	seeds.append(random.random ())
	
print (seeds)
