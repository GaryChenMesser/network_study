# sis.py

import graph_tool.all as gt
import numpy as np

class sis_epidemic:
#-------------------------init------------------------------
  def __init__(self, graphml = None, graph = None):
    if graphml != None:
      self.g = gt.load_graph(graphml)
      #self.v_name = self.g.new_edge_property("str")
      print(self.g.list_properties	())
      
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
    
    self.v_infected = self.g.new_vertex_property("bool")
    self.v_reinfected = self.g.new_vertex_property("int")
    self.e_reinfected = self.g.new_edge_property("int")
    self.e_spread_beta = self.g.new_edge_property("double")
    self.e_extinct_beta = self.g.new_edge_property("double")

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
      self._update_state(True)
    
    self._infection_amplifier(True)
    #print(list(self.e_spread_beta))
    #print(list(self.e_reinfected))
    
  def _init_spread(self, first_time, patient_zero):
    if first_time == True:
      eigenvalue, _ = gt.eigenvector(self.g)
      self.spread_beta = 0.05
      self.spread_delta = 0.05
      print("Spreading:\n    Largest eigenvalue: {}\n    beta: {}\n    delta: {}"\
            .format(eigenvalue, self.spread_beta, self.spread_delta))
      print("\n-----------------------------------------")
      
      for e in self.g.edges():
        self.e_spread_beta[e] = self.spread_beta
    
    self.infected_list = {patient_zero : None}
        
    for v in self.g.vertices():
      self.v_reinfected[v] = 0
      self.v_infected[v] = False
    for e in self.g.edges():
      self.e_reinfected[e] = 0
    
#---------------under epidemic threshold----------------------- 
  def extinction(self, first_time):
    self._init_extinction(first_time)
    
    print('Start Extinction.')
    
    while self._update_state(False):
      #self.g.set_vertex_filter(self.v_infected)
      #comp, hist = gt.label_components(self.g)
      #print("Number of components: {}".format(len(hist)))
      #print(hist)
      #self.g.clear_filters()
      pass
    
    self._infection_amplifier(False)
    #print(list(self.e_extinct_beta))
    
    print("\n-----------------------------------------")
    
  def _init_extinction(self, first_time):
    if first_time == True:
      eigenvalue, _ = gt.eigenvector(self.g)
      self.extinct_beta = 0.9 / eigenvalue
      self.extinct_delta = 0.9
      print("Extinction:\n    Largest eigenvalue: {}\n    beta: {}\n    delta: {}"\
            .format(eigenvalue, self.extinct_beta, self.extinct_delta))
      print("\n-----------------------------------------")
      
      for e in self.g.edges():
        self.e_extinct_beta[e] = self.extinct_beta
    
    self.infected_list = {v : None for v in self.g.vertices()}
    
    for v in self.g.vertices():
      self.v_infected[v] = True
      self.v_reinfected[v] = 0
    for e in self.g.edges():
      self.e_reinfected[e] = 0
    
#-----------------shared epidemic method----------------------------  
  def _update_state(self, flag):
    if flag == True:
      e_beta = self.e_spread_beta
      delta = self.spread_delta
    else:
      e_beta = self.e_extinct_beta
      delta = self.extinct_delta
    if len(self.infected_list) > 0:
      recover_list = {v : None for v in self.g.vertices() if np.random.random() < delta}
      
      temp = list(self.infected_list.keys())
      last_reinfection = self.v_reinfected.copy()
      
      for v in temp:
        for neighbor in self.g.vertex(v).out_neighbors():
          if np.random.random() < e_beta[self.g.edge(v, neighbor)]:
            self._infection(v, neighbor)
      
      for v in temp:
        if v in recover_list and last_reinfection[v] == self.v_reinfected[v]:
          self._recovery(v)
          
      print("Before: {}  After: {}".format(len(temp), len(self.infected_list)))
      return True
    
    else:
      return False

  def _infection(self, v, n):
    self.infected_list[n] = None
    self.v_infected[n] = True
    self.v_reinfected[n] += 1
    
    self.e_reinfected[self.g.edge(v, n)] += 1
    
  def _recovery(self, v):
    del self.infected_list[v]
    self.v_infected[v] = False
    
  def _infection_amplifier(self, flag):
    #maximum = max(self.e_reinfected)
    total_reinfection = 0.
    total_beta = 0.
    for e in self.g.edges():
      total_reinfection += self.e_reinfected[e]
      if flag == True:
        total_beta += self.e_spread_beta[e]
      else:
        total_beta += self.e_extinct_beta[e]
    for e in self.g.edges():
      if flag == True:
        self.e_spread_beta[self.g.edge(e.target(), e.source())] = \
        total_beta * self.e_reinfected[e] / total_reinfection
      else:
        self.e_extinct_beta[self.g.edge(e.target(), e.source())] = \
        total_beta * self.e_reinfected[e] / total_reinfection
