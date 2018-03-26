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

parser = argparse.ArgumentParser(prog='main_heat.py', 
                                 description='Specify the parameter for Forest Fire Model.')
parser.add_argument('--f_max', type=float, required = True, help='Maximum forward burning probability.')
parser.add_argument('--f_min', type=float, required = True, help='Minimun forward burning probability.')
parser.add_argument('--b_max', type=float, required = True, help='Maximun backard burning probability.')
parser.add_argument('--b_min', type=float, required = True, help='Minimun backard burning probability.')
parser.add_argument('--insert', type=int, required = True, help='Number of insertion between p_min and P_max.')
parser.add_argument('--nodes', type=int, required = True, help='Number of nodes.')
args = parser.parse_args()
#if args.p > 1. or args.r > 1. or args.p <= 0. or args.r <= 0. or args.nodes < 2 or args.p_min >= args.p_max:
#	raise argparse.ArgumentTypeError("Input error.")

#----------------------function definition----------------------------

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
	
	# recording list
	exponent_list = [ [[] for n in range(args.insert)] for m in range(args.insert) ]
	#node_list = [ [[] for n in range(args.insert)] for m in range(args.insert) ]
	#edge_list = [ [[] for n in range(args.insert)] for m in range(args.insert) ]
	diameter_list = [ [[] for n in range(args.insert)] for m in range(args.insert) ]
	#indegree_list = [ [] for m in range(args.insert) ]
	#outdegree_list = [ [] for m in range(args.insert) ]
	
	for m1 in range(args.insert):
		for m2 in range(args.insert):
			# clear graph
			g.clear()
			# vertex 0
			g.add_vertex()
			
			node_list = []
			edge_list = []
			
			# forest fire model
			for n in range(args.nodes - 1):
				# randomly(uniformly) choose a vertex in the existing vertices
				ambassador = numpy.random.random_integers(g.num_vertices()) - 1
				new = g.add_vertex()
				g.add_edge(new, ambassador)
		
				#recursion_set = OrderedSet()
				recursion_que = deque([])
		
				# recursively repeat the process from the chosen ambassador
				f = args.f_min + (args.f_max - args.f_min) / args.insert * m1
				b = args.b_min + (args.b_max - args.b_min) / args.insert * m2
				forest.burning(g, new, ambassador, f, b, recursion_que)
				while len(recursion_que) > 0:
					forest.burning(g, new, recursion_que.popleft(), f, b, recursion_que)

				# recording the evolution
				if n % 100 == 0:
					node_list.append(g.num_vertices())
					edge_list.append(g.num_edges())
					#diameter_list[m1][m2].append(numpy.average(util.effectiveDiameter(g)))
					#diameter_list.append(int(pseudo_diameter(g, g.vertex( g.num_vertices() - 1 ))[0]))
					#diameter_list.append(int(pseudo_diameter(g, g.vertex(0))[0]))
					# uncomment it for debug message
					# debug(g)

			log_node = list(map(math.log,map(float,node_list)))
			log_edge = list(map(math.log,map(float,edge_list)))
			fit = numpy.polyfit(log_node, log_edge, deg=1)
			exponent_list[m1][m2].append(fit[0])
			
			#degree_list[m1].append([v.in_degree() + 1 for v in g.vertices()])
			diameter_list[m1][m2].append(numpy.average(util.effectiveDiameter(g)))
			print(m1)
			print(m2)
		
	# output  to heat_dense.txt
	data = ""
	for m1 in range(args.insert):
		for m2 in range(args.insert):
			data += str(exponent_list[m1][m2][0])
			data += ","
		data = data[:-1]
		data += "\n"
	data = data[:-1]
	print(data)
	print('haha')
	with open("heat_dense.txt", 'w') as f:
		f.write(data)
	
	# output  to heat_shrink.txt
	data = ""
	for m1 in range(args.insert):
		for m2 in range(args.insert):
			data += str(diameter_list[m1][m2][0])
			data += ","
		data = data[:-1]
		data += "\n"
	data = data[:-1]
	print(data)
	print('haha')
	with open("heat_shrink.txt", 'w') as f:
		f.write(data)

if __name__ == "__main__":
	main()
