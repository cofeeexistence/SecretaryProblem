#!/usr/bin/python3

import collections
import math
import sys
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt
import operator
import time
import shelve
from mpl_toolkits.mplot3d import Axes3D



def configValue(fileName, key, returnType='str'):
	configFile = open(fileName, 'r')
	
	cache = configFile.read()
	
	index = cache.find(key, 0, len(cache))
	if index!=(-1):
		end=cache.find(">", index+1, len(cache))
		configFile.close()
		if returnType=='int':
			return int(cache[index+len(key)+1:end])
		else:
			return cache[index+len(key)+1:end]
	
	configFile.close()

topRange = configValue("./cfg/Secretary.cfg", "topRange", 'int')

def initApplicants(size):
	array=[]
	for x in range(size):
		array.append(np.random.random_integers(0, topRange))
	return array

def groupSize(length, alg):
	if alg=='a':
		result = math.sqrt(length)
		return int(math.ceil(result))
	if alg=='b':
		result = math.sqrt(length)
		result += math.sqrt(result)*(length/10)
		return int(math.ceil(result))
	if alg=='b2':
		result = math.sqrt(length)
		result += math.sqrt(result)*(length/(length/10))
		return int(math.ceil(result))
	if alg=='e':
		result = length/math.e
		
		return int(math.ceil(result))
	
def testGroupSize(array, alg):
	return groupSize(len(array), alg)

def chooseApplicants(array, testGroup):
	if testGroup==0:
		return 0
	highest = max(array[0:testGroup])
	for x in array[testGroup-1:len(array)+1]:
		if x >= highest:
			return x

def progressBar(progress, completion, resolution=20):
    index=math.ceil(((progress/completion)*resolution))
    sys.stdout.write("\r|")
    for x in range(index):
        sys.stdout.write("#")
    for x in range(resolution-index):
        sys.stdout.write("-")
    sys.stdout.write("| %f %% complete" % int((float(progress)/completion)*100))
    sys.stdout.flush()
    
def calculate(testCount, configFile, applicantCount, q, progress='no', customSize='no', sizeValue=0):
	alg = configValue(configFile, "alg")
	localCorrect=0
	for x in range(1, int(testCount+1)):
		
		applicants = initApplicants(applicantCount)

		if customSize=='yes':
			solution=chooseApplicants(applicants, sizeValue)
		else:
			size=testGroupSize(applicants, alg)
			solution=chooseApplicants(applicants, size)

		divisor=testCount/20
		if progress=='yes':
                        if x % divisor == 0:
                                
                                progressBar((x), testCount)
		if solution == max(applicants):
			localCorrect += 1
	q.put(localCorrect)

def testAccuracy(configFile, testGroupSize, applicantCount, verbose='yes'):
	testCount = configValue(configFile, "testCount", 'int')
	quadMode = configValue(configFile, "quadMode")
	correct=0.00
	startTime = datetime.now()
	q = Queue()

	if __name__ == '__main__':    
		results = []
		if quadMode=='yes':

		        threads=4
		        p1 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, verbose, 'yes', testGroupSize))
		        p1.start()
		        p2 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p2.start()
		        p3 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p3.start()
		        p4 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'no', 'yes', testGroupSize))
		        p4.start()  
		        

		        for i in range(threads):
		                #set block=True to block until we get a result
		                results.append(q.get(True))
		                     
		        
		        
		else:
		        threads=1
		        p1 = Process(target=calculate, args=(testCount/threads, configFile, applicantCount, q, 'yes', 'yes', testGroupSize))
		        p1.start() 
			
		        for i in range(threads):
		                #set block=True to block until we get a result
		                results.append(q.get(True))
		                     
	
		correct=float(sum(results))
		if verbose=='yes':
			sys.stdout.write("\n")
			#print(correct)
			#print(str(accuracy) + "% accuracy") 
			#print("Operation took "+ str(datetime.now() - startTime))

		accuracy=(correct/testCount)*100
		return accuracy

def hundreths_arr(value):
	return_value=[]
	divisor=value/100
	for x in range(100):
		return_value.append( int((x+1)*divisor) )
	return return_value
		
		

def ternarySearch(f, left, right, absolutePrecision):
    """
    Find maximum of unimodal function f() within [left, right]
    To find the minimum, revert the if/else statement or revert the comparison.
    """
    while True:
        #left and right are the current bounds; the maximum is between them
        if abs(right - left) < absolutePrecision:
            return (left + right)/2

        leftThird = left + (right - left)/3
        rightThird = right - (right - left)/3
	
	

        if f(leftThird) < f(rightThird):
            left = leftThird
        else:
            right = rightThird

def findOptimalStopping(secretaryCount, method):
	startTime = datetime.now()
	values=[]
	accuracy={}
	if method=='-b': #brute

		for x in range(secretaryCount):
			indexAccuracy = testAccuracy("./cfg/Secretary.cfg", x, secretaryCount)
			accuracy[x]=indexAccuracy
			#values.append(x)
			print("\n" +str(x)+" of "+str(secretaryCount/100) + " had accuracy of " + str(indexAccuracy))
			progressBar(x, secretaryCount)
			print("\n")

	if method=="-t": #ternary search
		
		left=3
		right=secretaryCount-1	
		absolutePrecision=3
		testers_hundreths=hundreths_arr(secretaryCount)
		#print("got this far")
		while True:
			#left and right are the current bounds; the maximum is between them
			if abs(right - left) <= absolutePrecision:
			    break

			leftThird = int(left + (right - left)/3)
			rightThird = int(right - (right - left)/3)
			
			leftThird_f=testAccuracy("./cfg/Secretary.cfg", leftThird, secretaryCount)
			accuracy[int(leftThird)]=leftThird_f	
			print("\n" +str(leftThird)+" of "+str(secretaryCount) + " had accuracy of " + str(leftThird_f))

			rightThird_f=testAccuracy("./cfg/Secretary.cfg", rightThird, secretaryCount)
			accuracy[int(rightThird)]=rightThird_f	
			print("\n" +str(rightThird)+" of "+str(secretaryCount) + " had accuracy of " + str(rightThird_f))

			if leftThird_f < rightThird_f:
			    left = leftThird
			else:
			    right = rightThird
	
	

	optimal_index=max(accuracy.items(), key=operator.itemgetter(1))[0]
	optimal_value=accuracy[optimal_index]

	#print("\nOperation took "+ str(datetime.now() - startTime))
	#print("Optimal stopping point is: " + str(optimal_index) +" at " + str(optimal_value) + " accuracy.")
	
	values = [] #in same order as traversing keys
	keys = [] #also needed to preserve order
	for key in accuracy.keys():
		keys.append(key)
		values.append(accuracy[key])	
	return optimal_index
#	plt.plot(keys, values, 'ro')
#	plt.show()

			
def getArg(arg_name):
	return sys.argv[sys.argv.index(arg_name)+1]


def isArg(arg_name):
	try:
		sys.argv.index(arg_name)
	
	except ValueError:
		return False
	else:
		return True
	

def calcDimension(verbose, dimension):

	global topRange
	topRange=dimension 	
	results={}
	database=shelve.open('./db/solutions.db', writeback=True)

	try:
		database['mainDict'[dimension]]
	
	except KeyError:
		results={}
		more=0
	except IndexError:
		results={}
		more=0
	else:
		results=database['mainDict'[dimension]]
		if isArg('-start'):
			more=int(getArg('-start'))
		else:
			more = max(results.items(), key=operator.itemgetter(1))[0]

	if isArg('run'):

		#aV=configValue("./cfg/Secretary.cfg", "applicantCount", 'int')
		runTime=int(getArg('run'))
		startTime=time.time()
		endTime=startTime+runTime
		x_count=10+more
		optimal_keys=[]
		optimal_values=[]

		time_dict={}

		while (time.time()<endTime):
			instance_start_time=time.time()
			cache=findOptimalStopping(x_count, "-t")
			results[x_count]=cache
			optimal_keys.append(x_count)
			optimal_values.append(cache)
			time_dict[x_count]=time.time()-instance_start_time
			x_count+=int(x_count/10)
		
		if verbose:
			plt.plot(optimal_keys, optimal_values, 'ro')
			plt.show()

			print(str(time_dict))

		['mainDict'[dimension]]=results

	elif isArg('run-until'):

		#aV=configValue("./cfg/Secretary.cfg", "applicantCount", 'int')
		until=int(getArg('run-until'))
		x_count=10+more
		optimal_keys=[]
		optimal_values=[]

		while (x_count<until):
			cache=findOptimalStopping(x_count, "-t")
			results[x_count]=cache
			optimal_keys.append(x_count)
			optimal_values.append(cache)
			x_count+=int(x_count/10)

		if verbose:
			plt.plot(optimal_keys, optimal_values, 'ro')
			plt.show()
		print(results)
		whole_db=database['mainDict']
		print(whole_db)
		print(dimension)
		whole_db[dimension]=results
		database['mainDict']=whole_db

	if verbose:
		total_keys=[]
		total_values=[]
	
		for key in results.keys():
			total_keys.append(key)
			total_values.append(results[key])	

		plt.plot(total_keys, total_values, 'ro')
		plt.show()
		print(str(results))

	database.close()

if isArg('calculate') and isArg('-from') and isArg('-to'):
	
	_from=int(getArg('-from'))
	to=int(getArg('-to'))+1	
	
	for dim in range(_from, to):
		print("Calculating Dimension"+str(dim))
		calcDimension(False, dim)
		


elif isArg('show_3d'):
	database=shelve.open('./db/solutions.db', writeback=True)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	for dimKey_z, dimDict in database['mainDict'].items():
		total_keys=[]
		total_values=[]
		
		for key in dimDict.keys():
			total_keys.append(key)
			total_values.append(dimDict[key])
	
		ax.bar(total_keys, total_values, dimKey_z, zdir='y')
	ax.set_xlabel('Number of applicants')
	ax.set_zlabel('Optimal stopping value')
	ax.set_ylabel('Fitness resolution')
	plt.show()
	database.close()
	
	

	
	







