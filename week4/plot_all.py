import plot
import powerlaw
import vis
import numpy
import sys

with open('degree.txt') as f:
	data = f.read().split('\n')
	degree = []
	for a in range(len(data)):
		degree.append(map(int, data[a].split(',')))

with open('node_edge.txt') as f:
	data = f.read().split('\n')
	node = map(int, data[0].split(','))
	edge = map(int, data[1].split(','))

with open('diameter.txt') as f:
	data = f.read().split('\n')
	diameter = map(float, data[0].split(','))

# plot node_edge
plot.node_edge(node, edge)

# plot diameter
plot.diameter(diameter, node)

results = []
# calculate exponent
for a in range(len(degree)):
	results.append(powerlaw.Fit(degree[a]))
	print(results[a].power_law.alpha)
	print(results[a].power_law.xmin)
# plot degree
vis.plplot(numpy.array(degree[0]), results[0].power_law.xmin, results[0].power_law.alpha, 'in')
if len(degree) > 1:
	vis.plplot(numpy.array(degree[1]), results[0].power_law.xmin, results[0].power_law.alpha, 'out')

