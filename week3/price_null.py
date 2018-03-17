#  price_null.py
#  Implement the Price model using a null vertex in representation
#  of a. This method has a     
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
MAX_STEP = int(10e+6)
NULL_VERTEX = 0

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

# intitial condition
# add a null vertex with index 0
g.add_vertex(args.init + 1)

for i in range(1, args.init + 1):
	for j in range(args.a):
		g.add_edge(NULL_VERTEX, i)

# start the process
for step in range(args.step):
	chosen = []
	edges = list(g.edges())
	for c in range(args.c):
		rand = random.randrange( 0, len(edges) )
		chosen.append( edges[rand].target() )
		
	new_vertex = g.add_vertex()
	
	for choice in chosen:
		if choice == 0:
			print("Error\n")
		g.add_edge(new_vertex, choice)
		for c in range(args.c):
			g.add_edge(NULL_VERTEX, new_vertex)
	
	if (step + args.init + 1) % 500 == 0:
		print('number of vertex: ', step + args.init + 1)
		print('number of edge: ', (step + 1) * args.c)

# filter out the null vertex and related edges
_map = g.new_edge_property("bool", val=True)
for i in g.vertex(NULL_VERTEX).out_neighbors():
	for j in g.edge(NULL_VERTEX, i, all_edges=True):
		_map[j] = False
g.set_edge_filter(_map)

print("--- %s seconds ---" % (time.time() - start_time))

# plot it
in_hist = vertex_hist(g, "in")

y = in_hist[0]
err = sqrt(in_hist[0])
err[err >= y] = y[err >= y] - 1e-2

figure(figsize=(6,4))
errorbar(in_hist[1][:-1], in_hist[0], fmt="o", yerr=err,
        label="in")
gca().set_yscale("log")
gca().set_xscale("log")
gca().set_ylim(1e-1, 1e5)
gca().set_xlim(0.8, 1e3)
subplots_adjust(left=0.2, bottom=0.2)
xlabel("$k_{in}$")
ylabel("$NP(k_{in})$")
tight_layout()
savefig("price_null-deg-dist.pdf")
