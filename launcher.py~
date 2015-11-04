#!/usr/bin/python3

import collections
import math
import sys
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue
import matplotlib.pyplot as plt

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


def initApplicants(size, topRange):
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
	#print("Testing first " + str(len(array[0:testGroup])))
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
	topRange = configValue(configFile, "topRange", 'int')
	alg = configValue(configFile, "alg")
	localCorrect=0
	for x in range(1, int(testCount+1)):
		
		applicants = initApplicants(applicantCount, topRange)

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




###BEGIN MAIN PROGRAM
def testAccuracy(configFile, testGroupSize, applicantCount, verbose='yes'):
	testCount = configValue(configFile, "testCount", 'int')
	quadMode = configValue(configFile, "quadMode")
	#print(configValue(configFile, "topRange"))
	

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
		
		

def findOptimalStopping(secretaryCount, method):
	startTime = datetime.now()
	values=[]
	accuracy=[]
	if method=='brute':
		testers_hundreths=hundreths_arr(secretaryCount)
		print(str(testers_hundreths))
		for x in testers_hundreths:
			indexAccuracy = testAccuracy("Secretary.cfg", x, secretaryCount)
			accuracy.append(indexAccuracy)
			values.append(x)
			print("\n" +str(x)+" of "+str(secretaryCount/100) + " had accuracy of " + str(indexAccuracy))
			progressBar(x, secretaryCount)
			print("\n")
	
	
	accuracy
	accuracy_np=np.array(accuracy)
	optimal_index=accuracy_np.argmax()
	optimal_value=values[optimal_index]

	print("\nOperation took "+ str(datetime.now() - startTime))
	print("Optimal stopping point is: " + str(optimal_value))
	
	plt.plot(values, accuracy, 'ro')
	plt.show()
			
aV=configValue("Secretary.cfg", "applicantCount", 'int')
print(str(aV))
findOptimalStopping(aV, 'brute')





