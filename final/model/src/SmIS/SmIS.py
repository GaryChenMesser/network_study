# SmIS.py

import graph_tool.all as gt
import numpy as np
import random

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
      self.v_reinfected[n] -= 1
    
    # infect
    else:
      self.v_infected[n] = self.v_infected[v]
      if self.v_infected[n] == 0 and self.v_reinfected[n] != 0:
        print('error!!!\n\n\n\n\n\n\n\n\n\n')
      self.v_reinfected[n] += 1
      #self.e_reinfected[self.g.edge(v, n)] += 1
  
  def _recovery(self, v):
    self.v_infected[v] = 0
    self.v_reinfected[v] = 0
