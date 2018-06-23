import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import sys
import time

import SmIS_commute

model = SmIS_commute.Commute(graphml=sys.argv[1])

model.travel(1)
print('modularity = {}'.format(model.get_modularity()))
start = time.time()
#model.travel(40)
print("time: {}".format(time.time() - start))
print('modularity = {}'.format(model.get_modularity()))
model.normalize()
model.remove(3)
model.travel(40, False)
print('modularity = {}'.format(model.get_modularity()))
model.normalize()
model.remove(3)
model.travel(40, False)
print('modularity = {}'.format(model.get_modularity()))
#for i in range(10):
#  model.travel(5, False)
#  print('modularity = {}'.format(model.get_modularity()))

g = model.get_graph()

model = SmIS_commute.SmIS_epidemic(graph=g)

g = model.get_g()

v_sequence = list(range(g.num_vertices()))
np.random.shuffle(v_sequence)

model.spreading(True, v_sequence[:300], 120)
#model.spreading(False, [0, 600], 24)


v_infected = model.get_v_infected()
v_reinfected = model.get_v_reinfected()
label = g.vertex_properties['label']
reindex = {}
label_table = {}
index = 0
count = 0
for v in g.vertices():
  count += 1
  label_table[label[v]] = int(v)
  if v_infected[v] not in reindex:
    reindex[v_infected[v]] = index
    index += 1
print(count)
print('left number of virus: {}'.format(index))

label = g.vertex_properties['label']

with open(sys.argv[2] + '.dat', 'w') as f:
  for i, v in enumerate(g.vertices()):
    f.write(str(i + 1) + '	' + str(reindex[v_infected[label_table[i + 1]]]))
    f.write('\n')
print(sys.argv[2] + '.dat')
