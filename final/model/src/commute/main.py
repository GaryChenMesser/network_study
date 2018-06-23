import graph_tool.all as gt
import numpy as np
import sys
import time

import commute

model = commute.Commute(graphml=sys.argv[1])

model.travel(1)
print('modularity = {}'.format(model.get_modularity()))
start = time.time()
model.travel(40)
print("time: {}".format(time.time() - start))
print('modularity = {}'.format(model.get_modularity()))
model.normalize()
#model.remove(3)
#model.travel(40, False)
print('modularity = {}'.format(model.get_modularity()))
model.normalize()
#model.remove(3)
#model.travel(40, False)
print('modularity = {}'.format(model.get_modularity()))
#for i in range(10):
#  model.travel(5, False)
#  print('modularity = {}'.format(model.get_modularity()))

g = model.get_graph()
weight = model.get_weight()
edge = g.get_edges()
label = g.vertex_properties['label']

with open(sys.argv[2] + '.dat', 'w') as f:
  for e in edge:
    f.write(str(label[e[0]]) + '	' + str(label[e[1]]) + '	' + str(weight[g.edge(e[0], e[1])]))
    f.write('\n')
print(sys.argv[2] + '.dat')
