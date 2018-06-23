import powerlaw
import sys
import scipy
import math
import numpy as np
import graph_tool.all as gt 
import matplotlib.pyplot as plt

import vis



G = gt.collection.data[sys.argv[1]]
giant = gt.label_largest_component(G)
origin_size = G.num_vertices()
print('test\n\n\n\n')
for v in range(1, origin_size + 1):
  if giant[origin_size - v] == False:
    G.remove_vertex(origin_size - v, fast = True)
G.set_directed(False)
data = sorted(G.get_out_degrees([v for v in G.vertices()])) # data can be list or numpy array
print('test\n\n\n\n')
print(len(data))
print('test\n\n\n\n')
results = powerlaw.Fit(data)
print(results.power_law.alpha)
print(results.power_law.xmin)
R, p = results.distribution_compare('power_law', 'lognormal')

y = []
x = []

for a in data:
	temp = int(math.log(a))
	if temp in x:
		y[x.index(temp)] += 1
	else:
		x.append(temp)
		y.append(1)

for i in range(len(y)):
	y[i] /= len(data)

x0 = []
y0 = []
step = 1 / len(data)

for a in data:
	temp = round(math.log(a), 2)
	if temp in x0:
		y0[x0.index(temp)] -= step
	else:
		x0.append(temp)
		if len(x0) == 1:
			y0.append(1.)
		else:
			y0.append(y0[len(x0) - 2])

print(x0)	
print(y0)

x1 = [i for i in range(len(x))]
y1 = [math.exp(- (results.power_law.alpha-1) * i) for i in range(len(x))]

#plt.plot(x, y,'bo')
#plt.plot(x0, y0, 'ro')
#plt.plot(x1, y1)
#plt.xscale('log')
#plt.yscale('log')
#plt.show()
#plt.savefig(sys.argv[1].split('/')[-1].split(',')[0] + '.png')

vis.plplot(data, results.power_law.xmin, results.power_law.alpha)

