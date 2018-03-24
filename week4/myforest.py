# myforest.py
# Implement the Forest Fire Model.
# 
# Reference:
#  
# Jure Leskovec , Jon Kleinberg , Christos Faloutsos, 
# Graphs over time: densification laws, shrinking diameters and possible explanations
#
# Gary Chen 2018/03/24

from graph_tool.all import *
from pylab import *
import sys
import argparse
import numpy
import time
import math
#from orderedset import OrderedSet
from collections import deque

#----------------------------------parse for arguments--------------------------------------

parser = argparse.ArgumentParser(prog='myforest.py', 
                                 description='Specify the parameter for Forest Fire Model.')
parser.add_argument('--p', type=float, required = True, help='Forward burning probability.')
parser.add_argument('--r', type=float, required = True, help='Backard burning probability.')
parser.add_argument('--nodes', type=int, required = True, help='Number of nodes.')
args = parser.parse_args()
if args.p > 1. or args.r > 1. or args.p <= 0. or args.r <= 0. or args.nodes < 2:
	raise argparse.ArgumentTypeError("Input error.")

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
	y = numpy.random.geometric(1 - forward * backard) - 1
	
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
	sample(out_list, x)
	sample(in_list, y)
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

########################################################
# Compute effective diameter(smoothed version).
# Choose sources and targets as many as square root 
# of the graph size randomly.
# Compute distance in a bidirected way.
########################################################
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

####################################
# output debug message
####################################
def debug(g):
	print('Number of nodes: ', g.num_vertices())
	print('Number of edges: ', g.num_edges())

################################################
# main function:
# 1. generate graph using forest fire model
# 2. record the evolution
# 3. write the result to related file
################################################
def main():
	start_time = time.time()
	# create a directed empty graph
	g = Graph()
	# vertex 0
	g.add_vertex()
	
	# recording list
	node_list = []
	edge_list = []
	diameter_list = []

	# forest fire model
	for n in range(args.nodes - 1):
		# randomly(uniformly) choose a vertex in the existing vertices
		ambassador = numpy.random.random_integers(g.num_vertices()) - 1
		new = g.add_vertex()
		g.add_edge(new, ambassador)
		
		#recursion_set = OrderedSet()
		recursion_que = deque([])
		
		# recursively repeat the process from the chosen ambassador
		burning(g, new, ambassador, args.p, args.r, recursion_que)
		while len(recursion_que) > 0:
			burning(g, new, recursion_que.popleft(), args.p, args.r, recursion_que)

		# recording the evolution
		if n % 1000 == 0:
			node_list.append(g.num_vertices())
			edge_list.append(g.num_edges())
			diameter_list.append(numpy.average(effectiveDiameter(g)))
			#diameter_list.append(int(pseudo_diameter(g, g.vertex( g.num_vertices() - 1 ))[0]))
			#diameter_list.append(int(pseudo_diameter(g, g.vertex(0))[0]))
			# uncomment it for debug message
			# debug(g)
	
	# print the time elapse
	print("--- %s seconds ---" % (time.time() - start_time))

	# print the record
	print(node_list)
	print(edge_list)
	
	# output the vertex degree to degree.txt
	dlist = [v.in_degree() + 1 for v in g.vertices()]
	data = ""
	for d in dlist:
		data += str(d)
		data += ","
	data = data[:-1]
	data += '\n'
	dlist = [v.out_degree() + 1 for v in g.vertices()]
	for d in dlist:
		data += str(d)
		data += ","
	data = data[:-1]

	with open("degree.txt", 'w') as f:
		f.write(data)

	# output the vertex and edge number over time to node_edge.txt
	data = ""
	for n in node_list:
		data += str(n)
		data += ","
	data = data[:-1] + '\n'
	for e in edge_list:
		data += str(e)
		data += ","
	data = data[:-1]

	with open("node_edge.txt", 'w') as f:
		f.write(data)
		print(data)

	# output pseudo_diameter to diameter.txt
	data = ""
	for d in diameter_list:
		data += str(d)
		data += ","
	data = data[:-1]
	#data += '\n'
	#for n in node_list:
	#	data += str(n)
	#data = data[:-1]
	print('diameter = ', data)
	with open("diameter.txt", 'w') as f:
		f.write(data)
	
	

if __name__ == '__main__':
	main() 







	
