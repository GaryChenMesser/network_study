import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import sys

import sis

model = sis.sis_epidemic(graphml=sys.argv[1])

#graph = gt.collection.data["polblogs"]
#model = sis.sis_epidemic(graph=graph)

model.extinction(True)
v_infected = list(model.get_v_reinfected())
kernel = v_infected.index(max(v_infected))

model.spreading(True, kernel, 24)
v_infected = list(model.get_v_reinfected())
kernel = v_infected.index(max(v_infected))

#model.spreading(False, kernel, 24)
#v_infected = list(model.get_v_reinfected())
#kernel = v_infected.index(max(v_infected))

#model.spreading(False, kernel, 24)
model.spreading(False, kernel, 24)

g = model.get_g()
v_infected = model.get_v_infected()
v_reinfected = model.get_v_reinfected()

#print(list(v_reinfected))
#print(data)

v_comm = model.get_v_comm()

size1 = 0
size2 = 0

inf1 = 0
inf2 = 0

reinf1 = 0
reinf2 = 0
for v in g.vertices():
  if v_comm[v] == 1:
    inf1 += v_infected[v]
    reinf1 += v_reinfected[v]
    size1 += 1
  elif v_comm[v] == 2:
    inf2 += v_infected[v]
    reinf2 += v_reinfected[v]
    size2 += 1
  else:
    print('error!!!!!!!!!!!!')

print('size1: {}  size2: {}'.format(size1, size2))
print('community1: {}  community2: {}'.format(inf1, inf2))
print('community1: {}  community2: {}'.format(inf1 / size1, inf2 / size2))
print('community1: {}  community2: {}'.format(reinf1, reinf2))
print('community1: {}  community2: {}'.format(reinf1 / size1, reinf2 / size2))


pos = gt.sfdp_layout(g)
#gt.graph_draw(g, pos=pos, vertex_fill_color=v_reinfected, output="test.pdf")
