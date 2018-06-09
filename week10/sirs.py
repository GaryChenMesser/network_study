from graph_tool.all import *
from numpy import *
from numpy.random import *
import sys, os, os.path
import matplotlib.pyplot as plt


import powerlaw

# SIRS dynamics parameters:

x = 0.005    # spontaneous outbreak probability
r = 0.1      # I->R probability
s = 0.01     # R->S probability
beta = 1

# enumeration
S = 0
I = 1
R = 2


g = price_network(1500, c=0.1)

# Initialize all vertices to the S state
state = g.new_vertex_property("int")
for v in g.vertices():
    state[v] = S

# to record state histogram of each node
state_his = [g.new_vertex_property("double") for i in range(3)]
for v in g.vertices():
    for i in range(3):
       state_his[i][v] = 0

'''
data = sorted(g.get_in_degrees(g.get_vertices())) # data can be list or numpy array
print(len(data))

results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')
'''
# record
s_his = []
i_his = []
r_his = []

# This function will be called repeatedly by the GTK+ main loop, and we use it
# to update the state according to the SIRS dynamics.
def update_state(model = None):
    # visit the nodes in random order
    vs = list(g.vertices())
    shuffle(vs)
    
    # temp state
    temp_s = []
    temp_i = []
    temp_r = []
    
    for v in vs:
        state_his[state[v]][v] += 1
        
        if state[v] == I:
            if random() < r:
                temp_r.append(v)
            else:
                ns = list(v.out_neighbors()) + list(v.in_neighbors())
                if len(ns) == 0:
                    continue
                for n in choice(ns, min(beta, len(ns))):
                    if state[n] == S:
                        temp_i.append(n)
        elif state[v] == S:
            if random() < x:
                temp_i.append(v)
        elif random() < s:
            temp_s.append(v)
        
    # update state
    for _s in temp_s:
        state[_s] = S
    for _i in temp_i:
        state[_i] = I
    for _r in temp_r:
        state[_r] = R

def state_time(_s, _i, _r):
    plt.plot(_s)
    plt.plot(_i)
    plt.plot(_r)
    plt.savefig('price_' + str(beta) + '_' + str(r) + '_' + str(s) + '.png')

def state_degree(his, degree):
    plt.close()
    uniques, counts = unique(degree, return_counts=True)
    print uniques
    print counts
    d = dict()
    for key in uniques:
        d[key] = [0, 0, 0]
    for i, v in enumerate(degree):
        d[v] += his[:,i]
    for key in d:
        d[key] /= sum(d[key])
    plt.plot(d.keys(), d.values())
    plt.savefig('price_' + str(beta) + '_' + str(r) + '_' + str(s) + 'degree.png')
    
for i in range(600):
    update_state()
    if i % 10 == 0:
        uniques, counts = unique(state.a, return_counts=True)
        for n in range(len(uniques)):
            if uniques[n] == S:
                s_his.append(counts[n])
            elif uniques[n] == I:
                i_his.append(counts[n])
            else:
                r_his.append(counts[n])

#state_time(s_his, i_his, r_his)
print g.num_edges()
state_degree(array([state_his[i].a for i in range(3)]), g.get_out_degrees(g.get_vertices()) + g.get_in_degrees(g.get_vertices()))
