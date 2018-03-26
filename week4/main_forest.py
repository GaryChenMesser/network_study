# main_forest.py
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

import myforest as forest
import util_forest as util

#----------------------------------parse for arguments--------------------------------------

parser = argparse.ArgumentParser(prog='main_forest.py', 
                                 description='Specify the parameter for Forest Fire Model.')
parser.add_argument('--f', type=float, required = True, help='Forward burning probability.')
parser.add_argument('--b', type=float, required = True, help='Backard burning probability.')
parser.add_argument('--nodes', type=int, required = True, help='Number of nodes.')
args = parser.parse_args()
if args.p > 1. or args.r > 1. or args.p <= 0. or args.r <= 0. or args.nodes < 2:
	raise argparse.ArgumentTypeError("Input error.")

#----------------------------------function definition--------------------------------------

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
		forest.burning(g, new, ambassador, args.p, args.r, recursion_que)
		while len(recursion_que) > 0:
			forest.burning(g, new, recursion_que.popleft(), args.p, args.r, recursion_que)

		# recording the evolution
		if n % 1000 == 0:
			node_list.append(g.num_vertices())
			edge_list.append(g.num_edges())
			diameter_list.append(numpy.average(util.effectiveDiameter(g)))
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







	
