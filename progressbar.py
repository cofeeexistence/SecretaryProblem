#!/usr/bin/python3
import sys
import math

def progressBar(progress, completion, resolution=20):
    index=math.ceil(((progress/completion)*resolution))
    sys.stdout.write("\r|")
    for x in range(index):
        sys.stdout.write("#")
    for x in range(resolution-index):
        sys.stdout.write("-")
    sys.stdout.write("| %f %% complete" % int((float(progress)/completion)*100))
    sys.stdout.flush()

done = input('How many done?')
total = input('Out of')
progressBar(int(done), int(total))
