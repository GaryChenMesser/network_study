import plot
import powerlaw
import vis
import numpy
import sys

with open('heat_dense.txt') as f:
	data = f.read().split('\n')
	print(data)
	exponent = [map(float, data[i].split(',')) for i in range(len(data))]

with open('heat_shrink.txt') as f:
	data = f.read().split('\n')
	print(data)
	diameter = [map(float, data[i].split(',')) for i in range(len(data))]


# plot heatmap of density
plot.heat_dense(exponent)

# plot heatmap of density
plot.heat_shrink(diameter)
