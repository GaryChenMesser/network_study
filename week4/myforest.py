#  myforest.py
#  
#  
#
# Gary Chen 2018/03/24

from graph_tool.all import *
from pylab import *
import sys
import argparse
import numpy
import time

# parse for arguments
parser = argparse.ArgumentParser(prog='myforest.py', description='Specify the parameter for Forest Fire Model.')
parser.add_argument('--p', type=float, required = True, help='Forward burning probability.')
parser.add_argument('--r', type=float, required = True, help='Backard burning probability.')
parser.add_argument('--nodes', type=int, required = True, help='Number of nodes.')
args = parser.parse_args()
if args.p > 1. or args.r > 1. or args.p <= 0. or args.r <= 0. or args.nodes < 2:
	raise argparse.ArgumentTypeError("Input error.")

# function
def burning(new, source, forward, backard):
	x = numpy.random.geometric(1 - forward) - 1
	y = numpy.random.geometric(1 - forward * backard) - 1
	#print(x)
	#srint(y)
	
	out_list = g.get_out_edges(source)[:, 1]
	in_list = g.get_in_edges(source)[:, 1]
	sample(out_list, x)
	sample(in_list, y)
	print(out_list)
	
	if len(out_list) < x:
		x = len(out_list)
	if len(in_list) < y:
		y = len(in_list)
	
	for _x in range(x):
		g.add_edge(new, out_list[_x])
	for _x in range(x):
		burning(new, out_list[_x], forward, backard)
		
	for _y in range(y):
		g.add_edge(new, in_list[_y])
	for _y in range(y):
		burning(new, in_list[_y], forward, backard)

# has similar effect as numpy.random.choice 
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
	

# create a directed empty graph
g = Graph()
g.add_vertex()
node_list = []
edge_list = []

for n in range(args.nodes - 1):
	new = g.add_vertex()
	ambassador = numpy.random.random_integers(len(g.get_vertices())) - 1
	g.add_edge(new, ambassador)
	
	burning(new, ambassador, args.p, args.r)
	
	if n % 100 == 0:
		node_list.append(len(g.get_vertices()))
		edge_list.append(len(g.get_edges()))
		print(node_list[-1])
		print(edge_list[-1])

print(node_list)
print(edge_list)







	
