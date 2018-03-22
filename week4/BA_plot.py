#  BA_plot.py
#   
#  
#
# Gary Chen 2018/03/18

from graph_tool.all import *
from pylab import *
import sys
import argparse
import random
import time

# parameter
node_list = []
edge_list = []
diameter_list = []

# parse for arguments
parser = argparse.ArgumentParser(prog='price.py', description='Specify the parameter for Price Model.')
parser.add_argument('--init', type=int, required = True, help='The initial volume.')
parser.add_argument('--a', type=int, required = True, help='The constant a.')
parser.add_argument('--c', type=int, required = True, help='The number of newly added edges.')
parser.add_argument('--step', type=int, required = True, help='The step of the process.')
args = parser.parse_args()
if args.init < 1 or args.a < 1 or args.c < 1 or args.step < 1:
	raise argparse.ArgumentTypeError("Each of the arguments must be larger than 0.")

start_time = time.time()

# create a directed empty graph
g = Graph()

# record evolution
g.add_vertex(args.init)
for count in range( int(args.step / 1000) ):
	g = price_network( (count + 1) * 100 + args.init, m=args.a, c=args.a, seed_graph=g)
	
	n = len(g.get_vertices())
	node_list.append(n)
	edge_list.append(len(g.get_edges()))
	
	g.set_directed(False)
	diameter_list.append(int(pseudo_diameter(g, g.vertex(n - 1))[0]))
	g.set_directed(True)
	
# print time elapse
print("--- %s seconds ---" % (time.time() - start_time))

# output the vertex degree to degree.txt
dlist = [v.in_degree() + 1 for v in g.vertices()]
data = ""
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

