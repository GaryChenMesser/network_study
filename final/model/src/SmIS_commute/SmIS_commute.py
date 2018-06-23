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
    self.g.edge_properties["weight"] = self.e_weights
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

class SmIS_epidemic:
#-------------------------init------------------------------
  def __init__(self, graphml = None, graph = None):
    if graphml != None:
      self.g = gt.load_graph(graphml)
      #self.v_name = self.g.new_edge_property("str")
      print(self.g.list_properties())
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
    
    self.diversity = 0
    self.e_weights = self.g.edge_properties["weight"]
    self.v_infected = self.g.new_vertex_property("int")
    self.v_reinfected = self.g.new_vertex_property("float")
    self.e_reinfected = self.g.new_edge_property("float")
    self.e_spread_beta = self.g.new_edge_property("double")
    
    self.threshold = 2
    self.activate = self.g.new_vertex_property("float")
    
#-----------------------get method------------------------
  def get_g(self):
    return self.g
  
  def get_v_infected(self):
    return self.v_infected
  
  def get_v_reinfected(self):
    return self.v_reinfected
  
  def get_v_comm(self):
    return self.g.vertex_properties['comm']

#---------------beyond epidemic threshold-------------------
  def spreading(self, first_time, patient_zero, update_times):
    self._init_spread(first_time, patient_zero)
    
    print('Start spreading.')
    
    for i in range(update_times):
      print("{}th update:".format(i))
      self._update_state()
    
    self._voting()
  
#-----------------private epidemic method----------------------------
  def _init_spread(self, first_time, patient_zero):
    if first_time == True:
      eigenvalue, _ = gt.eigenvector(self.g)
      self.spread_beta = 0.5
      self.spread_delta = 0.8
      print("Spreading:\n    Largest eigenvalue: {}\n    beta: {}\n    delta: {}"\
            .format(eigenvalue, self.spread_beta, self.spread_delta))
      print("\n-----------------------------------------")
      
      for e in self.g.edges():
        self.e_spread_beta[e] = self.spread_beta
        
    for v in self.g.vertices():
      self.v_reinfected[v] = 0
      self.v_infected[v] = 0
      self.activate[v] = self.threshold
    for e in self.g.edges():
      self.e_reinfected[e] = 0
    
    for virus, patient in enumerate(patient_zero):
      self.v_infected[patient] = virus + 1
    
  def _update_state(self):
    _return = False
    
    e_beta = self.e_spread_beta
    delta = self.spread_delta
    
    #for v in self.g.vertices():
    #  self.v_reinfected[v] = 0

    total = 0
    for v in self.g.vertices():
      total += self.v_infected[v]
    
    if total > 0:
      temp_list = self.v_infected.copy()
      
      recover_list = [False for v in self.g.vertices()]

      v_sequence = list(range(self.g.num_vertices()))
      np.random.shuffle(v_sequence)

      for v in v_sequence:
        if temp_list[v] != 0:
          if np.random.random() < delta:
            recover_list[v] = True
          
          chosen = np.random.randint(self.g.vertex(v).out_degree())
          for i, neighbor in enumerate(self.g.vertex(v).out_neighbors()):
            if i == chosen:
              if np.random.random() < e_beta[self.g.edge(v, neighbor)]:
                self._infection_or_attack(v, neighbor)
      
      for v, r in enumerate(recover_list):
        if r and self.v_reinfected[v] <= self.g.vertex(v).out_degree() * self.spread_beta * 0.0: # FIXME: This condition make corner node unstable. For example, no neighbor virus dominates.
          self._recovery(v)
      
      u, count = np.unique(self.v_infected.a, return_counts=True)
      print("After: \n{}\n{}".format(len(count), count))
      _return = True
    
    return _return
  
  def _voting(self):
    for v in self.g.vertices():
      voter = {}
      if self.v_infected[v] == 0:
        for neighbor in self.g.vertex(v).out_neighbors():
          if self.v_infected[neighbor] in voter:
            voter[self.v_infected[neighbor]] += 1
          else:
            voter[self.v_infected[neighbor]] = 1
        
        elected = max(voter, key=voter.get)
        if elected == 0:
          del voter[elected]
          elected = max(voter, key=voter.get)
          
        self.v_infected[v] = elected
  
  def _infection_or_attack(self, v, n):
    # attack
    if self.v_infected[n] != 0 and self.v_infected[v] != self.v_infected[n]:
      self.v_reinfected[n] -= self.e_weights[self.g.edge(v, n)]
    
    # infect
    else:
      self.v_infected[n] = self.v_infected[v]
      if self.v_infected[n] == 0 and self.v_reinfected[n] != 0:
        print('error!!!\n\n\n\n\n\n\n\n\n\n')
      self.v_reinfected[n] += self.e_weights[self.g.edge(v, n)]
      #self.e_reinfected[self.g.edge(v, n)] += 1
  
  def _recovery(self, v):
    self.v_infected[v] = 0
    self.v_reinfected[v] = 0
