'''
script for timing how long it takes 
to generate the shapes
'''
import sys
import time
sys.path.append("../")
import Shapes
times = {}
for i in range(10):
    times[i+1] = []
print(times)
w = Shapes.World()
for i in range(10): # make 10 measurements
    for j in range(10): #make between 1 and 10 shapes
        if j == 0:
            start_time = time.perf_counter_ns()
            w.create_initial_shape()
            times[j+1].append(time.perf_counter_ns() - start_time)
        else:
            print(f"=====/n{j}/n=====")
            time.sleep(2)
            start_time = time.perf_counter_ns()
            w.create_new_shape()
            times[j+1].append(time.perf_counter_ns() - start_time)
            if j == 9:
                w.clear()
print(times)     