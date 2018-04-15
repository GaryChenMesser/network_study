import plot
import powerlaw
import vis
import numpy
import sys

with open('degree.txt') as f:
	degree = map(int, f.read().split(','))

with open('node_edge.txt') as f:
	data = f.read().split('\n')
	node = map(int, data[0].split(','))
	edge = map(int, data[1].split(','))

with open('diameter.txt') as f:
	data = f.read().split('\n')
	diameter = map(int, data[0].split(','))

# calculate exponent
results = powerlaw.Fit(degree)
print(results.power_law.alpha)
print(results.power_law.xmin)
# plot degree
vis.plplot(numpy.array(degree), results.power_law.xmin, results.power_law.alpha)

# plot node_edge
plot.node_edge(node, edge)

# plot diameter
plot.diameter(diameter, node)
