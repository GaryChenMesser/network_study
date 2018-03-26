# util_forest.py
# Implement the Forest Fire Model.
# 
# Reference:
#  
# Jure Leskovec , Jon Kleinberg , Christos Faloutsos, 
# Graphs over time: densification laws, shrinking diameters and possible explanations
#
# Gary Chen 2018/03/24

from graph_tool.all import *
import numpy
import math

#----------------------------------function definition--------------------------------------

##########################################################################
# Compute effective diameter(smoothed version).
# Choose sources and targets as many as square root 
# of the graph size randomly.
# Compute distance in a bidirected way.
##########################################################################
def effectiveDiameter(g):
	arr = numpy.array(range(g.num_vertices()))
	num = int(math.sqrt(float(g.num_vertices())))
	diameter = []
	
	sample(arr, num)
	
	g.set_directed(False)
	for i in range(num):
		diameter.extend(shortest_distance(g, numpy.random.random_integers(g.num_vertices()) - 1, arr[:num]))
	g.set_directed(True)
	
	#print('dia')
	#print(diameter)
	return diameter

#######################################################
# sample for num of distinct result out of arr
# has similar effect as numpy.random.choice
# no return value, pass arr by reference
#
# three cases:
# case 1
# if length > num * 2: sampling for wanted
# case 2:
# if num * 2 > length > num: sampling for unwanted
# case 3:
# esle: then take all as sampling result, which
#       means do nothing
########################################################
def sample(arr, num):
	length = len(arr)
	
	if length > num * 2:
		for left in range(num):
			index = numpy.random.random_integers(length - left)
			
			swap = arr[left]
			arr[left] = arr[-1 * index]
			arr[-1 * index] = swap
			
	elif length > num:
		num = length - num
		
		for left in range(num):
			index = numpy.random.random_integers(length - left) - 1
			
			swap = arr[-1 * left - 1]
			arr[-1 * left - 1] = arr[index]
			arr[index] = swap
