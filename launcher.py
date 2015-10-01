#!/usr/bin/python3

import math
import sys
import numpy as np
from datetime import datetime
from multiprocessing import Process, Queue

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
	

def chooseApplicants(array, alg):
	testGroup = groupSize(len(array), alg)
	highest = max(array[0:testGroup])
	#print("Testing first " + str(len(array[0:testGroup])))
	for x in array[testGroup-1:len(array)+1]:
		if x >= highest:
			return x

def calculate(testCount, topRange, q):
	localCorrect=0
	for x in range(1, int(testCount+1)):
		
		applicants = initApplicants(applicantCount, topRange)
		solution=chooseApplicants(applicants, sys.argv[3])
		#print(x)
		divisor=testCount/20
		#if x % divisor == 0:
		#	sys.stdout.write("\r%f" % int((float(x)/testCount)*100))
		#	sys.stdout.flush()

		if solution == max(applicants):
			localCorrect += 1
	q.put(localCorrect)


###BEGIN MAIN PROGRAM

topRange = 101
applicantCount = int(sys.argv[1])
testCount = int(sys.argv[2])
quadMode=sys.argv[4]

correct=0.00
startTime = datetime.now()
q = Queue()

if quadMode=='quad':
	print("Quad process mode...")
	threads=4
	p1 = Process(target=calculate, args=(testCount/threads,topRange, q))
	p1.start()
	p2 = Process(target=calculate, args=(testCount/threads,topRange, q))
	p2.start()
	p3 = Process(target=calculate, args=(testCount/threads,topRange, q))
	p3.start()
	p4 = Process(target=calculate, args=(testCount/threads,topRange, q))
	p4.start()  
	results = []

	for i in range(threads):
		#set block=True to block until we get a result
		results.append(q.get(True))
		     
	
	
else:
	print("Single process mode...")
	threads=1
	p1 = Process(target=calculate, args=(testCount/threads,topRange, q))
	p1.start() 
	results = []

	for i in range(threads):
		#set block=True to block until we get a result
		results.append(q.get(True))
	
correct=float(sum(results))

sys.stdout.write("\n")
print(correct)
print(str((correct/testCount)*100) + "% accuracy") 
print("Operation took "+ str(datetime.now() - startTime))









