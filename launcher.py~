#!/usr/bin/python

import random

def initApplicants(size, topRange):
	array=[]
	for x in xrange(size):
		array.append(random.randrange(topRange))
	return array
		

topRange = 101
applicantCount = input("How many applicants do we have to choose from?")
print applicantCount

applicants = initApplicants(applicantCount, topRange)

print applicants

print "Most suitable applicant is: " + str(max(applicants))

