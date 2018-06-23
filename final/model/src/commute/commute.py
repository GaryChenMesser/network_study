# commute.py

import graph_tool.all as gt
import numpy as np
import random
import time

class Commute:
#-------------------------init------------------------------
  def __init__(self, graphml = None, graph = None):
    if graphml != None:
      self.g = gt.load_graph(graphml)
      self.g.set_directed(False)
      print("Create graph from graphml {}".format(graphml))
      
    elif graph != None:
      self.g = graph
      giant = gt.label_largest_component(self.g)
      origin_size = self.g.num_vertices()
      for v in range(1, origin_size + 1):
        if giant[origin_size - v] == False:
          self.g.remove_vertex(origin_size - v, fast = True)
      self.g.set_directed(False)
      print("Create graph from graph.")
      
    else:
      print("No graphml or graph are provided!")
    
    print("Number of vertices: {}\nNumber of edges: {}"\
          .format(self.g.num_vertices(), self.g.num_edges()))
    print("\n-----------------------------------------")
    
    self.v_residents = self.g.new_vertex_property("object")
    self.e_weights = self.g.new_edge_property("float")
    self.e_filter = self.g.new_edge_property("bool")
    self.walkers = [{} for v in self.g.vertices()]
    
    self.boost_size = 100  
    self.random_boost = [[100, [0 for i in range(self.boost_size)]] for v in self.g.vertices()]
    self.exetime = [0., 0., 0., 0.]
    
#-----------------------get method------------------------
  def get_graph(self):
    return self.g

  def get_weight(self):
    return self.e_weights
  
  def get_modularity(self):
    return gt.modularity(self.g, self.g.vertex_properties['comm'], weight=self.e_weights)

#---------------------public method-----------------------
  def travel(self, update_times, first_time = True):
    self._init_travel(first_time)
    
    for i in range(update_times):
      print("{}th update:".format(i), end='\r')
      self._update_travel()
  
  def remove(self, minimum):
    for e in self.g.edges():
      if self.e_weights[e] <= minimum:
        if e.source().out_degree() > 1 and e.target().in_degree() > 1:
          self.e_filter[e] = False
          self.g.set_edge_filter(prop=self.e_filter)
          for v in self.g.vertices():
            if v.out_degree() == 0:
              print('error!!!!!!!!!!!\n\n\n\n\n\n\n')
              print(int(v))
              print(int(e.source()))
              print(int(e.target()))
  
  def normalize(self):
    _min = np.inf
    for e in self.g.edges():
      if self.e_weights[e] < _min:
        _min = self.e_weights[e]
     
    for e in self.g.edges():
      self.e_weights[e] -= (_min - 1)

#---------------------private method-----------------------
  def _init_travel(self, first_time):
    for v in self.g.vertices():
      self.v_residents[v] = [int(v)]
      self.walkers[int(v)] = {}
    if first_time:
      for e in self.g.edges():
        self.e_weights[e] = 1.
        self.e_filter[e] = True
  
  def _update_travel(self):
    for v in self.g.vertices():
      if len(self.v_residents[v]) > 0:
        next = self._choosing(v, len(self.v_residents[v]))
        self._moving(self.v_residents[v], v, next)
      
  def _choosing(self, v, size):
    _return = []
    
    for i in range(size):
      if self.random_boost[int(v)][0] >= self.boost_size:
        self.random_boost[int(v)][1] = self._rechoosing(v)
        self.random_boost[int(v)][0] = 0
      
      #print('test {}'.format(self.random_boost[int(v)][0]))
      _return.append(self.random_boost[int(v)][1][self.random_boost[int(v)][0]])
      self.random_boost[int(v)][0] += 1
    
    return _return
  
  def _rechoosing(self, v):
    edge = self.g.get_out_edges(v)
    degree = v.out_degree(weight=self.e_weights)
    return np.random.choice(edge[:, 1], self.boost_size, list(map(lambda x: self.e_weights[self.g.edge(x[0], x[1])] / degree, edge)))
    #choice = np.random.randint(v.out_degree(self.e_weights), size=size)
    
    #for i in range(size):
    #  for e in edge:
    #    choice[i] -= self.e_weights[self.g.edge(e[0], e[1])]
    #    if choice[i] < 0:
    #      _return.append(e[1])
    #      break
    #return np.random.choice(edge[:, 1], size, weight)
    #return random.choices(edge[:, 1], weight, size)
    
  def _moving(self, w, v, next):
    for walker, n in zip(w, next):
      self.v_residents[v].remove(walker)
      self.v_residents[n].append(walker)
    
      if v in self.walkers[walker]: # commute!
        self._commute(walker, v, n)
      else:
        self.walkers[walker][v] = n
    
  def _commute(self, walker, v, n):
    temp = v
    while self.walkers[walker][temp] != v:
      self.e_weights[self.g.edge(temp, self.walkers[walker][temp])] += 1.
      if temp != v:
        temp = self.walkers[walker].pop(temp)
      else:
        temp = self.walkers[walker][temp]
    temp = self.walkers[walker].pop(temp)
    self.walkers[walker][temp] = n
