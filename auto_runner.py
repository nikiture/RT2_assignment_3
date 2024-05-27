import random
import subprocess
from threading import Thread
import random



def call_first_code ():
	subprocess.call (["python2", "run.py",  "algorithm_1.py"])
def call_second_code ():
	subprocess.call (['python2', 'run.py', 'algorithm_2.py'])
	
thread1 = Thread (target = call_first_code)
thread2 = Thread (target = call_second_code)
thread1.start ()
thread2.start ()
#6 minutes timeout, if more then that failure
thread1.join (360)
thread2.join (360)

#subprocess.run (["run.py"])



