import sys
from graph_tool.all import *
import math
import numpy as np

g = load_graph(sys.argv[1])
deg = g.degree_property_map("in")
deg.a = 2 * (np.sqrt(deg.a) * 0.5 + 0.4)
ebet = betweenness(g)[1]
graphviz_draw(g, vcolor=deg, vorder=deg, elen=10, 
              ecolor=ebet, eorder=ebet, output=sys.argv[1].split('.')[0]+".pdf")
