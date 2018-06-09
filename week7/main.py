import sys
from graph_tool.all import *
import powerlaw
import numpy
import argparse

import forest
import vis
import percolation
import plot

parser = argparse.ArgumentParser(prog='perco.py', 
                                 description='Percolation.')
#parser.add_argument('--p', type=float, required = True, help='Forward burning probability.')
#parser.add_argument('--r', type=float, required = True, help='Backard burning probability.')
#parser.add_argument('--nodes', type=int, required = True, help='Number of nodes.')
parser.add_argument('--file', type=str, required = True, help='File.')
args = parser.parse_args()



# forest fire, price, barabasi
models = ['random', 'price', args.file]
sizes = [400, 2000, 10000]

forest_param = [[0.30, 0.95], [0.32, 0.95], [0.34, 0.95], [0.36, 0.95]]
price_param = [[3, 1], [3, 2], [3, 3], [3, 4]]
random_param = [0.001, 0.002, 0.004, 0.008]

class deq_sampler:
  def __init__(self, degree):
    self.degree = degree
  def degree_sequence(self, index):
    return self.degree[index]

for model in models:
  print model
  for size in sizes:
    print size
    # generate directed network
    for param in range(4):
      if model == 'forest':
        g = forest.forest(forest_param[param][0], forest_param[param][1], size)
      elif model == 'price':
        g = price_network(size, m = price_param[param][0], c = price_param[param][1])
      elif model == 'random':
        g = random_graph(size, lambda: numpy.random.binomial(size, random_param[param]), edge_probs=lambda i, k: 0,
                         model="probabilistic-configuration", directed=False, n_iter=100)
      else:
        if param > 0:
          break
        g = load_graph(args.file)
      
      # set to undirected
      g.set_directed(False)
      
      # collect degree sequence
      degree = [v.out_degree() for v in g.vertices()]
      
      if model == 'random' or model == args.file:
        plot.degree_dist(vertex_hist(g, "out"), model + '_' + str(size) + '_' + str(param))
      
      else:
        # calculate exponent
        results = powerlaw.Fit(degree)
        # plot degree
        vis.plplot(numpy.array(degree), results.power_law.xmin, results.power_law.alpha,
                   model + '_' + str(size) + '_' + str(param))
                   
      # uniform removel
      number_cluster, giant_cluster = percolation.uniform_removal(g.copy())
      plot.giant_phi(giant_cluster, model + '_' + str(size) + '_' + str(param) + '_uni')
      plot.cluster_phi(number_cluster, model + '_' + str(size) + '_' + str(param) + '_uni')
      
      # non-uniform
      number_cluster, giant_cluster = percolation.non_uniform_removal(g)
      plot.giant_phi(giant_cluster, model + '_' + str(size) + '_' + str(param) + '_non')
      plot.cluster_phi(number_cluster, model + '_' + str(size) + '_' + str(param) + '_non')
      plot.giant_k0(giant_cluster, model + '_' + str(size) + '_' + str(param) + '_non')
      
