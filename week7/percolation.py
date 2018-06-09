from graph_tool.all import *
import numpy

def uniform_removal(g):
  orig_size = g.num_vertices()
  number_cluster = []
  giant_cluster = []
  
  # compute giant component's size
  l = label_largest_component(g)
  giant = GraphView(g, vfilt=l).num_vertices()
  
  fraction = -.1
  
  for i in range(orig_size):
    remove = numpy.random.randint(0, orig_size - i)
    g.remove_vertex(remove, fast = True)
    
    # record number of cluster and size of giant cluster
    if float(i) / orig_size - fraction >= .1:
      fraction += 0.1
      _, hist = label_components(g)
      number_cluster.append([len(hist), 1 - fraction])
      giant_cluster.append([max(hist) / giant, 1 - fraction])
    
  return number_cluster, giant_cluster

def non_uniform_removal(g):
  orig_size = g.num_vertices()
  dlist = [v.out_degree() for v in g.vertices()]
  number_cluster = []
  giant_cluster = []
  
  # compute giant component's size
  l = label_largest_component(g)
  giant = GraphView(g, vfilt=l).num_vertices()
  
  fraction = -.01
  
  for i in range(orig_size / 10 * 2):
    remove = numpy.argmax(dlist)
    k0 = dlist[remove]
    dlist[remove] = dlist[-1]
    dlist.pop()
    g.remove_vertex(remove, fast = True)
    
    # record number of cluster and size of giant cluster
    if float(i) / orig_size - fraction >= .01:
      fraction += .01
      _, hist = label_components(g)
      number_cluster.append([len(hist), 1 - fraction, k0])
      giant_cluster.append([max(hist) / giant, 1 - fraction, k0])
    
  return number_cluster, giant_cluster
