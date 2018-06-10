import graph_tool.all as gt
import numpy as np
import matplotlib.pyplot as plt
import sys

import SmIS


model = SmIS.SmIS_epidemic(graphml=sys.argv[1])

g = model.get_g()

v_sequence = list(range(g.num_vertices()))
np.random.shuffle(v_sequence)


model.spreading(True, v_sequence[:300], 100)
#model.spreading(False, [0, 600], 24)


v_infected = model.get_v_infected()
v_reinfected = model.get_v_reinfected()
reindex = {}
index = 0
for v in g.vertices():
  if v_infected[v] not in reindex:
    reindex[v_infected[v]] = index
    index += 1

print('left number of virus: {}'.format(index))

with open(sys.argv[2] + '.dat', 'w') as f:
  for i, v in enumerate(g.vertices()):
    f.write(str(i + 1) + '	' + str(reindex[v_infected[v]]))
    f.write('\n')
print(sys.argv[2] + '.dat')
