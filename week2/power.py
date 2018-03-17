import powerlaw
import networkx as nx
import sys
import scipy
#import numpy as np
#help(powerlaw)
G = nx.read_edgelist(sys.argv[1])
data = sorted([d for n, d in G.degree()]) # data can be list or numpy array
print(data)
results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')
