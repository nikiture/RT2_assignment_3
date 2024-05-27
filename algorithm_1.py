#!/usr/bin/env/python

from __future__ import print_function

import time
import math
from sr.robot import *



"""
first 2023 assignment python script

by running this code the robot is tasked with grabbing and moving the boxes such that at the end they will be all together in a specific point

	to run it, type in the command shell one of the following two commands:
	if you have python 3 installed: python run.py assignment.py
	
	if you have python 2 installed: python2 run.py assignment.py 

"""
#algorithm 1 
#author: Torre Nicolo

a_th = 2.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_unmoved_token(moved_token_id):
    """
    Function to find the closest unmoved token
    
    Args: 
    moved_token_id: list of codes (values stored in the .info.code attribute) of either the token where to bring the other boxes close or the tokens which were already moved by the robot

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
	code (int): identifier of the token, corresponding to the attribute .info.code
    """
    dist=100
    m = 0

    for token in R.see():
        
        try:
        	m = moved_token_id.index(token.info.code) 
        	continue   #if index doesn't give an error the token has already been moved, so the robot must not check if it is the closest
        except:    #if index launches an error it means the token has not been moved yet: after catching the error the robot checks if it is closer than previously registered tokens during this call
			if (token.dist < dist):
				dist=token.dist
				rot_y=token.rot_y
				code = token.info.code
    if dist==100:
		return -1, -1, -1
    else:
   		return dist, rot_y, code

def find_center_token(dest_token_id):
    """
    Function to find the token set as destination to place all other tokens
	Args:
	dest_token_id: code identifier of the destination token
    Returns:
	dist (float): distance of the destination token (-1 if not detected)
	rot_y (float): angle between the robot and the token (-1 if not detected)
    """
    dist = -1
    rot_y = -1
    for token in R.see():
        
		if (not token.info.code == dest_token_id): #the robot ignores the token if its code does not coincide with the one of the destination box
		    	continue
		else:
			dist=token.dist
	    	rot_y=token.rot_y
	    	break #if here the robot found the only token set as destination: no other token has to be checked
    return dist, rot_y


token_moved = []
"""
list containing the codes of already moved tokens and of the destination token
"""
max_dist = 0.3
"""
radius of the circle in which the boxes are to be moved
"""


dest_code = -1
"""
(int) storer of the code assigned with the destination box
"""
unseen_count = 0 #counter to check if the robot did a 360 degrees rotation looking for token to move



def token_grab (Robot):
	""" 
	Function to include to R.grab() a print to the terminal about the result of the grebbing attempt
	Args:
	Robot: object identifying the robot that does the action of grabbing
	Returns:
	token_grabbed (bool): result of the grabbing attempt
	"""
	if Robot.grab(): 
		print("Target grabbed!") 
		return True
	else:
		print ("Target missed")
		return False
		
def reach_token (rot):
	"""
	Function to make the robot move towards a specific point by either going straight or adjusting its directiong in order to have the point in more or less front of him 
	Args:
	rot: relative angle between the point to reach and the robot
	"""
	if -a_th<= rot <= a_th: # if the robot is well aligned with the token, we go forward
		#print("This way!.")
		drive(60, 0.1)
	elif rot < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
		#print("Left a bit...")
		turn(-10, 0.1)
	elif rot > a_th:
		#print("Right a bit...")
		turn(+10, 0.1)


def set_destination_token ():
	"""sets a box as the token around which all the others tokens are to be brought
   	   The token selected is going to be the closest the robot can see at the beginning of the simulation
   	   Returns:
   	   dest_code: alias for marker.info.code for the token chosen
   	"""
	while dest_code < 0: #the robot chooses the closest token as the place around which to put the other tokens
			dist, rot_y, targ_code = find_unmoved_token (token_moved)
			if dist==-1: #the robots rotates on itself looking for a token if none are in its field of view
				#print("looking for boxes...")
				turn (20, 0.2)
				continue
			else: 
				print ("Box with code", targ_code, "set as destination to transport other boxes to")
				token_moved.append(targ_code)
				return targ_code 


def print_time_left (delta_time): 
	#msg = 'niki code: time taken: %f seconds\n', 
	print ('algorithm 1: time taken: ', delta_time, ' seconds')
	f = open ('times_1.txt', 'a')
	f.write ('{}\n'.format (delta_time))
        f.close ()



def main ():
	start_time = time.time ()
	grabbed_token = False
	"""
	bool indicating if the robot is holding a box
	"""
	dest_code = set_destination_token ()
	while 1:		

		if not grabbed_token: 
		#the robot looks for tokens to grab if none is grabbed
			#dist = 101
			dist, rot_y, target_code = find_unmoved_token(token_moved)  # we look for token yet to move
			#print (dist)
			if dist==-1:
				#print("looking for tokens to move...")
				
				turn (30, 0.05)
				
				
				unseen_count = unseen_count + 1 #at every iteration this counter increases; when it is at 250 the robot did an entire rotation on himself without finding any unoved token, therefore it assumes no more boxes are to be moved and the robot exits the program
				
				
				if unseen_count > 80:
					print ("No more boxes to be moved found, ending program!")
					break
				
				else:
					continue
			
			else:
				unseen_count = 0
				
				if dist <d_th: # if we are close to the token, we grab it.
					print("Box reached!")
					grabbed_token = token_grab (R)
				
				else:
					reach_token (rot_y)			
		
		else: #if the robot has already grabbed a token it brings it to the destination token
			targ_dist, targ_dir = find_center_token (dest_code)
			
			if targ_dist == -1:
				#print("Looking for the destination box...")
				turn (30, 0.05)
			
			elif  targ_dist < d_th + max_dist : #release of token since we are reasonably close to the target area and memorize it as already moved 
				R.release ()
				print ("Box moved! Looking for next one!")
				drive (-40, 0.5) #the robot goes a bit backwards to avoid colliding with it while looking for another token
				grabbed_token = False
				token_moved.append (target_code)
			
			else: #the robot moves toward the destination token, adjusting its direction if necessary
				reach_token (targ_dir)
	end_time = time.time ()
	delta_time = end_time - start_time
	print_time_left (delta_time)
	#with open ('times.txt', 'a') as f:
		#print ('niki code: time taken: ', delta_time, ' seconds')
		
		
main()

