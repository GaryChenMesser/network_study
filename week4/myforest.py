# myforest.py
# Implement the Forest Fire Model.
# 
# Reference:
#  
# Jure Leskovec , Jon Kleinberg , Christos Faloutsos, 
# Graphs over time: densification laws, shrinking diameters and possible explanations
#
# Gary Chen 2018/03/24

import numpy
import util_forest as util

#----------------------------------function definition--------------------------------------

############################################################################################
# The process of burning:
# Although it's a recursive process,
# the maximum recursive depth exceeded for p > 0.5 and r > 0.5 roughly.
# Hence, I implement burning procrss in iterative way.
#
############################################################################################
def burning(g, new, source, forward, backard, recursion_que):
	# decide x and y using geometric distribution
	x = numpy.random.geometric(1 - forward) - 1
	y = numpy.random.geometric(1 - backard) - 1
	
	# get out- and in-degree list from the given source
	out_list = g.get_out_neighbors(source)
	in_list = g.get_in_neighbors(source)
	out_n = g.get_out_neighbors(new)
	
	# filter out the visited vertices
	out_list = numpy.setdiff1d(out_list, out_n, assume_unique = True)
	in_list = numpy.setdiff1d(in_list, out_n, assume_unique = True)
	#out_set.difference_update(resursion_set)
	#in_set.difference_update(resursion_set)
	
	# sampling uniformly:
	# if the # of sample is larger than # of provided list,
	# the list itself is the sample result
	util.sample(out_list, x)
	util.sample(in_list, y)
	if len(out_list) < x:
		x = len(out_list)
	if len(in_list) < y:
		y = len(in_list)
	
	# update recursion_que
	recursion_que.extend(out_list[:x])
	recursion_que.extend(in_list[:y])
	
	for _x in range(x):
		g.add_edge(new, out_list[_x])
		
	for _y in range(y):
		g.add_edge(new, in_list[_y])
