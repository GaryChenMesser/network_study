#  price_vlist.py
#  Implement the Price model using a vertex list to represent 
#  a and c.    
#  
#
# Gary Chen 2018/03/18

from graph_tool.all import *
from pylab import *
import sys
import argparse
import random
import time

import powerlaw

# parameter
MAX_STEP = int(10e+6)

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
vlist = []

# intitial condition
g.add_vertex(args.init)

for i in range(0, args.init):
	for j in range(args.a):
		vlist.append(i)

# start the process
for step in range(args.step):
	chosen = []
	for c in range(args.c):
		chosen.append(vlist[random.randrange( 0, len(vlist))])
		
	new_vertex = g.add_vertex()
	
	for choice in chosen:
		g.add_edge(new_vertex, choice)
		vlist.append(choice)
	for a in range(args.a):
		vlist.append(new_vertex)
	
	if (step + 1 + args.init) % 5000 == 0:
		print('number of vertex: ', step + 1 + args.init)
		print('number of edge: ', (step+1) * args.c)

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
savefig("price_vlist-deg-dist.pdf")

# output the vertex degree to temp.txt
dlist = sorted([v.in_degree() + 1 for v in g.vertices()])
data = ""
for d in dlist:
	data += str(d)
	data += ","
data = data[:-1]

with open("temp.txt", 'w') as f:
	f.write(data)
