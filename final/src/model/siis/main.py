import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import sys

import sis
import siis

#model = siis.siis_epidemic(graphml=sys.argv[1])

graph = gt.collection.data["polblogs"]
model = siis.siis_epidemic(graph=graph, seed=2)

#model.extinction(True)
'''
v_comm = model.get_v_comm()
'''

model.spreading(True, [0, 600], 24)
model.spreading(False, [0, 600], 24)

'''
v_infected = [n[0] + n[1] for n in list(model.get_v_reinfected())]
kernel1 = v_infected.index(max(v_infected))
v_infected.pop(kernel1)
kernel2 = v_infected.index(max(v_infected))
while v_comm[kernel1] == v_comm[kernel2]:
  v_infected.pop(kernel2)
  kernel2 = v_infected.index(max(v_infected))
'''

#model.spreading(False, kernel, 24)
#v_infected = list(model.get_v_reinfected())
#kernel = v_infected.index(max(v_infected))

#model.spreading(False, kernel, 24)
#model.spreading(True, [kernel1, kernel2], 24)
#model.spreading(False, [kernel1, kernel2], 24)

g = model.get_g()
v_infected = model.get_v_infected()
v_reinfected = model.get_v_reinfected()

#print(list(v_reinfected))
#print(data)
'''
v_comm = model.get_v_comm()

size1 = 0
size2 = 0

inf1 = [0, 0]
inf2 = [0, 0]

reinf1 = [0, 0]
reinf2 = [0, 0]
for v in g.vertices():
  if v_comm[v] == 1:
    inf1[0] += v_infected[0][v]
    reinf1[0] += v_reinfected[0][v]
    inf1[1] += v_infected[1][v]
    reinf1[1] += v_reinfected[1][v]
    size1 += 1
  elif v_comm[v] == 2:
    inf2[0] += v_infected[0][v]
    reinf2[0] += v_reinfected[0][v]
    inf2[1] += v_infected[1][v]
    reinf2[1] += v_reinfected[1][v]
    size2 += 1
  else:
    print('error!!!!!!!!!!!!')

print('size1: {}  size2: {}'.format(size1, size2))
print('community1: {},{}  community2: {},{}'.format(inf1[0], inf1[1], inf2[0], inf2[1]))
print('community1: {},{}  community2: {},{}'.format(inf1[0] / size1, inf1[1] / size1, inf2[0] / size2, inf2[1] / size2))
print('community1: {},{}  community2: {},{}'.format(reinf1[0], reinf1[1], reinf2[0], reinf2[1]))
print('community1: {},{}  community2: {},{}'.format(reinf1[0] / size1, reinf1[1] / size1, reinf2[0] / size2, reinf2[1] / size2))
#print('kernel1: {}  kernel2: {}'.format(kernel1, kernel2))
#print('kernel1: {}  kernel2: {}'.format(v_comm[kernel1], v_comm[kernel2]))
print('kernel1: {}  kernel2: {}'.format(v_comm[0], v_comm[700]))
'''

pos = gt.sfdp_layout(g)
gt.graph_draw(g, pos=pos, vertex_fill_color=v_reinfected[0], output="test_amplify1.pdf")
gt.graph_draw(g, pos=pos, vertex_fill_color=v_reinfected[1], output="test_amplify2.pdf")
gt.graph_draw(g, pos=pos, vertex_fill_color=v_infected[0], output="test_amplify3.pdf")
gt.graph_draw(g, pos=pos, vertex_fill_color=v_infected[1], output="test_amplify4.pdf")
