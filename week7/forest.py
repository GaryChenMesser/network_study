from graph_tool.all import *
from collections import deque

import numpy

def _sample(arr, num):
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
			
def _burning(g, new, source, forward, backard, recursion_que):
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
	_sample(out_list, x)
	_sample(in_list, y)
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

def _debug(g):
	print('Number of nodes: ', g.num_vertices())
	print('Number of edges: ', g.num_edges())

def forest(p, r, nodes):
	# create a directed empty graph
	g = Graph()
	# vertex 0
	g.add_vertex()
	
	# recording list
	node_list = []
	edge_list = []
	diameter_list = []

	# forest fire model
	for n in range(nodes - 1):
		# randomly(uniformly) choose a vertex in the existing vertices
		ambassador = numpy.random.random_integers(g.num_vertices()) - 1
		new = g.add_vertex()
		g.add_edge(new, ambassador)
		
		#recursion_set = OrderedSet()
		recursion_que = deque([])
		
		# recursively repeat the process from the chosen ambassador
		_burning(g, new, ambassador, p, r, recursion_que)
		while len(recursion_que) > 0:
			_burning(g, new, recursion_que.popleft(), p, r, recursion_que)
	return g
