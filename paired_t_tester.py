import math


#using paired t-test between 2 algorithms
#observation/hypothesis: algorithm 1 faster than algorithm 2
#null hypothesis: algorithm 1 as fast as or slower than algorithm 2
#alternative hypothesis: mean1 < mean2
#30 tests done per algorithm
N1 = 30
N2 = 30
n1 = n2 = 0
#time taken for the algorithms read from files
f1 = open ('times_1.txt')
f2 = open ('times_2.txt')
times1 = []
times2 = []
#iter over lines in the files 
for i in f1: 
	n1 += 1
	s = i.replace ('\n', '')
	#f = filter (str.isdecimal, i)
	times1.append (float (s))

for i in f2:
	n2 += 1
	s = i.replace ('\n','' )
	times2.append (float (s))
	
#for failures set time taken to 5 minutes
for i in range (n1, N1):
	times1.append (300)

for i in range (n2, N2):
	times2.append (300)
	
#d = times1 - times2
d = []
for (t1, t2) in zip (times1, times2):
	d.append (t1 - t2)
#print (d)

mean_d = 0
for i in d:
	mean_d += i
mean_d /= float (N1)
var_d = 0
for n in d:
	var_d += pow (n - mean_d, 2)
var_d /= float(N1)

se_d = math.sqrt (var_d / N1)

t = mean_d /  se_d
print ('estimated t: {0}, DOF: {1}'.format (t, N1 - 1)) 
f1.close ()
f2.close ()

