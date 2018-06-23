# sis.py

import graph_tool.all as gt
import numpy as np

class siis2_epidemic:
#-------------------------init------------------------------
  def __init__(self, graphml = None, graph = None, seed=2):
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
    
    self.diversity = seed
    self.v_infected = [self.g.new_vertex_property("bool") for i in range(self.diversity)]
    self.v_reinfected = [self.g.new_vertex_property("float") for i in range(self.diversity)]
    self.e_reinfected = [self.g.new_edge_property("float") for i in range(self.diversity)]
    self.e_spread_beta = [self.g.new_edge_property("double") for i in range(self.diversity)]
    self.e_extinct_beta = [self.g.new_edge_property("double") for i in range(self.diversity)]
    
    self.threshold = 2
    self.activate = [self.threshold for v in self.g.vertices()]
    
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
      self._update_state(True)
    
    self._infection_amplifier(True)
    
  def _init_spread(self, first_time, patient_zero):
    if first_time == True:
      eigenvalue, _ = gt.eigenvector(self.g)
      self.spread_beta = 0.5
      self.spread_delta = 0.5
      print("Spreading:\n    Largest eigenvalue: {}\n    beta: {}\n    delta: {}"\
            .format(eigenvalue, self.spread_beta, self.spread_delta))
      print("\n-----------------------------------------")
      
      for e in self.g.edges():
        for i in range(self.diversity):
          self.e_spread_beta[i][e] = self.spread_beta
        
    self.infected_list = [{patient_zero[i] : None} for i in range(self.diversity)] 
        
    for v in self.g.vertices():
      for i in range(self.diversity):
        self.v_reinfected[i][v] = 0
        self.v_infected[i][v] = False
    for e in self.g.edges():
      for i in range(self.diversity):
        self.e_reinfected[i][e] = 0
    
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
    
    #self._infection_amplifier(False)
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
        for i in range(self.diversity):
          self.e_extinct_beta[i][e] = self.extinct_beta
    
    self.infected_list = [{v : None for v in self.g.vertices()}, {}]
        
    for v in self.g.vertices():
      for i in range(self.diversity):
        self.v_infected[i][v] = True
        self.v_reinfected[i][v] = 0
    for e in self.g.edges():
      for i in range(self.diversity):
        self.e_reinfected[i][e] = 0
      
#-----------------shared epidemic method----------------------------  
  def _update_state(self, flag):
    _return = False
    
    if flag == True:
      e_beta = [self.e_spread_beta[i].copy() for i in range(self.diversity)]
      delta = self.spread_delta
    else:
      e_beta = [self.e_extinct_beta[i].copy() for i in range(self.diversity)]
      delta = self.extinct_delta
    '''
    if flag == True:
      for v, active in enumerate(self.activate):
        if active < self.threshold:
          for n in self.g.vertex(v).out_neighbors():
            for i in range(self.diversity):
              e_beta[i][self.g.edge(v, n)] *= 0.5
    '''
    self.activate = [0 for v in self.g.vertices()]
    
    last_reinfection = [self.v_reinfected[i].copy() for i in range(self.diversity)]
    temp = [list(self.infected_list[i].keys()) for i in range(self.diversity)]
    
    for i in range(2):
      if len(temp[i]) > 0:
        recover_list = {v : None for v in self.g.vertices() if np.random.random() < delta}
        
        for v in temp[i]:
          for neighbor in self.g.vertex(v).out_neighbors():
            if np.random.random() < e_beta[i][self.g.edge(v, neighbor)]:
              if neighbor not in temp[(i + 1) % 2]:
                self._infection(v, neighbor, i)
              else:
                self._attack(neighbor, (i + 1) % 2)
      
    for i in range(2):
      if len(temp[i]) > 0:
        for v in temp[i]:
          if v in recover_list and last_reinfection[i][v] >= self.v_reinfected[i][v]:
            self._recovery(v, i)
        
        print("After: {}  {}".format(len(self.infected_list[0]), len(self.infected_list[1])))
        _return = True
    
    return _return
  
  def _attack(self, n, i):
    self.v_reinfected[i][n] -= 1
  
  def _infection(self, v, n, i):
    self.infected_list[i][n] = None
    self.v_infected[i][n] = True
    self.v_reinfected[i][n] += 1
    self.activate[int(n)] += 1
    
    self.e_reinfected[i][self.g.edge(v, n)] += 1
    
  def _recovery(self, v, i):
    del self.infected_list[i][v]
    self.v_infected[i][v] = False
    
  def _infection_amplifier(self, flag):
    #maximum = max(self.e_reinfected)
    
    for i in range(self.diversity):
      total_reinfection = 0.
      total_beta = 0.
      for e in self.g.edges():
        total_reinfection += self.e_reinfected[i][e]
        if flag == True:
          total_beta += self.e_spread_beta[i][e]
        else:
          total_beta += self.e_extinct_beta[i][e]
      for e in self.g.edges():
        if flag == True:
          self.e_spread_beta[i][self.g.edge(e.target(), e.source())] = \
          total_beta * self.e_reinfected[i][e] / total_reinfection
        else:
          self.e_extinct_beta[i][self.g.edge(e.target(), e.source())] = \
          total_beta * self.e_reinfected[i][e] / total_reinfection
