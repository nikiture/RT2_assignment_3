import math


#using two_sample t-test between 2 algorithms
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

#print (times1)
#print (times2)
#print (len (times1))
mean1 = 0
mean2 = 0
for n in times1:
	mean1 += float(n)/N1
for n in times2: 
	mean2 += float(n)/N2

var1 = var2 = 0
for n in times1:
	var1 += pow (n - mean1, 2)
var1 /= float (N1)
for n in times2:
	var2 += pow (n - mean2, 2)
var2 /= float(N2)

se1 = math.sqrt (var1) / math.sqrt (N1)
se2 = math.sqrt (var2) / math.sqrt (N2)

pool_var = ((N1 - 1) * se1 * se1 + (N2 - 1) * se2 *se2) / (N1 + N2 - 2)
pool_se = math.sqrt (pool_var * (float(1)/N1 + float(1)/N2))

t_diff = (mean1 - mean2) / pool_se

print ('mean1: {0}, mean2: {1}, pool_se: {2}'.format (mean1, mean2, pool_se))

print ('estimated t: {0}, DOF: {1}'.format (t_diff, N1 + N2 - 2)) 
f1.close ()
f2.close ()

#test result: t = -51, DOF = 58
#H0 is rejected with confidence level bigger than (1 - 0.001) = 99. 9 % and probability error < 0.1 %
#algorithm 1 is faster than algorithm 2 with (way?) less than 0.1 % chance of error 

